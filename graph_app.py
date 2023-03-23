import networkx as nx
from pyvis.network import Network
import tkinter as tk
from tkinter import ttk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Graph Visualization")

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both')

        self.init_graph()

    def init_graph(self):
        G = nx.karate_club_graph()
        self.nt = Network(height='400px', width='100%', directed=False)

        for node in G.nodes:
            self.nt.add_node(node)

        for edge in G.edges:
            self.nt.add_edge(edge[0], edge[1])

        self.nt.set_options("""
        var options = {
          "nodes": {
            "borderWidth": 2
          },
          "edges": {
            "color": {
              "inherit": true
            },
            "smooth": {
              "type": "continuous"
            }
          },
          "physics": {
            "minVelocity": 0.75
          }
        }
        """)

        self.nt.show("graph.html")

        graph_frame = ttk.Frame(self.notebook)
        self.notebook.add(graph_frame, text="Graph")

        self.webview = tk.Text(graph_frame, wrap="word", width=80, height=20)
        self.webview.pack(expand=True, fill='both')

        with open("graph.html") as file:
            html_code = file.read()

        self.webview.insert('1.0', html_code)

        self.nt.enable_physics(True)
        self.webview.tag_bind("node", "<Button-1>", self.on_node_click)

        for node in G.nodes:
            self.webview.tag_add("node", f"1.0+{html_code.find(f'>{node}</span>') + 2}", f"1.0+{html_code.find(f'>{node}</span>') + 2+len(str(node))}")


    def on_node_click(self, event):
        index = self.webview.index(f"@{event.x},{event.y}")
        node = int(self.webview.get(index))

        node_connections = list(self.nt.get_adj_list()[node])

        connections_frame = ttk.Frame(self.notebook)
        self.notebook.add(connections_frame, text=f"Node {node}")

        connections_label = tk.Label(connections_frame, text=f"Node {node} is connected to nodes: {', '.join(map(str, node_connections))}")
        connections_label.pack()

        self.notebook.select(connections_frame)

if __name__ == "__main__":
    app = App()
    app.mainloop()
