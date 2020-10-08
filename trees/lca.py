class Node:
    def __init__(self, info): 
        self.info = info  
        self.left = None  
        self.right = None 
        self.level = None 

    def __str__(self):
        return str(self.info) 

class BinarySearchTree:
    def __init__(self): 
        self.root = None

    def create(self, val):  
        if self.root == None:
            self.root = Node(val)
        else:
            current = self.root
         
            while True:
                if val < current.info:
                    if current.left:
                        current = current.left
                    else:
                        current.left = Node(val)
                        break
                elif val > current.info:
                    if current.right:
                        current = current.right
                    else:
                        current.right = Node(val)
                        break
                else:
                    break

# Enter your code here. Read input from STDIN. Print output to STDOUT
'''
class Node:
      def __init__(self,info): 
          self.info = info  
          self.left = None  
          self.right = None 
           

       // this is a node of the tree , which contains info as data, left , right
'''


# Finds the path from root node to given root of the tree. 
# Stores the path in a list path[], returns true if path  
# exists otherwise false 
def findPath(root, path, k): 
  
    # Baes Case 
    if root is None: 
        return False
  
    # Store this node is path vector. The node will be 
    # removed if not in path from root to k 
    path.append(root) 
  
    # See if the k is same as root's key 
    if root.info == k : 
        return True
  
    # Check if k is found in left or right sub-tree 
    if ((root.left != None and findPath(root.left, path, k)) or
            (root.right!= None and findPath(root.right, path, k))): 
        return True 
  
    # If not present in subtree rooted with root, remove 
    # root from path and return False 
       
    path.pop() 
    return False
  
# Returns LCA if node n1 , n2 are present in the given 
# binary tre otherwise return -1 
def lca(root, n1, n2): 
  
    # To store paths to n1 and n2 fromthe root 
    path1 = [] 
    path2 = [] 
  
    # Find paths from root to n1 and root to n2. 
    # If either n1 or n2 is not present , return -1  
    if (not findPath(root, path1, n1) or not findPath(root, path2, n2)): 
        return -1 
  
    # Compare the paths to get the first different value 
    i = 0 
    while(i < len(path1) and i < len(path2)): 
        if path1[i] != path2[i]: 
            break
        i += 1
    return path1[i-1] 

tree = BinarySearchTree()
t = int(input())

arr = list(map(int, input().split()))

for i in range(t):
    tree.create(arr[i])

v = list(map(int, input().split()))

ans = lca(tree.root, v[0], v[1])
print (ans.info)
