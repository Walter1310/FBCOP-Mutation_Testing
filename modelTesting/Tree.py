from Constraints import *
from Node import *


class Tree :

    # mettre ça dans une classe principale plutot

    # mettre les contraintes liées à l'enfant
    # mettre différents groupes d'enfants pour chaque contraintes
    # enfants : liste de tuples ([node object.s], Constraint object) (dictionnaire pas une bonne idée ex: si on a deux groupes avec une relation "or")
    # faire une liste en plus pour avoir tous les noeuds créer pour faciliter la recherche

    def __init__(self,rootName):
        self.flatList = [] #list of nodes useful if you want to find an element of the tree
        self.root = Node(rootName,None,isRoot = True)
        self.flatList.append(self.root)
        self.size = 1

    def addConstraintGroup(self,nodeNameList, constraint,parentName):
        parent = self.get(parentName)
        for nodeName in nodeNameList:
            toAddNode = Node(nodeName,parent)
            constraint.nodeSet.add(toAddNode)
            self.flatList.append(toAddNode)
            self.size+= 1

        parent.children.append(constraint)
        
    def removeNode(self,node):
        constraintGroup = self.getConstraintGroup(node)

        constraintGroup.NodeSet.remove(node)

        if constraintGroup.isEmpty():
            node.parent.children.remove(constraintGroup)
        
        self.flatList.remove(node)
        self.size -= 1
        return node
        
    def get(self,nodeName):
        for node in self.flatList:
            if node.name == nodeName:
                return node
        return None
    
    def getConstraintGroup(self,node):
        for child in node.parent.children:
            if node in child.nodeSet:
                return child
        return None
    
    def getConstraintGroupFromName(self,nodeName):
        node = self.get(nodeName)
        return self.getConstraintGroup(node)
    
    def getParentName(self,nodeName):
        return self.get(nodeName).parent.name
    
    def getParent(self,nodeName):
        return self.get(nodeName).parent
    
    def copyNodeWithOneChild(self,parentName,childName,constraint):
        newTree = Tree(parentName)
        newTree.addConstraintGroup([childName],constraint,parentName)
        return newTree


    def copyFromNode(self,tree, nodeToCopy,parent):
        
        #print ("nodeToCopy: ",nodeToCopy)
        #print ("parent: ",parent)


        newNode = Node(nodeToCopy.name,parent)
        tree.flatList.append(newNode)

        if len(nodeToCopy.children) ==0:
            return newNode

        for const in nodeToCopy.children:
            newConst = type(const)(nodeSet = set(self.copyFromNode(tree,childNode,newNode) for childNode in const.nodeSet))
            newNode.children.append(newConst)

        return newNode


    def copy(self):
        """
        newRoot = self.root.copy()
        newFlatList = [node.copy() for node in self.flatList if not node.isRoot]
        newFlatList.append(newRoot)
        newSize = self.size

        toReturn = Tree(newRoot.name)
        toReturn.flatList = newFlatList
        toReturn.size = newSize
        toReturn.root = newRoot

        return toReturn
        """
        #print (self)
        newTree = Tree(self.root.name)

        for const in self.root.children:
            newConst = type(const)(nodeSet=set(self.copyFromNode(newTree,childNode,newTree.root) for childNode in const.nodeSet))
            newTree.root.children.append(newConst)
        
        newTree.size = self.size
        return newTree

    
    def __eq__(self, other):
        if not isinstance(other,Tree):
            return False
        if len(self.flatList) != len(other.flatList): 
            return False
        
        for node in self.flatList:
            if node not in other.flatList:
                return False
            
        return self.size == other.size and self.root == other.root
    
    
    def __str__(self):
        toReturn =""
        for node in self.flatList:
            if len(node.children) == 0:
                continue
            toReturn += str(node)
            toReturn += " -> "
            for const in node.children:
                toReturn+= str(const)
                toReturn += " "
            toReturn += "\n"
            
        return toReturn
        #return str([str(node) +" "+ str(len(node.children)) for node in self.flatList])


            

    """
    use case :
    -> read the firs line in the context file
    -> parse ("Context", constraint, children)
    -> new Tree("Context")
    -> tree.addConstraintGroup(children, constraint)
    -> read the next line
    -> parse (parentName, constrain, children)
    -> check if parent is in the list of nodes, if yes : tree.addConstraintGroup(children,constraint,parentName)
                                                else : trhrow error message

    """

    

    
        
    