class ASTNode:
    def __init__(self, node_type, **kwargs):
        self.type = node_type
        self.fields = kwargs

    def __repr__(self):
        return f"ASTNode(type={self.type}, fields={self.fields})"
