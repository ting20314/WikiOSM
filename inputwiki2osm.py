import csv
import shutil
import xml.etree.ElementTree as ET
import copy

def inputwiki2osm_osc(download_place):
    with open('compare.csv', newline='', encoding='utf-8') as csvfile:
        reader_Ds  = csv.reader(csvfile) #將內容全轉成字典
        osm_origion = list(reader_Ds)  #將A表存進矩陣
    shutil.copyfile(download_place+"\\export.osm",'osm2change.osm')
    # osm
    tree = ET.parse('osm2change.osm')
    root = tree.getroot()
    # osc
    output_attr = {"version": "0.3", "generator": root.attrib.get("generator")}
    output_root = ET.Element("osmChange", output_attr)
    output_tree = ET.ElementTree(output_root)

    operation = {}
    for opname in [ "create", "modify", "delete" ]:
        operation[opname] = ET.SubElement(output_root,opname, output_attr)
    root_osc = output_tree.getroot()

    for child in root.iter('relation'):
        for i in range(1,len(osm_origion)):
            if child.attrib.get('id')==osm_origion[i][1]:
                cchild = ET.SubElement(child, 'tag')
                cchild.set('k', "wikidatalll")
                cchild.set('v',osm_origion[i][0])
        co = copy.deepcopy(child)  # copy <c> node
        root_osc[1].append(co)  # insert the new node

    tree.write('osm2change.osm')
    output_tree.write('osm2change.osc')
