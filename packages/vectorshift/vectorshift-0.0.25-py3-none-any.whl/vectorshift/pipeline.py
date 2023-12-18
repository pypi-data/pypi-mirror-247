# functionality to stitch together nodes into pipelines
from collections import defaultdict
import json
import requests
from networkx import MultiDiGraph, topological_generations

import vectorshift
from vectorshift.node import *
from vectorshift.consts import *

# Helpers for converting to/from JSON
# Assign a width and height to a node. Crude approximation for now.
def assign_node_size(node:NodeTemplate) -> tuple[int, int]:
    if type(node) in [InputNode, FileNode, OutputNode, GitLoaderNode, SerpAPILoaderNode]:
        return 250, 155
    elif type(node) in [URLLoaderNode, FileLoaderNode, WikipediaLoaderNode, ArXivLoaderNode, ChatMemoryNode]:
        return 200, 100
    elif type(node) in [PipelineNode, TransformationNode, NotionLoaderNode, OpenAILLMNode, VectorDBLoaderNode, VectorDBReaderNode, LogicMergeNode, 
    SplitTextNode]:
        return 275, 175
    elif type(node) in [IntegrationNode]:
        return 300, 175
    else:
        # the more inputs/outputs the node has, the taller it should be
        return 300, 45 + max(len(node._inputs), len(node.outputs())) * 65

# Figure out what node class a JSON represents, and convert it into an object
# of that class using the class's from_json_rep method.
node_type_to_node_class:dict[str, NodeTemplate] = {
    'customInput': InputNode,
    'customOutput': OutputNode,
    'text': TextNode,
    'file': FileNode,
    'pipeline': PipelineNode,
    'integration': IntegrationNode,
    'transformation': TransformationNode,
    'fileSave': FileSaveNode,
    'llmOpenAI': OpenAILLMNode,
    'llmAnthropic': AnthropicLLMNode,
    'imageGen': ImageGenNode,
    'speechToText': SpeechToTextNode,
    'vectorDBLoader': VectorDBLoaderNode,
    'vectorDBReader': VectorDBReaderNode,
    'vectorStore': VectorStoreNode,
    'condition': LogicConditionNode,
    'merge': LogicMergeNode,
    'splitText': SplitTextNode,
    'chatMemory': ChatMemoryNode,
    'agent': AgentNode,
}

dataloader_node_type_to_node_class:dict[str, NodeTemplate] = {
    'File': FileLoaderNode,
    'CSV Query': CSVQueryLoaderNode,
    'URL': URLLoaderNode,
    'Wikipedia': WikipediaLoaderNode,
    'YouTube': YouTubeLoaderNode,
    'Arxiv': ArXivLoaderNode,
    'SerpAPI': SerpAPILoaderNode,
    'Git': GitLoaderNode,
    'Notion': NotionLoaderNode,
    'Confluence': ConfluenceLoaderNode
}

def node_from_json_data(node_json_data) -> NodeTemplate:
    if node_json_data['type'] in node_type_to_node_class:
        return node_type_to_node_class[node_json_data['type']].from_json_rep(node_json_data)
    elif node_json_data['type'] in dataloader_node_type_to_node_class:
        if node_json_data['data']['loaderType'] in dataloader_node_type_to_node_class:
            return dataloader_node_type_to_node_class[node_json_data['data']['loaderType']].from_json_rep(node_json_data)
        raise ValueError(f"Unrecognized type for data loader node {node_json_data['data']['loaderType']}.")
    raise ValueError(f"Unrecognized node type {node_json_data['type']}.")

# Assign a position (x,y) to a node. Right now this function is 
# rudimentary, arranging all nodes in a straight line.
def top_sort_nodes(node_ids:list[str], edges:list[dict]) -> list:
    edges = [(edge['source'], edge['target'], {
        'sourceHandle': edge['sourceHandle'].replace(f"{edge['source']}-", '', 1),
        'targetHandle': edge['targetHandle'].replace(f"{edge['target']}-", '', 1)
    }) for edge in edges]
    G = MultiDiGraph()
    G.add_nodes_from(node_ids)
    G.add_edges_from(edges)
    # Sort the nodes into topological generations
    return topological_generations(G)

def assign_node_positions(node_ids:list[str], edges:list[dict]) -> dict[str, dict[str, int]]:
    # Generate a graph with just the relevant data from the nodes and edges
    top_gen = top_sort_nodes(node_ids, edges)

    # Assign positions to each node, aligning the nodes within each generation 
    # vertically and centered about the x-axis
    positions = {}
    for i, generation in enumerate(top_gen):
        for j, node_id in enumerate(generation):
            positions[node_id] = {
                'x': i * 400, 
                'y': (j - len(generation) // 2) * 250}

    return positions

# Create a pipeline by passing nodes and params in.
class Pipeline():
    def __init__(self, name:str, description:str, nodes:list[NodeTemplate], id:str = None):
        self.id = id
        self.name = name 
        self.description = description 
        # Map node IDs to the objects
        self.nodes:dict[str, NodeTemplate] = {}
        # Assign node IDs and gather ID (node type) counts; also record the 
        # inputs and outputs
        # NB: in a node's JSON representation, id, type, data.id, and 
        # data.nodeType are essentially the same
        self.node_type_counts = defaultdict(int)
        # The OVERALL pipeline input and output nodes, keyed by node IDs 
        # (analogous to Mongo)
        self.inputs, self.outputs = {}, {}
        # assign each node an ID and increment self.node_type_counts - before 
        # adding edges, all nodes must have IDs first
        for node in nodes:
            self._add_node(node)
        
        # Create edges: An edge is a dict following the JSON structure. All 
        # edges in the computation graph defined by the nodes terminate at some
        # node, i.e. are in the node's _inputs. So it should suffice to parse
        # through every node's _inputs and create an edge for each one. 
        self.edges:list[dict[str, str]] = []
        for n in self.nodes.values():
            # n.inputs() is a dictionary of input field names to NodeOutputs 
            # from ancestor nodes filling those fields
            target_node_id = n._id
            for input_name, outputs in n._inputs.items():
                if outputs == []:
                    print(f'WARNING: {type(n)} node did not receive any inputs for input field {input_name}')
                # an input could have aggregated several NodeOutputs
                for output in outputs:
                    # Edges are specifically defined by source/target handles, 
                    # derived from the node ids
                    source_node_id = output.source._id
                    output_field = output.output_field
                    source_handle = f'{source_node_id}-{output_field}'
                    target_handle = f'{target_node_id}-{input_name}'
                    # Create an edge id following ReactFlow's formatting
                    id = f'reactflow__edge-{source_node_id}{source_handle}-{target_node_id}{target_handle}'
                    self.edges.append({
                        'source': source_node_id,
                        'sourceHandle': source_handle,
                        'target': target_node_id,
                        'targetHandle': target_handle,
                        'id': id
                    })
    
    def __repr__(self):
        return f'<Pipeline with JSON representation\n\
            {json.dumps(self.to_json_rep())}\n>'
    
    def __str__(self):
        nodes_strs = ['\t' + n.__str__().replace('\n', '\n\t') 
                      for n in self.nodes.values()]
        nodes_str = ',\n'.join(nodes_strs)
        id_str = f"'{self.id}'" if self.id is not None \
            else '(no assigned pipeline id)'
        return f"(pipeline id {self.id})=Pipeline(\n\
    name='{self.name}',\n\
    description='{self.description}',\n\
    nodes=[\n{nodes_str}\n\t],\n\
    id={id_str}\n\
)"
    
    # Analogous to __str__, but prints the output in a way that aims to
    # be copy-pastable Python code. Nodes are initialized in a top-sorted
    # order before being inserted into the Pipeline constructor.
    def print_construction(self):
        construct_node_strs = []
        construct_node_ids = []
        top_gen = top_sort_nodes(list(self.nodes.keys()), self.edges)
        for generation in top_gen:
            for node_id in generation:
                construct_node_strs.append(
                    self.nodes[node_id].construction_str()
                )
                construct_node_ids.append(
                    node_id.replace('-', '_')
                )
        id_str = f"'{self.id}'" if self.id is not None \
            else '(no assigned pipeline id)'
        pipeline_construct_str = f"{id_str.replace('-', '_')}=Pipeline(\n\
    name='{self.name}',\n\
    description='{self.description}',\n\
    nodes=[\n{', '.join(construct_node_ids)}\n\t],\n\
    id={id_str}\n\
)"
        return '\n'.join(construct_node_strs) + '\n' + pipeline_construct_str

    # Convert a Pipeline into a JSON string.  
    def to_json_rep(self) -> dict:
        nodes = list(self.nodes.values())
        node_sizes = [assign_node_size(n) for n in nodes]
        node_positions = assign_node_positions(
            list(self.nodes.keys()), 
            self.edges
        )
        node_jsons = []
        for i, node in enumerate(nodes):
            # we currently fix the position and absolute position to be the same
            node_display_params = {
                'position': node_positions[node._id],
                'positionAbsolute': node_positions[node._id],
                'width': node_sizes[i][0],
                'height': node_sizes[i][1],
                'selected': False,
                'dragging': False
            }
            node_json = nodes[i].to_json_rep()
            node_jsons.append({**node_json, **node_display_params})
        # these edge display params are also fixed for now
        # TODO: might not need these anymore
        edge_display_params = {
            'type': 'defaultEdge',
            'animated': True,
            'markerEnd': {
                'type': 'arrow',
                'height': '20px',
                'width': '20px'
            }
        }
        edge_jsons = [{**e, **edge_display_params} for e in self.edges]
        pipeline_obj = {
            # The overall (top-level) _id field for the JSON is gen'd by Mongo.
            'name': self.name,
            'description': self.description,
            'nodes': node_jsons,
            'edges': edge_jsons,
            'inputs': self.inputs,
            'outputs': self.outputs,
            'nodeIDs': dict(self.node_type_counts),
            # TODO: should this always be false?
            'zipOutputs': False,
        }
        if self.id:
            pipeline_obj['id'] = self.id
        return pipeline_obj
    
    def to_json(self) -> str:
        return json.dumps(self.to_json_rep(), indent=4)
    
    @staticmethod 
    def from_json_rep(json_data:dict[str, any]) -> 'Pipeline':
        # build all nodes first 
        node_ids_to_nodes:dict[str, NodeTemplate] = {}
        for node_json_data in json_data['nodes']:
            n = node_from_json_data(node_json_data)
            node_ids_to_nodes[node_json_data['id']] = n
        # add edges
        for edge in json_data['edges']:
            # find the specific source and target edges
            source_id, target_id = edge['source'], edge['target']
            source_output_field = edge['sourceHandle'].replace(f'{source_id}-', '', 1)
            target_input_name = edge['targetHandle'].replace(f'{target_id}-', '', 1)
            source_node = node_ids_to_nodes[source_id]
            target_node = node_ids_to_nodes[target_id]
            # make sure the input/output fields as stored in the edge exist
            if target_input_name not in target_node._inputs.keys():
                raise ValueError(f'Edge destination input field {target_input_name} not found.')
            source_node_outputs = source_node.outputs()
            if source_output_field not in source_node_outputs.keys():
                raise ValueError(f'Edge source output field not {source_output_field} not found.')
            # link up the source's NodeOutput to the target's _inputs
            target_node._inputs[target_input_name].append(source_node_outputs[source_output_field])
        
        # TODO: save additional metadata like createdDate, userID, cost, etc., 
        # as well as node-specific data like their positions...
        # this necessitates making new member vars in the Pipeline class.
        # Note: Make sure Mongo's ObjectId has been cast to a string already.
        pipeline_id = json_data.get('id')
        return Pipeline(
            name=json_data['name'],
            description=json_data['description'],
            nodes=list(node_ids_to_nodes.values()),
            id=pipeline_id
        )
    
    @staticmethod 
    def from_json(json_str:str) -> 'Pipeline':
        json_data = json.loads(json_str)
        return Pipeline.from_json_rep(json_data)
    
    @staticmethod
    def fetch(
        pipeline_name:str = None,
        pipeline_id:str = None,
        username:str = None,
        org_name:str = None,
        public_key:str = None,
        private_key:str = None
    ) -> 'Pipeline':
        if pipeline_id is None and pipeline_name is None:
            raise ValueError('Must specify either pipeline_id or pipeline_name.')
        if pipeline_name is not None and username is None and org_name is not None:
            raise ValueError('Must specify username if org_name is specified.')
        response = requests.get(
            API_PIPELINE_FETCH_ENDPOINT,
            data={
                'pipeline_id': pipeline_id,
                'pipeline_name': pipeline_name,
                'username': username,
                'org_name': org_name,
            },
            headers={
                'Public-Key': public_key or vectorshift.public_key,
                'Private-Key': private_key or vectorshift.private_key,
            }
        )
        if response.status_code != 200:
            raise Exception(response.text)
        response = response.json()
        return Pipeline.from_json_rep(response)
    
    def get_nodes(self) -> dict[str, NodeTemplate]: return self.nodes

    # Helper function to add a node and assign it an ID; does not add the
    # input edges to the node
    def _add_node(self, node:NodeTemplate):
        # assign a fresh new ID to the node
        t = node.node_type 
        type_counter = self.node_type_counts[t] + 1
        node_id = f'{t}-{type_counter}'
        node._id = node_id 
        self.node_type_counts[t] = type_counter
        if type(node) == InputNode:
            self.inputs[node_id] = {'name': node.name, 'type': node.input_type.capitalize()}
        elif type(node) == OutputNode:
            self.outputs[node_id] = {'name': node.name, 'type': node.output_type.capitalize()}
        self.nodes[node_id] = node
    
    def add_node(self, node:NodeTemplate):
        # logic for adding node and input edges is analogous to __init__
        self._add_node(node)
        # add edges for the node's inputs
        for input_name, outputs in node._inputs.items():
            if outputs == []:
                print(f'WARNING: {type(node)} node did not receive any inputs for input field {input_name}')
            # an input could have aggregated several NodeOutputs
            for output in outputs:
                # Edges are specifically defined by source/target handles, 
                # derived from the node ids
                source_node_id = output.source._id
                output_field = output.output_field
                source_handle = f'{source_node_id}-{output_field}'
                target_handle = f'{node._id}-{input_name}'
                # Create an edge id following ReactFlow's formatting
                id = f'reactflow__edge-{source_node_id}{source_handle}-{node._id}{target_handle}'
                self.edges.append({
                    'source': source_node_id,
                    'sourceHandle': source_handle,
                    'target': node._id,
                    'targetHandle': target_handle,
                    'id': id
                })

    # Replace one node with another. Nodes should be of the same exact type. 
    # Any inputs and outputs to the replaced node are kept as inputs and 
    # outputs of the new node.
    # If the replacement node is of a different type, users should provide 
    # input and output maps from old I/O names to new I/O names.
    def replace_node(self, node_id:str, replacement_node:NodeTemplate, 
                     input_map:dict[str, str]=None, 
                     output_map:dict[str, str]=None):
        if node_id not in self.nodes.keys(): 
            raise ValueError(f'Node id {node_id} not found.')
        existing_node = self.nodes[node_id]
        if not (type(existing_node) == type(replacement_node)):
            print(f'WARNING: Replacement node type ({type(replacement_node)}) does not equal the type of the existing node ({type(existing_node)}), which may cause functionality issues.')
        # if an input_map is given, the map keys should be a subset of the 
        # existing node's _inputs keys
        if input_map:
            if not set(input_map.keys()).issubset(set(existing_node._inputs.keys())):
                raise ValueError('Input map\'s keys do not constitute a subset of the existing node\'s input names.')
            mapped_inputs = {}
            for name, mapped_name in input_map.items():
                mapped_inputs[mapped_name] = existing_node._inputs[name]
            replacement_node._inputs = mapped_inputs 
        else:
            replacement_node._inputs = existing_node._inputs 
        # the out-edge IDs stay mostly the same as the replacement node takes 
        # the existing node's ID; if the output field names are changed (e.g. 
        # via an output_map), then we can modify the edges' handle attribute
        if output_map:
            for e in self.edges:
                if e['source'] == node_id:
                    old_output_field = e['sourceHandle'].split('-')[-1]
                    if old_output_field not in output_map.keys():
                        raise ValueError(f'Output map does not contain existing node\'s output {old_output_field}.')
                    e['sourceHandle'] = f'{node_id}-{output_map[old_output_field]}'
        replacement_node._id = node_id
        self.nodes[node_id] = replacement_node 

    def delete_node(self, node_id:str):
        if node_id not in self.nodes.keys(): 
            raise ValueError(f'PipelineNode: node id {node_id} not found.')
        del self.nodes[node_id]
        updated_edges = []
        # delete all the out-edges of the node
        for e in self.edges:
            if e['source'] == node_id:
                print(f"WARNING: Removing edge from deleted node {node_id} to node {e['target']}")
                # assume that output field names don't contain hyphens
                target_node_input_name = e['targetHandle'].split('-')[-1]
                target_node = self.nodes[e['target']]
                target_node._inputs[target_node_input_name] = None
            else:
                updated_edges.append(e)
        self.edges = updated_edges
    
    def save(self, public_key:str = None, private_key:str = None, 
             update_existing:bool = False) -> dict:
        if update_existing and not self.id:
            raise ValueError('Error updating: Pipeline object does not have an existing ID. It must be saved as a new pipeline.')
        # if update_existing is false, save as a new pipeline
        if not update_existing:
            self.id = None 
        
        # API_PIPELINE_SAVE_ENDPOINT handles saving and updating pipelines 
        # depending on whether or not the JSON has an id (logic in api repo)
        response = requests.post(
            API_PIPELINE_SAVE_ENDPOINT,
            data=({'pipeline': self.to_json()}),
            headers={
                'Public-Key': public_key or vectorshift.public_key,
                'Private-Key': private_key or vectorshift.private_key,
            }
        )

        if response.status_code != 200:
            raise Exception(response.text)
        response = response.json()
        self.id = response.get('id')
        return response

    def update(self, public_key:str = None, private_key:str = None):
        self.save(public_key, private_key, update_existing=True)
    
    def run(self, inputs={}, public_key:str = None, private_key:str = None) -> dict:
        if not self.id:
            raise ValueError('Pipeline must be saved before it can be run.')
        response = requests.post(
            API_PIPELINE_RUN_ENDPOINT,
            data=({
                'pipeline_id': self.id,
                'inputs': json.dumps(inputs),
            }),
            headers={
                'Public-Key': public_key or vectorshift.public_key,
                'Private-Key': private_key or vectorshift.private_key,
            }
        )
        if response.status_code != 200:
            raise Exception(response.text)
        response = response.json()
        return response
