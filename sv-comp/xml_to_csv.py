#!/usr/bin/env python3

# This script parses a given results XML file produced by BenchExec,
# Here the following file layout is expected:
#
#   result - this the root of the XML tree
#   |
#   |- description  - textual description of the current experiment
#   |- columns      - list of columns that are present in the TXT output
#   |- systeminfo   - description of each available machine
#   |   |
#   |   |- os           - operating system information
#   |   |- cpu          - CPU description
#   |   |- ram          - amount of available RAM
#   |   |- environment  - just an empty node
#   |  ...
#   |- run          - actual execution statistics for each task
#   |  ...
#   |- column       - additional info columns (seems to be overall walltime atm)


import sys
import os
import xml.etree.ElementTree as ET
import pandas as pd
import bz2


def string_list_to_list(string_list):
    return string_list.strip('][').split(', ')


# This method converts a special case node with a tag "column" into dictionary.
# The following structure is assumed. Attributes "title" and "value" must
# be present, and all other attributes are ignored.
#
#   <column title="title_text" value="value_text"/>
#
# @param column - an XML mode with the structure assumed above
# @return - empty dictionary if the "title" attribute is missing
#           a dictionary {"title_text" : None"} if "title" is present 
#           while the "value" is missing,
#           and a dictionary {"title_text" : "value_text"} otherwise.
def column_node_to_dict(column):
    result = {}
    if column is None:
        return result

    if not isinstance(column, ET.Element):
        return result

    if column.tag != "column":
        return result
    
    if not ("title" in column.keys()):
        return result

    if not ("value" in column.keys()):
        result[column.attrib["title"]] = None
        return result

    # Safe to access both attributes now
    result[column.attrib["title"]] = column.attrib["value"]
    return result

def xml_to_dict(node):
    result = {}
    prefix = node.tag + "_"
    for attrib_key, attrib_value in node.items():
        key = prefix + attrib_key
        attrib_list = string_list_to_list(attrib_value)
        if len(attrib_list) > 1:
            i = 0
            for attrib in attrib_list:
                result[key + "_" + str(i)] = attrib
                i += 1
        else:
            value = attrib_list[0]
            result[key] = value
            

    for child in node:
        if child.tag == "column":
            result.update(column_node_to_dict(child))
        else:
            result.update(xml_to_dict(child))

    return result


def xml_list_to_dict_list(nodes):
    result_dict_list = []
    if len(nodes) < 1:
        return result_dict_list

    for node in nodes:
        result_dict_list.append(xml_to_dict(node))

    return result_dict_list


##
#
# The "main" workflow begins here
#
##

# Just exit if there are no command line options
if len(sys.argv) < 2:
    sys.exit()

# The first argument is the file path, and everything else is ignored for now
filepath = sys.argv[1]
print("Working on the file at:", filepath)

# Getting file extension
prefix, ext = os.path.splitext(filepath)
if ext not in [".bz2", ".xml"]:
    print("*** ERROR: unknown file extension \"%s\"" % ext)
    sys.exit()

# This is an XML file
if ext == ".xml":
    f = open(filepath, "rb")

# This is a BZ2 file
if ext == ".bz2":
    f = bz2.open(filepath, "rb")

# Reading the XML data and parsing it
xml_data = f.read()
root = ET.XML(xml_data)

# Working on the "description" node
description = root.find("description")
if description is None:
    print("*** WARNING: could not find the experiments description", file=sys.stderr)
else:
    print("Description:")
    print("----------")
    print(description.text)
    print("----------")

# Working on the "columns" node
columns = root.find("columns")
if columns is None:
    print("*** WARNING: could not find the output columns names", file=sys.stderr)
else:
    print("The following columns are used by the BenchExec table generator:")
    columns_df = pd.DataFrame(xml_list_to_dict_list(columns))
    print(columns_df)

# Working on extra columns
extra_columns = root.findall("column")
if len(extra_columns):
    print("Found %d extra columns:" % (len(extra_columns)))
    extra_columns_df = pd.DataFrame(xml_list_to_dict_list(extra_columns))
    print(extra_columns_df)

# Working on the "systeminfos" node
systeminfos = root.findall("systeminfo")
if len(systeminfos):
    print("Found descriptions for %d hosts:" % (len(systeminfos)))
    systeminfos_df = pd.DataFrame(xml_list_to_dict_list(systeminfos))
    print(systeminfos_df)
    systeminfos_filepath = filepath + ".systeminfos.csv"
    # This script is executed without the "-i" option
    if not sys.flags.interactive:
        print("The hosts descriptions will be saved to:", systeminfos_filepath)
        systeminfos_df.to_csv(systeminfos_filepath)
else:
    print("*** WARNING: no hosts descriptions available", file=sys.stderr)

# Working on the "runs" node
runs = root.findall("run")
if len(runs):
    print("Found information about %d runs" % (len(runs)))
    runs_df = pd.DataFrame(xml_list_to_dict_list(runs))
    print(runs_df)
    runs_filepath = filepath + ".runs.csv"
    # This script is executed without the "-i" option
    if not sys.flags.interactive:
        print("The information about the runs will be saved to:", runs_filepath)
        runs_df.to_csv(runs_filepath)
else:
    print("*** WARNING: no BenchExec runs could be found", file=sys.stderr)













