class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

    def __repr__(self):
        return str(self.data)

    def __del__(self):
        print(f"Node Deleted : {self.data}")
        # del self


class DoubleLinkedList:

    def __init__(self):
        self.head = None
        self.tail = None

    def traverse_next(self):
        temp = self.head
        print(f"Current head: {self.head}")
        traversed_list = list()
        while temp:
            traversed_list.append(temp)
            temp = temp.next

        return traversed_list

    def traverse_prev(self):
        temp = self.head
        print(f"Current head: {self.head}")
        traversed_list = list()
        while temp:
            traversed_list.append(temp)
            temp = temp.prev

        return traversed_list


    def insert_after(self, data, position):
        pass

    def insert_before(self, data, position):
        pass

    def search(self, data):
        # Note: You have to search in both directions from the head as head could be anywhere

        if self.head is None:
            return False

        # Search from the head to the right nodes
        temp = self.head
        while temp:
            if temp.data == data:
                return True
            else:
                temp = temp.next

        # Search from the head to the left nodes
        temp = self.head
        while temp:
            if temp.data == data:
                return True
            else:
                temp = temp.prev

        return False

    def insert_at_left(self, data):
        node = Node(data)
        temp = self.head

        if self.head is None:
            self.head = node
            return self

        while temp:
            if temp.prev is None:
                temp.prev = node
                node.next = temp
                self.head = node
                break
            else:
                temp = temp.prev

        return self

    def insert_at_right(self, data):
        node = Node(data)

        if self.head is None:
            self.head = node

        temp = self.head
        while temp:
            if temp.next is None:
                temp.next = node
                node.prev = temp
                self.head = node
                break
            else:
                temp = temp.next

        return self


def create_linked_list():
    double_linked_list = DoubleLinkedList()
    double_linked_list.insert_at_left(0).insert_at_left(-1)
    print(double_linked_list.traverse_next())
    double_linked_list.insert_at_right(2).insert_at_right(3)
    print(double_linked_list.traverse_prev())


if __name__ == '__main__':
    create_linked_list()
