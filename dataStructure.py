class Node:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.rightChild = None
        self.leftChild = None
        self.parent = None


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, _key, _value):
        nodeToInsert = Node(_key, _value)
        currentNode = self.root
        parentNode = None
        if currentNode is not None:
            while currentNode is not None:
                if currentNode.key > _key:
                    parentNode = currentNode
                    currentNode = parentNode.leftChild
                else:
                    parentNode = currentNode
                    currentNode = parentNode.rightChild

            if parentNode.key > _key:
                parentNode.leftChild = nodeToInsert
            else:
                parentNode.rightChild = nodeToInsert

            nodeToInsert.parent = parentNode
        else:
            self.root = nodeToInsert

    def search(self, key):
        currentNode = self.root
        while True:
            if currentNode is None:
                return None
            elif currentNode.key == key:
                return currentNode.value
            else:
                if currentNode.key > key:
                    currentNode = currentNode.left_child
                else:
                    currentNode = currentNode.right_child
