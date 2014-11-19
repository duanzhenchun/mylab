def reverse_link(head):
    if not head:
        return head
    p1,p2,p3 = None, head, head.next
    while p3:
        p2.next=p1
        p1,p2,p3=p2,p3,p3.next
    p2.next=p1
    return p2

#simulate c structure
class Node(object):
    def __init__(self, v):
        self.v=v
        self.next=None

    def traverse(self):
        p=self
        while p:
            print p.v
            p=p.next
       

class Link(object):
    def __init__(self,lst0):
        lst=[Node(i) for i in lst0]
        if len(lst)>1:
            for i in range(len(lst)-1):
                lst[i].next = lst[i+1]
        self.head = lst[0]
        del lst
    

link=Link([2,5,6,8])
link.head.traverse()
res = reverse_link(link.head)
res.traverse()

