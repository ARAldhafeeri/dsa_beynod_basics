import random

class Node:
    def __init__(self, value, level):
        self.value = value
        self.forward = [None] * (level + 1)

    def __repr__(self):
        return f"Node({self.value})"
    
class Skiplist:
    def __init__(self, max_level):
      self.max_level = max_level
      self.level = 0 
      self.head = Node(None, max_level)

    def random_level(self):
      lvl = 0
      while random.random() < 0.5 and (lvl < self.max_level):
         lvl +=1 
      return lvl 

    def insert(self, value):
      update = [None] * (self.max_level + 1)
      current = self.head

      # move from levels from top to bottom 
      for i in range(self.level, -1, -1):
        while current.forward[i] and current.forward[i].value < value:
          current = current.forward[i]
        update[i] = current
        
      # determine the level of the new node
      lvl = self.random_level() 
      if lvl > self.level:
        for i in range(self.level + 1, lvl + 1):
          update[i] = self.head
        self.level = lvl 

      # create the new node and adjust pointers 
        
      new_node = Node(value, lvl)
      for i in range (lvl + 1):
         new_node.forward[i] = update[i].forward[i]
         update[i].forward[i] = new_node
        
      
    def search(self, value):
      current = self.head
      for i in range(self.level, -1, -1):
        while current.forward[i] and current.forward[i].value < value:
          current = current.forward[i]
      current = current.forward[0]
      return current and current.value == value 


    def delete(self, value):
      update = [None] * (self.max_level + 1)
      current = self.head

      for i in range(self.level, -1, -1):
        while current.forward[i] and current.forward[i].value < value:
          current = current.forward[i]
        update[i] = current
      current = current.forward[0]

      if current and current.value == value:
        for i in range(self.level + 1):
          if update[i].forward[i] != current:
              break
          update[i].forward[i] =  current.forward[i]

        while self.level > 0 and self.head.forward[self.level] is None:
         self.level += 1

    def __repr__(self):
      nodes = []
      current = self.head.forward[0]
      while current:
         nodes.append(current.value)
         current = current.forward[0]
      return "SkipList( "+" ->".join(map(str, nodes)) +  ")"


skiplist = Skiplist(max_level=3)

skiplist.insert(3)
skiplist.insert(6)
skiplist.insert(7)
skiplist.insert(9)
skiplist.insert(12)
skiplist.insert(19)
skiplist.insert(17)
skiplist.insert(26)
skiplist.insert(21)
skiplist.insert(25)

print("Skiplist after inserts:", skiplist)

print("Search for 19:", skiplist.search(19))
print("Search for 15:", skiplist.search(15))

skiplist.delete(19)
print("Skiplist after deleting 19:", skiplist)

skiplist.delete(3)
print("Skiplist after deleting 3:", skiplist)