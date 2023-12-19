import sys


def visualize_tree(tree, filename="tree.html"):

    class TreeNode:
        def __init__(self, value):
            self.value = value
            self.children = []

        def add_child(self, value):
            self.children.append(TreeNode(value))

    def to_mermaid(tree, node, parent_id=None, graph=None, index=None, show_terminated=False):
        if node < 0:
            return graph

        if graph is None:
            graph = ["graph LR"]
            graph.append("classDef terminated fill:#f99,stroke:#333,stroke-width:1px;")  # terminatedのクラス定義

        node_id = str(node)
        node_label = f"n={tree.node_visit_count(node)}"
        graph.append(f"    {node_id}[\"{node_label}\"]")

        terminated = tree.terminated[node]

        if terminated:
            graph.append(f"    class {node_id} terminated;")

        if parent_id is not None and index is not None:
            r = tree.reward(parent_id, index)
            n = tree.visit_count(parent_id, index)
            q = tree.qvalue(parent_id, index)
            graph.append(f"    {parent_id} -->|a={index}<br>r={r:.02f}<br>q={q:.02f}<br>n={n}| {node_id}")

        if not terminated or show_terminated:
            for i, child in enumerate(tree.children[node]):
                to_mermaid(tree, child, node, graph, i)

        return graph


    def generate_html(mermaid_code):
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
        <title>Mermaid Tree Visualization</title>
        <script src="https://cdn.jsdelivr.net/npm/mermaid@8.13.5/dist/mermaid.min.js"></script>
        <script>mermaid.initialize({{startOnLoad:true}});</script>
        </head>
        <body>
        <div class="mermaid">
        {mermaid_code}
        </div>
        </body>
        </html>
        """

    mermaid_code = to_mermaid(tree, 0)
    html_content = generate_html("\n".join(mermaid_code))
    with open(filename, 'w') as file:
        file.write(html_content)
    print(f'Tree visualization is generated at ./{filename}', file=sys.stderr)