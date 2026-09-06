
class Node:
  def __init__(self,value,child=None,next=None):
    self.value=value
    self.next=next
    self.child=child


class LinkedList:
  def __init__(self):
    self.head=None
#   def insert(self,value,child=None):
#     nod=Node(value,child)
#     if(self.head is None ):
#       self.head=nod
#       return self.head

#     node=self.head
#     while(node.next!=None):
#       node=node.next
#     node.next=nod
#     return nod  # Return the newly inserted node 

  def insert(self,value):
     nod=Node(value)
     if(self.head is None ):
       self.head=nod
       return self.head
 
     node=self.head
     while(node.next!=None):
       node=node.next
     node.next=nod
     return nod  # Return the newly inserted node 
  
  def flatten(self):
     if self.head is None:
         return self.head
     node = self.head
     while node is not None:
        if node.child is not None:
            storing_next_address=node.next
            node.next=node.child
            node.child=None
            next_node=node.next
            while next_node.next is not None:
               next_node=next_node.next
            next_node.next=storing_next_address
        node=node.next

#   def display(self):
#     node=self.head
#     while(node!=None):
#         print(node.value,end="->")
#         child_node=node.child
#         # if child is there go through the child linked list and print the values
#         # if child is not there then go to current child node and next node and print the values
#         if(node.child!=None):
#             child_node=node.child
#             while(child_node!=None):
#                 nodek=child_node
#                 while(nodek!=None):
#                     print(nodek.value,end="->")
#                     nodek=nodek.next
#                 child_node=child_node.child 
#         node=node.next
  def middleElement(self):
    node=self.head
    fast=self.head
    slow=self.head
    while(fast.next!=None and fast.next.next!=None):
        fast=fast.next.next
        slow=slow.next
    return slow.value

  def deleteNode(self,value):
    if(self.head is None):
        return self.head
    node=self.head
    while(node.next!=None):
        if(node.next.value ==value):
           node.next=node.next.next
        node=node.next
           
       
    return self.head
  def display(self):  
        node=self.head
        while(node!=None):
            print(node.value,end="->")
            node=node.next
  
l=LinkedList()
node1=l.insert(1)
# k=Node(7,next=Node(8),child=Node(3,next=Node(10),child=Node(5)))

node=l.insert(2)#,child=k)
l.insert(3)
l.insert(4)
l.insert(5)
# l.flatten()


print(l.middleElement())
l.deleteNode(3)
l.display()