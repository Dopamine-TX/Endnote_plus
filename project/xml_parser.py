import xml.etree.ElementTree as ET
import sys

def parse_exported_xml(xml_filename):
    tree = ET.parse(xml_filename)
    root = tree.getroot()
    
    jnames = []
    for i in root[0]:
        titles = i.find("titles")
        stitle = titles.find("secondary-title")
        if stitle:
            jname = stitle.find("style").text
            jnames.append(jname)

     return jnames
    
