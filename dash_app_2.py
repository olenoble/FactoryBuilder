import dash
from dash import html, dcc
import dash_cytoscape as cyto
# import plotly.graph_objects as go
# import plotly as plt
import networkx as nx
from factory.factory import Factory

# import math

workflow2 = {'function_name': 'power',
             'kwargs': {'x': {'function_name': 'subtract',
                              'kwargs': {'x': 7,
                                         'y': {'function_name': 'multiply',
                                               'kwargs': {'x': 2,
                                                          'y': 2
                                                          }
                                               }
                                         }
                              },
                        'y': {'function_name': 'exponential',
                              'kwargs': {'x': 1,
                                         }
                              }

                        }
             }

workflow1 = {'function_name': 'logarithm',
             'kwargs': {'x': {'function_name': 'divide',
                              'kwargs': {'x': 7,
                                         'y': 8
                                         }
                              },

                        }
             }

workflow = {'function_name': 'add',
            'kwargs': {'x': workflow1,
                       'y': workflow2
                       },
            }


# Function to parse workflow into a networkx graph
def parse_workflow(wf, grph, parent=None, level=0):
    func_name = wf['function_name']
    node_id = f"{func_name}_{level}"
    grph.add_node(node_id, label=func_name, level=level)
    if parent:
        grph.add_edge(parent, node_id)
    if 'kwargs' in wf:
        for key, value in wf['kwargs'].items():
            if isinstance(value, dict) and 'function_name' in value:
                parse_workflow(value, grph, node_id, level + 1)


# Initialize Factory and get workflow (assuming it's defined similarly)
f = Factory()
graph = nx.DiGraph()
parse_workflow(workflow, graph)

# Convert to cytoscape elements
elements = []
for node in graph.nodes():
    elements.append({'data': {'id': node,
                              'label': graph.nodes[node]['label']
                              }
                     })

for edge in graph.edges():
    elements.append({'data': {'source': edge[1],
                              'target': edge[0]
                              },
                     'width': 100,
                     'height': 500
                     })

# Dash app - workflow must be in a separate tab from the function list, and the function list should be organized according to the folder structure of the factory
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1("Workflow Flowchart"),
    cyto.Cytoscape(
        id='cytoscape',
        elements=elements,
        layout={'name': 'breadthfirst'},  # Or 'cose' for force-directed
        style={'width': '100%', 'height': '600px'},
        stylesheet=[{'selector': 'node',
                     'style': {'content': 'data(label)',
                               'text-valign': 'center',
                               'text-halign': 'center',
                               'background-color': 'lightblue',
                               'shape': 'rectangle'
                               }
                     },
                    {'selector': 'edge',
                     'style': {'curve-style': 'bezier',
                               'target-arrow-shape': 'triangle',
                               'line-color': 'blue'}
                     }
                    ]
    )
])

# add all available factory functions as a list on the left of the graph (organized according the folder structure of the factory)
# each function is shown in a box and can be dragged and dropped on the graph to replace a node with that function
app.layout.children.append(html.Div([
    html.H2("Available Functions"),
    html.Ul([html.Li(func) for func in f.all_functions.keys()])
], style={'position': 'absolute', 'left': '10px', 'top': '100px'}))





# add callback to replace node with another function when right-clicked
@app.callback(
    dash.dependencies.Output('cytoscape', 'elements'),
    [dash.dependencies.Input('cytoscape', 'tapNodeData')]
)
def replace_node(data):
    if data:
        node_id = data['id']
        # Here you can implement logic to replace the node with another function
        # For example, you could update the graph and re-parse it to get new elements
        # For simplicity, we'll just print the node id for now
        print(f"Node {node_id} was right-clicked")
    return elements


if __name__ == '__main__':
    app.run(debug=False)
