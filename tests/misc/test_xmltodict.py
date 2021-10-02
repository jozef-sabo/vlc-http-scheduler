"""
This code is from Kier von Konigslow's pull request for dicttoxml library [1]. PEP 8 rules were fulfilled.
[1] https://github.com/quandyfactory/dicttoxml/pull/74
"""

import unittest
import dicttoxml
import app.modules.misc.xmltodict as xmltodict


class Tests(unittest.TestCase):
    def test_xmltodict(self):
        inp = {
            'string': "This is a string with special characters",
            'empty_string': '',
            'int': 1002,
            'float': 12.56,
            'other_float': float(80),
            'boolean': False,
            'none_type': None,
            'list': [99, 'sheep', 'dog'],
            'empty_list': [],
            'list_of_dicts': [{}, {'hi_there': 7, 'owl': 'exterminator'}, {'foo': 56.2, 'ok': True}],
            'dict_of_lists': {'list1': [3, 6, 'dog', 'cat', False], 'empty_list': []},
            'nested_lists': [[4, 5, 6, 7], [1, 2, 3, 4, [5, 6, 7, 8]]]
        }
        xml = dicttoxml.dicttoxml(inp)
        output = xmltodict.xmltodict(xml)
        self.assertEqual({'root': inp}, output)


if __name__ == "__main__":
    unittest.main()
