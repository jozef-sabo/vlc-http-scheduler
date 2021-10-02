"""
This code is from Kier von Konigslow's pull request for dicttoxml library [1]. Shadow names were fixed.
Unfixable errors in library code were fixed on own hook.
[1] https://github.com/quandyfactory/dicttoxml/pull/74
"""

from xml.etree import ElementTree


def cast_from_attribute(text, attr):
    """Converts XML text into a Python data format based on the tag attribute"""
    if attr["type"] == "str":
        if not text:
            return ""
        return str(text)
    elif attr["type"] == "int":
        return int(text)
    elif attr["type"] == "float":
        return float(text)
    elif attr["type"] == "bool":
        if str(text).lower() == "true":
            return True
        elif str(text).lower() == "false":
            return False
        else:
            raise ValueError("bool attribute expected 'true' or 'false'")
    elif attr["type"] == "list":
        return []
    elif attr["type"] == "dict":
        return {}
    elif attr["type"].lower() == "null":
        return None
    else:
        raise TypeError("unsupported type: only 'str', 'int', 'float', 'bool', 'list', 'dict', and 'None' supported")


def xmltodict(obj, ignore_root: bool = True):
    """Converts an XML string into a Python object based on each tag's attribute"""
    def add_to_output(out_object, tree_child):
        if "type" not in tree_child.attrib:
            raise ValueError("XML must contain type attributes for each tag")
        if isinstance(out_object, dict):
            out_object.update({tree_child.tag: cast_from_attribute(tree_child.text, tree_child.attrib)})
            for sub in tree_child:
                add_to_output(out_object[tree_child.tag], sub)
        elif isinstance(out_object, list):
            out_object.append(cast_from_attribute(tree_child.text, tree_child.attrib))
            for sub in tree_child:
                add_to_output(out_object[-1], sub)
    root = ElementTree.fromstring(obj)
    output = {}
    for child in root:
        add_to_output(output, child)
    if ignore_root:
        return output
    return {root.tag: output}
