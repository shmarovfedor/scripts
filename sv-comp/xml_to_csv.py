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
import logging


def process_file(filepath):
    logging.info("Processing: %s" % filepath)
    # Getting file extension
    prefix, ext = os.path.splitext(filepath)
    if ext not in [".bz2", ".xml"]:
        logging.error("Unknown file extension \"%s\"" % ext)
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
    process_xml(root)


# This method splits the given XML data according to the structure
# requirements laid out in the header of this file.
def process_xml(root):
    # Working on the "description" node
    description = root.find("description")
    if description is None:
        logging.warning("Could not find the experiments description")
    else:
        logging.debug("Found the following description:\n%s" % description.text)

    # Working on the "columns" node
    columns = root.find("columns")
    if columns is None:
        logging.warning("Could not find the output columns names")
    else:
        columns_df = pd.DataFrame(xml_list_to_dict_list(columns))
        logging.debug("The following columns are used by the BenchExec table generator:\n%s" % columns_df)

    # Working on extra columns
    extra_columns = root.findall("column")
    if len(extra_columns):
        extra_columns_df = pd.DataFrame(xml_list_to_dict_list(extra_columns))
        logging.debug("Found %d extra columns:\n%s" % (len(extra_columns), extra_columns_df))

    # Working on the "systeminfos" node
    systeminfos = root.findall("systeminfo")
    if len(systeminfos):
        systeminfos_df = pd.DataFrame(xml_list_to_dict_list(systeminfos))
        logging.debug("Found descriptions for %d hosts:\n%s" % (len(systeminfos), systeminfos_df))
        # This script is executed without the "-i" option
        if not sys.flags.interactive:
            systeminfos_filepath = filepath + ".systeminfos.csv"
            logging.info("The hosts descriptions will be saved to: %s" % systeminfos_filepath)
            systeminfos_df.to_csv(systeminfos_filepath)
    else:
        logging.warning("No hosts descriptions available")

    # Working on the "runs" node
    runs = root.findall("run")
    if len(runs):
        runs_df = pd.DataFrame(xml_list_to_dict_list(runs))
        logging.debug("Found information about %d runs:\n%s" % (len(runs), runs_df))
        # This script is executed without the "-i" option
        if not sys.flags.interactive:
            runs_filepath = filepath + ".runs.csv"
            logging.info("The information about the runs will be saved to: %s" % runs_filepath)
            runs_df.to_csv(runs_filepath)
    else:
        logging.warning("No BenchExec runs could be found")

    df = pd.merge(runs_df, systeminfos_df, left_on="host", right_on="systeminfo_hostname")
    # This script is executed without the "-i" option
    if not sys.flags.interactive:
        merged_filepath = filepath + ".merged.csv"
        logging.info("The information about the runs will be saved to: %s" % merged_filepath)
        df.to_csv(merged_filepath)


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


def xml_to_dict(node, prefix=''):
    result = {}
    prefix = prefix + node.tag + "_"
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
            result.update(xml_to_dict(child, prefix))

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

logging.basicConfig(level=logging.INFO)
# Just exit if there are no command line options
if len(sys.argv) < 2:
    logging.error("No input files specifyed")
    sys.exit()

# Expecting a list of file paths as command line arguments
for filepath in sys.argv[1:]:
    process_file(filepath)














