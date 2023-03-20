import xml.etree.ElementTree as ET
import json

# Create an empty list for nodes and edges
nodes = []
edges = []

# Parse the XML file
tree = ET.parse('historical_events.xml')
root = tree.getroot()

# Parse identities
idens = root.find('identities')
identities = {}
for identity in idens.iter('identity'):
    try:
        id_ = int(identity.find('id').text)
        name = identity.find('name').text
        identities[id_] = name
    except:
        ...

# Add nodes
for id_, name in identities.items():
    nodes.append({"id": id_, "label": name})
    

# Find the historical_event_relationships element in the XML
relships = root.find('historical_event_relationships')

# Loop through each historical_event_relationship element inside the historical_event_relationships element
for event in relships.iter('historical_event_relationship'):
    source_hf = int(event.find('source_hf').text)
    target_hf = int(event.find('target_hf').text)
    event_id = int(event.find('event').text)

    # Check if source_hf and target_hf nodes already exist
    source_exists = any(node['id'] == source_hf for node in nodes)
    target_exists = any(node['id'] == target_hf for node in nodes)

    # Add source_hf node if it doesn't exist
    if not source_exists:
        nodes.append({"id": source_hf, "label": str(source_hf)})

    # Add target_hf node if it doesn't exist
    if not target_exists:
        nodes.append({"id": target_hf, "label": str(target_hf)})

    # Add edge for the relationship
    edges.append({"from": source_hf, "to": target_hf})

# Create a dictionary for the nodes and edges
graph = {"nodes": nodes, "edges": edges}

# Write the graph to a JSON file
with open('historical_events.json', 'w') as f:
    json.dump(graph, f)

