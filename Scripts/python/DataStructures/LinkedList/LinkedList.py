class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

    def __repr__(self):
        return self.data

    def __del__(self):
        print(f"Node Deleted : {self.data}")
        # del self

class LinkedList:
    def __init__(self):
        self.head = None

    def traverse(self):
        """
        Traverses the Linked list
        Returns:

        """
        temp = self.head
        traversed_list = list()
        while temp:
            traversed_list.append(temp.data)
            temp = temp.next

        return traversed_list

    def push(self, data):
        """
        Pushes the head to the right of the list and adds the new element to the beginning of the list
        Args:
            data:
        Returns: self so that you can chain multiple push() requests
        """
        if data:
            node = Node(data)

        current_head = self.head
        node.next = current_head
        self.head = node

        return self

    def append(self, data):
        """
        Appends a node to the end of the linked list. This requires the entire linked list to be traversed
        Args:
            data:

        Returns:

        """
        if data:
            node = Node(data)

        if self.head is None:
            self.head = node
            return self

        temp = self.head
        while temp:
            if temp.next is None:
                temp.next = node
                break
            else:
                temp = temp.next
        return self

    def insert_after(self, data, pos):
        """
        Inserts a node after the said position
        Args:
            data: the data to be inserted
            pos: position at which it needs to be inserted

        Returns: self  - faciliates multiple chained insert() requests

        """
        print(pos)
        if pos == -1:
            self.push(data)

        if data:
            node = Node(data)

        counter = 0
        temp = self.head
        while temp:
            if counter == pos:
                next_node = temp.next
                temp.next = node
                node.next = next_node
                return self
            else:
                temp = temp.next
                counter += 1
        else:
            self.append(data)

    def search(self, data):
        """
        Searches the linked list for the data
        Args:
            data:

        Returns: if found returns true else false

        """
        temp = self.head
        while temp:
            if temp.data == data:
                return True
            else:
                temp = temp.next
        return False

    def index(self, data):
        """
        Returns the position of the data (first occurence) within the linked list
        Args:
            data:

        Returns:

        """
        ctr = 0
        temp = self.head
        while temp:
            if temp.data == data:
                return ctr
            else:
                temp = temp.next
                ctr += 1
        return None

#TODO: pop(), delete_at_pos(), delete_at_end()
def delete_at_pos():


def create_linked_list():
    ## Create a linked_list object
    linked_list = LinkedList()

    ## Now let's create some nodes
    node1 = Node("A")
    node2 = Node("B")
    node3 = Node("C")

    ## Linking the nodes
    node1.next = node2
    node2.next = node3

    linked_list.head = node1
    # print(linked_list.head)
    # print(linked_list.head.next)
    # print(linked_list.head.next.next)
    # print(linked_list.head.next.next.next)

    return linked_list


def linked_list_actions():
    print("Traversing a linked list")
    linked_list = create_linked_list()
    traversed_nodes = linked_list.traverse()
    print(traversed_nodes)
    linked_list.push("D").push("E")
    traversed_nodes = linked_list.traverse()
    print(traversed_nodes)
    linked_list.append("F").append("G")
    traversed_nodes = linked_list.traverse()
    print(traversed_nodes)
    linked_list.insert_after("X", 11)
    traversed_nodes = linked_list.traverse()
    print(traversed_nodes)
    result = linked_list.search("C")
    print(f"Search Result: {result}")
    result = linked_list.index("C")
    print(f"Data found at position: {result}")


if __name__ == '__main__':
    linked_list_actions()
