"""
Base for this code is from Daniel Bader's schedule library [1]. Code was edited for the purposes of this app.
[1] https://github.com/dbader/schedule
"""
from collections.abc import Hashable
import datetime
import functools
import logging
import random
import re
import time
from typing import Set, List, Optional, Callable, Union
import queue
import os
import app.modules.misc.errors as errors
import json

JOBS_EXPORT_FILE_NAME = "schedule.json"
used_functions = {}

logger = logging.getLogger("schedule")


class ScheduleError(Exception):
    """Base schedule exception"""
    pass


class ScheduleValueError(ScheduleError):
    """Base schedule value error"""
    pass


class IntervalError(ScheduleValueError):
    """An improper interval was used"""
    pass


class CancelJob(object):
    """
    Can be returned from a job to unschedule itself.
    """
    pass


class Scheduler(object):
    """
    Objects instantiated by the :class:`Scheduler <Scheduler>` are
    factories to create jobs, keep record of scheduled jobs and
    handle their execution.
    """

    def __init__(self) -> None:
        self.jobs: List[Job] = []

    def run_pending(self) -> None:
        """
        Run all jobs that are scheduled to run.
        Please note that it is *intended behavior that run_pending()
        does not run missed jobs*. For example, if you've registered a job
        that should run every minute and you only call run_pending()
        in one hour increments then your job won't be run 60 times in
        between but only once.
        """
        runnable_jobs = (job for job in self.jobs if job.should_run)
        for job in sorted(runnable_jobs):
            self._run_job(job)

    def get_jobs(self, tag: Optional[Hashable] = None) -> List["Job"]:
        """
        Gets scheduled jobs marked with the given tag, or all jobs
        if tag is omitted.
        :param tag: An identifier used to identify a subset of
                    jobs to retrieve
        """
        if tag is None:
            return self.jobs[:]
        else:
            return [job for job in self.jobs if tag in job.tags]

    def export_jobs(self, filename: str = JOBS_EXPORT_FILE_NAME):
        if not os.path.isdir(os.path.abspath("./config")):
            raise errors.ConfigFolderMissingError("Config folder was not found. The app needs reinitialization.")
        jobs_list = [job.as_dictionary() for job in self.jobs]

        with open(os.path.join(os.path.abspath("./config"), filename), "w+", encoding="UTF-8") as jobs_export:
            jobs_export.writelines(json.dumps(jobs_list, indent=4))

    def import_jobs(self, filename: str = JOBS_EXPORT_FILE_NAME):
        if not os.path.isdir(os.path.abspath("./config")):
            raise errors.ConfigFolderMissingError("Config folder was not found. The app needs reinitialization.")
        file_path = os.path.join(os.path.abspath("./../config"), filename)
        if not os.path.isfile(file_path):
            raise errors.ConfigFileMissingError("Jobs file was not found. Any jobs were stored.")

        with open(file_path, "r", encoding="UTF-8") as jobs_import:
            jobs_list = json.loads(jobs_import.read())

        for job in jobs_list:
            sched_job = Job(1)
            # sched_job.from_dictionary(job, self)
            try:
                sched_job.from_dictionary(job, self)
            except Exception as e:  # TODO: better exception
                logger.debug('Job could not been imported "%s"', str(job))
            else:
                self.jobs.append(sched_job)

    def clear(self, tag: Optional[Hashable] = None) -> None:
        """
        Deletes scheduled jobs marked with the given tag, or all jobs
        if tag is omitted.
        :param tag: An identifier used to identify a subset of
                    jobs to delete
        """
        if tag is None:
            logger.debug("Deleting *all* jobs")
            del self.jobs[:]
        else:
            logger.debug('Deleting all jobs tagged "%s"', tag)
            self.jobs[:] = (job for job in self.jobs if tag not in job.tags)

    def cancel_job(self, job: "Job") -> None:
        """
        Delete a scheduled job.
        :param job: The job to be unscheduled
        """
        try:
            logger.debug('Cancelling job "%s"', str(job))
            self.jobs.remove(job)
        except ValueError:
            logger.debug('Cancelling not-scheduled job "%s"', str(job))

    def every(self, interval: int = 1) -> "Job":
        """
        Schedule a new periodic job.
        :param interval: A quantity of a certain time unit
        :return: An unconfigured :class:`Job <Job>`
        """
        job = Job(interval, self)
        return job

    def _run_job(self, job: "Job") -> None:
        ret = job.run()
        if isinstance(ret, CancelJob) or ret is CancelJob:
            self.cancel_job(job)

    @property
    def next_run(self) -> Optional[datetime.datetime]:
        """
        Datetime when the next job should run.
        :return: A :class:`~datetime.datetime` object
                 or None if no jobs scheduled
        """
        if not self.jobs:
            return None
        return min(self.jobs).next_run


def _decode_datetimestr(
        datetime_str: str, formats: List[str]
) -> Optional[datetime.datetime]:
    for f in formats:
        try:
            return datetime.datetime.strptime(datetime_str, f)
        except ValueError:
            pass
    return None


class Job(object):
    """
    A periodic job as used by :class:`Scheduler`.
    :param interval: A quantity of a certain time unit
    :param scheduler: The :class:`Scheduler <Scheduler>` instance that
                      this job will register itself with once it has
                      been fully configured in :meth:`Job.do()`.
    Every job runs at a given fixed time interval that is defined by:
    * a :meth:`time unit <Job.second>`
    * a quantity of `time units` defined by `interval`
    A job is usually created and returned by :meth:`Scheduler.every`
    method, which also defines its `interval`.
    """

    def __init__(self, interval: int, scheduler: Scheduler = None):
        self.interval: int = interval  # pause interval * unit between runs
        self.latest: Optional[int] = None  # upper limit to the interval
        self.job_func: Optional[functools.partial] = None  # the job job_func to run

        # time units, e.g. 'minutes', 'hours', ...
        self.unit: Optional[str] = None

        # optional time at which this job runs
        self.at_time: Optional[datetime.time] = None

        # datetime of the last run
        self.last_run: Optional[datetime.datetime] = None

        # datetime of the next run
        self.next_run: Optional[datetime.datetime] = None

        # timedelta between runs, only valid for
        self.period: Optional[datetime.timedelta] = None

        self.tags: Set[Hashable] = set()  # unique set of tags for the job
        self.scheduler: Optional[Scheduler] = scheduler  # scheduler to register with

    def __lt__(self, other) -> bool:
        """
        PeriodicJobs are sortable based on the scheduled time they
        run next.
        """
        return self.next_run < other.next_run

    def __str__(self) -> str:
        if hasattr(self.job_func, "__name__"):
            job_func_name = self.job_func.__name__  # type: ignore
        else:
            job_func_name = repr(self.job_func)

        return "Job(interval={}, unit={}, do={}, args={}, kwargs={})".format(
            self.interval,
            self.unit,
            job_func_name,
            "()" if self.job_func is None else self.job_func.args,
            "{}" if self.job_func is None else self.job_func.keywords,
        )

    def __repr__(self):
        def format_time(t):
            return t.strftime("%Y-%m-%d %H:%M:%S") if t else "[never]"

        def is_repr(j):
            return not isinstance(j, Job)

        timestats = "(last run: %s, next run: %s)" % (
            format_time(self.last_run),
            format_time(self.next_run),
        )

        if hasattr(self.job_func, "__name__"):
            job_func_name = self.job_func.__name__
        else:
            job_func_name = repr(self.job_func)
        args = [repr(x) if is_repr(x) else str(x) for x in self.job_func.args]
        kwargs = ["%s=%s" % (k, repr(v)) for k, v in self.job_func.keywords.items()]
        call_repr = job_func_name + "(" + ", ".join(args + kwargs) + ")"

        if self.at_time is not None:
            return "Every %s %s at %s do %s %s" % (
                self.interval,
                self.unit[:-1] if self.interval == 1 else self.unit,
                self.at_time,
                call_repr,
                timestats,
            )
        else:
            fmt = (
                    "Every %(interval)s "
                    + ("to %(latest)s " if self.latest is not None else "")
                    + "%(unit)s do %(call_repr)s %(timestats)s"
            )

            return fmt % dict(
                interval=self.interval,
                latest=self.latest,
                unit=(self.unit[:-1] if self.interval == 1 else self.unit),
                call_repr=call_repr,
                timestats=timestats,
            )

    @property
    def hours(self):
        self.unit = "hours"
        return self

    @property
    def days(self):
        self.unit = "days"
        return self

    @property
    def weeks(self):
        self.unit = "weeks"
        return self

    @property
    def date(self):
        self.unit = "date"
        return self

    def tag(self, *tags: Hashable):
        """
        Tags the job with one or more unique identifiers.
        Tags must be hashable. Duplicate tags are discarded.
        :param tags: A unique list of ``Hashable`` tags.
        :return: The invoked job instance
        """
        if not all(isinstance(tag, Hashable) for tag in tags):
            raise TypeError("Tags must be hashable")
        self.tags.update(tags)
        return self

    def at(self, time_str):

        """
        Specify a particular time that the job should be run at.
        :param time_str: A string in one of the following formats:
            - For specific date and time -> `YYYY-MM-DD HH:MM:SS`
            - For daily jobs -> `HH:MM:SS` or `HH:MM`
            - For hourly jobs -> `MM:SS` or `:MM`
            - For minute jobs -> `:SS`
            The format must make sense given how often the job is
            repeating; for example, a job that repeats every minute
            should not be given a string in the form `HH:MM:SS`. The
            difference between `:MM` and `:SS` is inferred from the
            selected time-unit (e.g. `every().hour.at(':30')` vs.
            `every().minute.at(':30')`).
        :return: The invoked job instance
        """
        if self.unit not in ("days", "hours", "date"):
            raise ScheduleValueError(
                "Invalid unit (valid units are `days`, `hours`, and `minutes`)"
            )
        if not isinstance(time_str, str):
            raise TypeError("at() should be passed a string")
        if self.unit == "days":
            if not re.match(r"^([0-2]\d:)?[0-5]\d:[0-5]\d$", time_str):
                raise ScheduleValueError(
                    "Invalid time format for a daily job (valid format is HH:MM(:SS)?)"
                )
        if self.unit == "hours":
            if not re.match(r"^([0-5]\d)?:[0-5]\d$", time_str):
                raise ScheduleValueError(
                    "Invalid time format for an hourly job (valid format is (MM)?:SS)"
                )

        if self.unit == "date":
            if re.match(r"^([2-9]\d{3})-(([0][1-9])|([1][0-2]))-(([0][1-9])|([1-2]\d)|([3][0-2])) "
                        r"(([0-1]\d)|([2][0-3])):[0-5]\d:[0-5]\d$", time_str):
                year: Union[str, int]
                month: Union[str, int]
                day: Union[str, int]
                hour: Union[str, int]
                minute: Union[str, int]
                second: Union[str, int]

                date, tm = time_str.split()
                year, month, day = (int(x) for x in date.split("-"))
                hour, minute, second = (int(x) for x in tm.split(":"))

                self.at_time = datetime.datetime(year, month, day, hour, minute, second)
                # ValueError is intended if date is wrong
                return self
            else:
                raise ScheduleValueError(
                    "Invalid datetime format for a job at specific date and time (valid format is YYYY-MM-DD HH:MM:SS)"
                )

        time_values = time_str.split(":")
        hour: Union[str, int]
        minute: Union[str, int]
        second: Union[str, int]
        if len(time_values) == 3:
            hour, minute, second = time_values
        elif len(time_values) == 2 and self.unit == "hours" and len(time_values[0]):
            hour = 0
            minute, second = time_values
        else:
            hour, minute = time_values
            second = 0
        if self.unit == "days":
            hour = int(hour)
            if not (0 <= hour <= 23):
                raise ScheduleValueError(
                    "Invalid number of hours ({} is not between 0 and 23)"
                )
        elif self.unit == "hours":
            hour = 0
        minute = int(minute)
        second = int(second)
        self.at_time = datetime.time(hour, minute, second)
        return self

    def do(self, job_func: Callable, *args, **kwargs):
        """
        Specifies the job_func that should be called every time the
        job runs.
        Any additional arguments are passed on to job_func when
        the job runs.
        :param job_func: The function to be scheduled
        :return: The invoked job instance
        """
        self.job_func = functools.partial(job_func, *args, **kwargs)
        functools.update_wrapper(self.job_func, job_func)
        self._schedule_next_run()
        if self.scheduler is None:
            raise ScheduleError(
                "Unable to a add job to schedule. "
                "Job is not associated with an scheduler"
            )
        self.scheduler.jobs.append(self)
        return self

    @property
    def should_run(self) -> bool:
        """
        :return: ``True`` if the job should be run now.
        """
        assert self.next_run is not None, "must run _schedule_next_run before"
        return datetime.datetime.now() >= self.next_run

    def run(self):
        """
        Run the job and immediately reschedule it.
        If the job's deadline is reached (configured using .until()), the job is not
        run and CancelJob is returned immediately. If the next scheduled run exceeds
        the job's deadline, CancelJob is returned after the execution. In this latter
        case CancelJob takes priority over any other returned value.
        :return: The return value returned by the `job_func`, or CancelJob if the job's
                 deadline is reached.
        """

        logger.debug("Running job %s", self)
        ret = self.job_func()
        self.last_run = datetime.datetime.now()
        if self.unit == "date":
            return CancelJob
        self._schedule_next_run()

        return ret

    def _schedule_next_run(self) -> None:
        """
        Compute the instant when this job should run next.
        """
        if self.unit == "date":
            self.next_run = self.at_time
            return

        if self.unit not in ("hours", "days", "weeks"):
            raise ScheduleValueError(
                "Invalid unit (valid units are `seconds`, `minutes`, `hours`, "
                "`days`, and `weeks`)"
            )

        if self.latest is not None:
            if not (self.latest >= self.interval):
                raise ScheduleError("`latest` is greater than `interval`")
            interval = random.randint(self.interval, self.latest)
        else:
            interval = self.interval

        self.period = datetime.timedelta(**{self.unit: interval})
        self.next_run = datetime.datetime.now() + self.period
        if self.at_time is not None:
            if self.unit not in ("days", "hours"):
                raise ScheduleValueError("Invalid unit without specifying start day")
            kwargs = {"second": self.at_time.second, "microsecond": 0}
            if self.unit == "days":
                kwargs["hour"] = self.at_time.hour
            if self.unit in ["days", "hours"]:
                kwargs["minute"] = self.at_time.minute
            self.next_run = self.next_run.replace(**kwargs)  # type: ignore
            # Make sure we run at the specified time *today* (or *this hour*)
            # as well. This accounts for when a job takes so long it finished
            # in the next period.
            if not self.last_run or (self.next_run - self.last_run) > self.period:
                now = datetime.datetime.now()
                if (
                        self.unit == "days"
                        and self.at_time > now.time()
                        and self.interval == 1
                ):
                    self.next_run = self.next_run - datetime.timedelta(days=1)
                elif self.unit == "hours" and (
                        self.at_time.minute > now.minute
                        or (
                                self.at_time.minute == now.minute
                                and self.at_time.second > now.second
                        )
                ):
                    self.next_run = self.next_run - datetime.timedelta(hours=1)

    def as_dictionary(self) -> dict:
        return {
            "interval": self.interval,
            "unit": self.unit,
            "latest": self.latest,
            "job": {
                "name": self.job_func.func.__name__,
                "args": self.job_func.args,
                "kwargs": self.job_func.keywords
            },
            "at_time": self.at_time.strftime("%Y-%m-%d %H:%M:%S"),
            "last_run": self.last_run.strftime("%Y-%m-%d %H:%M:%S") if self.last_run is not None else None,
            "next_run": self.next_run.strftime("%Y-%m-%d %H:%M:%S"),
            "period": self.period,
            "tags": list(self.tags)
        }

    def from_dictionary(self, job: dict, scheduler: Scheduler):
        self.interval = job["interval"]
        self.unit = job["unit"]
        self.latest = job["latest"]
        self.at(job["at_time"])
        self.last_run = datetime.datetime.strptime(job["last_run"], "%Y-%m-%d %H:%M:%S") if job["last_run"] else None
        self._schedule_next_run()
        self.tag(*job["tags"])
        self.scheduler = scheduler
        # JOB
        self.do(used_functions[job["job"]["name"]], *job["job"]["args"], **job["job"]["kwargs"])
        # referring to functions in this instance, after some program failure e.g. PC was shut down
        # or electricity went out


# The following methods are shortcuts for not having to
# create a Scheduler instance:

#: Default :class:`Scheduler <Scheduler>` object
default_scheduler = Scheduler()

#: Default :class:`Jobs <Job>` list
jobs = default_scheduler.jobs


def every(interval: int = 1) -> Job:
    """Calls :meth:`every <Scheduler.every>` on the
    :data:`default scheduler instance <default_scheduler>`.
    """
    return default_scheduler.every(interval)


def run_pending() -> None:
    """Calls :meth:`run_pending <Scheduler.run_pending>` on the
    :data:`default scheduler instance <default_scheduler>`.
    """
    default_scheduler.run_pending()


def get_jobs(tag: Optional[Hashable] = None) -> List[Job]:
    """Calls :meth:`get_jobs <Scheduler.get_jobs>` on the
    :data:`default scheduler instance <default_scheduler>`.
    """
    return default_scheduler.get_jobs(tag)


def export_jobs(filename: Optional[str] = JOBS_EXPORT_FILE_NAME) -> None:
    """Calls :meth:`export_jobs <Scheduler.export_jobs>` on the
    :data:`default scheduler instance <default_scheduler>`.
    """
    return default_scheduler.export_jobs(filename)


def import_jobs(filename: Optional[str] = JOBS_EXPORT_FILE_NAME) -> None:
    """Calls :meth:`import_jobs <Scheduler.import_jobs>` on the
    :data:`default scheduler instance <default_scheduler>`.
    """
    return default_scheduler.import_jobs(filename)


def clear(tag: Optional[Hashable] = None) -> None:
    """Calls :meth:`clear <Scheduler.clear>` on the
    :data:`default scheduler instance <default_scheduler>`.
    """
    default_scheduler.clear(tag)


def cancel_job(job: Job) -> None:
    """Calls :meth:`cancel_job <Scheduler.cancel_job>` on the
    :data:`default scheduler instance <default_scheduler>`.
    """
    default_scheduler.cancel_job(job)


def next_run() -> Optional[datetime.datetime]:
    """Calls :meth:`next_run <Scheduler.next_run>` on the
    :data:`default scheduler instance <default_scheduler>`.
    """
    return default_scheduler.next_run


def repeat(job, *args, **kwargs):
    """
    Decorator to schedule a new periodic job.
    Any additional arguments are passed on to the decorated function
    when the job runs.
    :param job: a :class:`Jobs <Job>`
    """

    def _schedule_decorator(decorated_function):
        job.do(decorated_function, *args, **kwargs)
        return decorated_function

    return _schedule_decorator


def parse_used_functions(*args: Callable) -> None:
    """
    Stores every function which was or is going to be scheduled.
    The syntax of dict goes from <Scheduler.export_jobs> function and this function does the right opposite
    of what is in export_jobs:
    "job": {
        "name": self.job_func.func.__name__,
        "args": self.job_func.args,
        "kwargs": self.job_func.keywords
    },
    :param args: functions which are going to be scheduled
    """
    global used_functions
    for arg in args:
        used_functions[arg.__name__] = arg


def create_app(queue_to_main: queue.LifoQueue = None, queue_to_scheduler: queue.LifoQueue = None):

    while True:
        time.sleep(1)
