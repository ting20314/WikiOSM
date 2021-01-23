import xml.etree.ElementTree as ET
import copy

tree_osc = ET.parse('osm2change.osc')
root_osc = tree_osc.getroot()
output_attr = {"version": "0.3", "generator": root_osc.attrib.get("generator")}
output_root = ET.Element("osmChange", output_attr)
output_tree = ET.ElementTree(output_root)
operation = {}
for opname in [ "create", "modify", "delete" ]:
    operation[opname] = ET.SubElement(output_root, opname, output_attr)


tree_osc.write('osm2change.osc')