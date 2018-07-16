from linked_list import *

class ExtendedLinkedList(LinkedList):
    def __init__(self, L = None):
        super().__init__(L)

    def rearrange(self):
        L=LinkedList()
        start=int(len(self)//2)
        L.head=Node(self.value_at(start))
        index=start
        for i in range(1,int(len(self))):
            index=index+((-1)**i)*i
            L.append(self.value_at(index))
        node=self.head
        node1=L.head
        while node1:
            node.value=node1.value
            node=node.next_node
            node1=node1.next_node
