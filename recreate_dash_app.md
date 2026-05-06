# Recreating the Interactive Workflow Flowchart Dash App

This document provides a step-by-step guide to recreate the interactive Dash application that visualizes a workflow as a flowchart using Cytoscape for interactivity. The app includes tabs for the workflow and function list, with the function list organized by folder structure, and supports node replacement via right-click (with placeholders for drag-and-drop functionality).

## Prerequisites

- Python 3.x installed.
- Install required packages:
  ```
  pip install dash dash-cytoscape networkx
  ```
- Ensure the `factory.factory` module is available in your project, containing the `Factory` class with an `all_functions` attribute that includes functions organized by folders (e.g., a dict with folder names as keys and lists of functions as values).

## Step 1: Set Up the Project Structure

Create a new Python file named `dash_app_2.py` in your project directory.

## Step 2: Import Necessary Libraries

Import the required libraries at the top of `dash_app_2.py`:

```python
import dash
from dash import html, dcc
import dash_cytoscape as cyto
import networkx as nx
from factory.factory import Factory
```

## Step 3: Define the Workflow Data

Define the nested workflow dictionaries (`workflow1`, `workflow2`, `workflow`) as shown in the original code. These represent the workflow structure with functions and their dependencies.

## Step 4: Implement the Workflow Parsing Function

Add the `parse_workflow` function to recursively build a NetworkX directed graph from the workflow dictionary:

```python
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
```

## Step 5: Initialize the Graph and Convert to Cytoscape Elements

Initialize the Factory, create the graph, parse the workflow, and convert the graph to Cytoscape elements. Note the reversed edge direction in the original code.

```python
f = Factory()
graph = nx.DiGraph()
parse_workflow(workflow, graph)

elements = []
for node in graph.nodes():
    elements.append({'data': {'id': node, 'label': graph.nodes[node]['label']}})

for edge in graph.edges():
    elements.append({'data': {'source': edge[1], 'target': edge[0]}, 'width': 100, 'height': 500})
```

## Step 6: Create the Dash App Layout with Tabs

Set up the Dash app with tabs: one for the workflow flowchart and one for the function list. Use `dcc.Tabs` and `dcc.Tab` for this.

```python
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1("Workflow Flowchart"),
    dcc.Tabs([
        dcc.Tab(label='Workflow', children=[
            cyto.Cytoscape(
                id='cytoscape',
                elements=elements,
                layout={'name': 'breadthfirst'},
                style={'width': '100%', 'height': '600px'},
                stylesheet=[
                    {'selector': 'node', 'style': {'content': 'data(label)', 'text-valign': 'center', 'text-halign': 'center', 'background-color': 'lightblue', 'shape': 'rectangle'}},
                    {'selector': 'edge', 'style': {'curve-style': 'bezier', 'target-arrow-shape': 'triangle', 'line-color': 'blue'}}
                ]
            )
        ]),
        dcc.Tab(label='Available Functions', children=[
            # Function list organized by folders
            html.Div([
                html.H2("Available Functions"),
                # Assuming f.all_functions is a dict like {'math': ['add', 'subtract'], ...}
                *[html.Div([
                    html.H3(folder),
                    html.Ul([html.Li(func, style={'border': '1px solid black', 'padding': '5px', 'margin': '5px', 'cursor': 'grab'}) for func in funcs])
                ]) for folder, funcs in f.all_functions.items()]
            ])
        ])
    ])
])
```

Note: For drag-and-drop, the functions are styled as boxes with `cursor: 'grab'`, but full drag-and-drop implementation requires additional JavaScript or Dash extensions (e.g., `dash-draggable`). The current code uses a right-click callback for replacement.

## Step 7: Add a Callback for Node Interaction

Implement a callback to handle node taps (right-clicks) for replacement. Currently, it prints the node ID; extend it to replace the node in the graph.

```python
@app.callback(
    dash.dependencies.Output('cytoscape', 'elements'),
    [dash.dependencies.Input('cytoscape', 'tapNodeData')]
)
def replace_node(data):
    if data:
        node_id = data['id']
        # Implement logic to replace the node (e.g., update graph, re-parse)
        print(f"Node {node_id} was right-clicked")
    return elements
```

## Step 8: Run the App

Add the main block to run the server:

```python
if __name__ == '__main__':
    app.run(debug=True)
```

## Running the App

Execute the script with `python dash_app_2.py`. The app will launch a local server with tabs for the workflow and functions. Nodes are draggable, and right-clicking a node triggers the callback. For full drag-and-drop from the function list to the graph, integrate a drag-and-drop library and update the callback accordingly.
