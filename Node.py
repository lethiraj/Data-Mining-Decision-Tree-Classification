class Node:
    def __init__(self,data = ''):
        self.data = data
        self.parent = None
        self.n_child = 0
        self.children = []

    def is_empty(self):
        return (self.data is None)

    def set_parent(self, parent):
        self.parent = parent

    def set_data(self,data):
        self.data = data

    def get_parent(self):
        return self.parent

    def get_data(self):
        return self.data

    def get_n_child(self):
        return self.n_child

    def add_child(self, child):
        self.children.append(child)
        self.n_child += 1

    def get_children(self):
        return self.children
