import xml.etree.ElementTree as ET
import json

root = ET.parse('events.xml')
historical_figures_root = root.find('historical_figures')

nodes = []
edges = []

for hf in historical_figures_root.findall('historical_figure'):
    hf_id = int(hf.find('id').text)
    name = hf.find('name').text
    nodes.append({"id": hf_id, "label": name})

    for link in hf.findall('hf_link'):
        link_type = link.find('link_type').text
        hfid = int(link.find('hfid').text)
        edges.append({"from": hf_id, "to": hfid, "label": link_type})

graph = {"nodes": nodes, "edges": edges}

with open('historical_figures_graph.json', 'w') as json_file:
    json.dump(graph, json_file, indent=2)

