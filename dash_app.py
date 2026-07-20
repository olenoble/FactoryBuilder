import dash
from dash import html, dcc
import plotly.graph_objects as go
import plotly as plt
import networkx as nx
from factory.factory import Factory
import math

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

# Position nodes using spring layout
pos = nx.spring_layout(graph)

# Create Plotly figure
fig = go.Figure()


# Add edges as annotations with arrows, adjusted for size and edge positioning
offset = 0.05  # Approximate half-node offset in data units; adjust as needed for your layout
for edge in graph.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    dx = x1 - x0
    dy = y1 - y0
    dist = math.sqrt(dx ** 2 + dy ** 2)
    if dist > 0:
        # Position tail on source edge
        ax = x0 + (dx / dist) * offset
        ay = y0 + (dy / dist) * offset
        # Position head on target edge
        x = x1 - (dx / dist) * offset
        y = y1 - (dy / dist) * offset
        fig.add_annotation(x=x,
                           y=y,
                           ax=ax,
                           ay=ay,
                           xref="x",
                           yref="y",
                           axref="x",
                           ayref="y",
                           showarrow=True,
                           # clicktoshow=True,
                           arrowhead=2,
                           arrowsize=1,
                           arrowwidth=1,
                           arrowcolor='blue')

# Add nodes as square markers with text
node_x = [pos[node][0] for node in graph.nodes()]
node_y = [pos[node][1] for node in graph.nodes()]
node_text = [graph.nodes[node]['label'] for node in graph.nodes()]
fig.add_trace(go.Scatter(x=node_x,
                         y=node_y,
                         mode='markers+text',
                         text=node_text,
                         textposition="middle center",
                         marker=dict(size=50,
                                     symbol='square',
                                     color='lightblue',
                                     line=dict(width=2, color='black'))))

# Update layout
fig.update_layout(showlegend=False,
                  xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                  yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                  title="Workflow Flowchart")


# Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Workflow Flowchart"),
    dcc.Graph(figure=fig)
])

if __name__ == '__main__':
    app.run(debug=True)
