class KDTreeNode:
    def __init__(self, point, left=None, right=None):
        self.point = point
        self.left = left
        self.right = right

class KDTree:
    def __init__(self):
        self.root = None

    def build(self, points, depth=0):
        """Build the kd tree for n-dimension O(nlogn)"""
        # base case
        if not points:
            return None
        # get curr axis in traversal
        k = len(points[0])
        axis = depth % k

        # sort popints to get the median where we split the plane into two halves
        points.sort(key=lambda x: x[axis])
        median = len(points) // 2

        # build root, left, right recursivly
        node = KDTreeNode(
            point=points[median],
            left=self.build(points[:median], depth + 1),
            right=self.build(points[median + 1:], depth + 1)
        )
        return node

    def insert(self, root, point, depth=0):
        """Insert a node in the kd tree O(logn)"""
        if root is None:
            return KDTreeNode(point)

        # get the curr axis in the recursive call
        # cycle through the dimensions for every call
        k = len(point)
        axis = depth % k

        # determine to move left or right of root based on
        # comparing the axis point value 
        # e.g. root -> x = 2, point -> x = 3 go to right sub tree
        if point[axis] < root.point[axis]:
            root.left = self.insert(root.left, point, depth + 1)
        else:
            root.right = self.insert(root.right, point, depth + 1)

        return root

    def search(self, root, point, depth=0):
        """Search for a point in the kd tree O(logn)"""
        if root is None:
            return None
        if root.point == point:
            return root.point

        # get the curr axis in the recursive call
        # cycle through the dimensions for every call
        k = len(point)
        axis = depth % k

        # determine to move left or right of root based on
        # comparing the axis point value 
        # e.g. root -> x = 2, point -> x = 3 go to right sub tree
        if point[axis] < root.point[axis]:
            return self.search(root.left, point, depth + 1)
        else:
            return self.search(root.right, point, depth + 1)

    def remove(self, root, point):
        """ Remove node from k-d tree O(logn)"""
        path = []
        # Find the node and collect the path
        self._find_and_collect_path(root, point, path)

        if not path:
            return root  # Point not found, return original root

        # get parent in path, node to be removed
        parent = path[-1]
        node_to_remove = path[-2]

        # rebuild sub tree
        if parent.left and parent.left.point == point:
            parent.left = None
        elif parent.right and parent.right.point == point:
            parent.right = None

        return root

    def _find_and_collect_path(self, root, point, path):
        if root is None:
            return False
        path.append(root)
        if root.point == point:
            return True

        k = len(point)
        axis = len(path) % k

        if point[axis] < root.point[axis]:
            return self._find_and_collect_path(root.left, point, path)
        else:
            return self._find_and_collect_path(root.right, point, path)


    def nearest_neighbor(self, root, point, depth=0, best=None):
        if root is None:
            return best

        # get current axises of recursive call
        k = len(point)
        axis = depth % k

        next_branch = None
        opposite_branch = None

        # compare to move left or right
        if point[axis] < root.point[axis]:
            next_branch = root.left
            opposite_branch = root.right
        else:
            next_branch = root.right
            opposite_branch = root.left

        # Only update best if root.point is not the same as point
        if root.point != point:
            best = self.closer_distance(point, best, root.point)
            
        best = self.nearest_neighbor(next_branch, point, depth + 1, best)

        if (point[axis] - root.point[axis]) ** 2 < self.distance(point, best):
            best = self.nearest_neighbor(opposite_branch, point, depth + 1, best)

        return best

    @staticmethod
    def distance(point1, point2):
        return sum((x - y) ** 2 for x, y in zip(point1, point2))

    @staticmethod
    def closer_distance(point, p1, p2):
        if p1 is None:
            return p2
        if p2 is None:
            return p1
        d1 = KDTree.distance(point, p1)
        d2 = KDTree.distance(point, p2)
        return p1 if d1 < d2 else p2


# Usage example:

# Create KDTree instance
tree = KDTree()

# Build the tree from a list of points
points = [(2, 3), (5, 4), (9, 6), (4, 7), (8, 1), (7, 2)]
tree.root = tree.build(points)

# Insert a point
tree.root = tree.insert(tree.root, (6, 5))

# Search for a point
print(tree.search(tree.root, (5, 4)))  # Output: (5, 4)

# Remove a point
tree.root = tree.remove(tree.root, (5, 4))

# Find nearest neighbor
print(tree.nearest_neighbor(tree.root, (5, 4)))  #  (6, 5)
