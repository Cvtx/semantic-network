# -*- coding: utf-8 -*-

# Commented out IPython magic to ensure Python compatibility.
# from IPython.display import clear_output

# %pip install dash
# %pip install dash-cytoscape
# %pip install tabulate
# clear_output()

import os
import uuid
import json
import dash
from dash import html
import dash_cytoscape as cyto
from tabulate import tabulate
from collections import defaultdict
import plotly.graph_objects as go
from plotly.subplots import make_subplots


class Node():
    def __init__(self, label: str = "Node", x: int = 0, y: int = 0) -> None:
        self.id = str(uuid.uuid4())
        self.label = label
        self.position = {'x': x, 'y': y}

class Edge():
    def __init__(self, source: Node, target: Node, label: str="") -> None:
        self.source = source
        self.target = target
        self.label = label

class SemanticNetwork():
    def __init__(self) -> None:
        self.elements = []
        self.nodes = []

    def add_node(self, node: Node):
        if (self.get_node_by_label(node.label) == None):
            #data = {'data': {'id': node.id, 'label': node.label}, 'position': node.position, 'classes': 'top-center'}
            data = {'data': {'id': node.id, 'label': node.label}}
            self.elements.append(data)
            self.nodes.append(node)
            #print(f"Node {node.label} added at {node.position}.")

    def add_edge(self, edge: Edge):
        data = {'data': {'source': edge.source.id, 'target': edge.target.id, 'label': edge.label}, 'classes': 'autorotate'}
        self.elements.append(data)

    def add_edge_by_labels(self, source: str, target: str, label: str = ""):
        s = self.get_node_by_label(source)
        t = self.get_node_by_label(target)
        if (s != None and t != None):
            data = {'data': {'source': s.id, 'target': t.id, 'label': label}, 'classes': 'autorotate'}
            self.elements.append(data)

    def get_node_by_label(self, label: str) -> Node | None:
        return next((node for node in self.nodes if node.label == label), None)

    def get_elements(self):
        return self.elements


def get_node_label_by_id(data: list, id: str) -> dict | None:
    obj = next((l for l in data if 'source' not in l['data'] and l['data']['id'] == id), None)
    return obj['data']['label']

def get_frame(data: list, name: str):
    obj = next((l for l in data if 'source' not in l['data'] and l['data']['label'] == name), None)
    if obj != None:
        obj_id = obj['data']['id']
        obj_label = obj['data']['label']
        references = [r for r in data if 'source' in r['data'] and r['data']['source'] == obj_id]
        print(f"References of this object: {len(references)}")
        properties = defaultdict(list)
        properties['Имя'].append(obj_label)
        for r in references:
            l = r['data']['label']
            id = r['data']['target']
            v = get_node_label_by_id(data, id)
            properties[l].append(v)
        return properties

# net 1
net = SemanticNetwork()
net.add_node(Node("Птица"))
net.add_node(Node("Животные"))
net.add_node(Node("Летать"))
net.add_node(Node("Оперенье"))
net.add_node(Node("Страус"))
net.add_node(Node("Ходить"))
net.add_node(Node("Пингвин"))
net.add_node(Node("Черный"))
net.add_node(Node("Желтый"))
net.add_node(Node("Петь"))
net.add_node(Node("Коричневый"))
net.add_node(Node("Канарейка"))
net.add_node(Node("Дрозд"))
net.add_edge_by_labels("Птица", "Животные", "является")
net.add_edge_by_labels("Птица", "Летать", "умеет")
net.add_edge_by_labels("Птица", "Оперенье", "имеет")
net.add_edge_by_labels("Страус", "Птица", "является")
net.add_edge_by_labels("Страус", "Ходить", "умеет")
net.add_edge_by_labels("Пингвин", "Птица", "является")
net.add_edge_by_labels("Пингвин", "Ходить", "умеет")
net.add_edge_by_labels("Пингвин", "Черный", "имеет цвет")
net.add_edge_by_labels("Канарейка", "Желтый", "имеет цвет")
net.add_edge_by_labels("Канарейка", "Птица", "является")
net.add_edge_by_labels("Канарейка", "Петь", "умеет")
net.add_edge_by_labels("Дрозд", "Коричневый", "имеет цвет")
net.add_edge_by_labels("Дрозд", "Петь", "умеет")
net.add_edge_by_labels("Дрозд", "Птица", "является")

# net 2
#net = SemanticNetwork()
net.add_node(Node("ТУ-134"))
net.add_node(Node("Самолет"))
net.add_node(Node("Мотор"))
net.add_node(Node("Бензин"))
net.add_node(Node("Крылья"))
net.add_node(Node("Летать"))
net.add_node(Node("Законы аэродинамики"))
net.add_node(Node("Птица"))
net.add_node(Node("Орел"))
net.add_node(Node("Клюв"))
net.add_node(Node("Оперение"))
net.add_edge_by_labels("ТУ-134", "Самолет", "является")
net.add_edge_by_labels("Самолет", "Мотор", "имеет")
net.add_edge_by_labels("Мотор", "Бензин", "использует")
net.add_edge_by_labels("Самолет", "Крылья", "имеет")
net.add_edge_by_labels("Самолет", "Летать", "умеет")
net.add_edge_by_labels("Самолет", "Законы аэродинамики", "использует")
net.add_edge_by_labels("Птица", "Летать", "Умеет")
net.add_edge_by_labels("Птица", "Крылья", "Имеет")
net.add_edge_by_labels("Птица", "Клюв", "Имеет")
net.add_edge_by_labels("Птица", "Оперение", "Имеет")
net.add_edge_by_labels("Птица", "Законы аэродинамики", "использует")
net.add_edge_by_labels("Орел", "Законы аэродинамики", "планирующий полет")
net.add_edge_by_labels("Орел", "Крылья", "широкие")
net.add_edge_by_labels("Орел", "Птица", "является")

# net 3
#net = SemanticNetwork()
net.add_node(Node("Млекопитающее"))
net.add_node(Node("Позвоночник"))
net.add_node(Node("Кошка"))
net.add_node(Node("Шерсть"))
net.add_node(Node("Медведь"))
net.add_node(Node("Кит"))
net.add_node(Node("Вода"))
net.add_node(Node("Рыба"))
net.add_node(Node("Животное"))
net.add_edge_by_labels("Млекопитающее", "Позвоночник", "имеет")
net.add_edge_by_labels("Млекопитающее", "Животное", "есть")
net.add_edge_by_labels("Кошка", "Млекопитающее", "есть")
net.add_edge_by_labels("Кошка", "Шерсть", "имеет")
net.add_edge_by_labels("Медведь", "Шерсть", "имеет")
net.add_edge_by_labels("Медведь", "Млекопитающее", "есть")
net.add_edge_by_labels("Кит", "Млекопитающее", "есть")
net.add_edge_by_labels("Кит", "Вода", "живет в")
net.add_edge_by_labels("Рыба", "Вода", "живет в")
net.add_edge_by_labels("Рыба", "Животное", "есть")

headers = ["Свойство", "Значение"]
# print frames
for node in net.nodes:
    frame = get_frame(net.get_elements(), node.label)
    table = [[k,', '.join(v)] for k, v in frame.items()]
    print(tabulate(table, headers=headers, tablefmt='fancy_grid'))

n = len(net.nodes)
headers = ["Свойство", "Значение"]

fig = make_subplots(
    rows=n, cols=1,
    #shared_xaxes=True,
    vertical_spacing=0.01,
    horizontal_spacing = 0.01,
    specs=[[{"type": "table"}] for i in range(n)]
)

label = net.nodes[0].label
label = "Кит"

for i, node in enumerate(net.nodes):
    label = node.label
    frame = get_frame(net.get_elements(), label)
    table = [[k,', '.join(v)] for k, v in frame.items()]
    keys =  [[k] for k, v in frame.items()]
    values = [[', '.join(v)] for k,  v in frame.items()]

    # fig = go.Figure(data=[go.Table(header=dict(values=headers),
    #     cells=dict(values=[keys, values]))
    # ])

    fig.add_trace(go.Table(header=dict(values=headers), cells=dict(values=[keys, values])), row=i + 1, col= 1)

fig.update_layout(
    height= n * 120,
    autosize=True,
    showlegend=False,
    title_text="Фреймы семантической сети",
)
fig.show()

# run server
if __name__ == '__main__':
    # read stylesheet
    fileObject = open(os.path.join(os.path.abspath(''), "cy-style.json"), "r")
    jsonContent = fileObject.read()
    stylesheet = json.loads(jsonContent)

    app = dash.Dash(__name__)

    app.layout = html.Div([
        cyto.Cytoscape(
            id='cytoscape-two-nodes',
            layout={'name': 'breadthfirst'},
            style={'width': '100%', 'height': '100vh'},
            elements = net.get_elements(),
            stylesheet = stylesheet
        )
    ])

    app.run(debug=False, port=os.getenv("PORT", "8060"))
