class Node:



    """
        Instance variables :
            @name   : String containing the name of the node to create
            @parent : Node Object representing the parent of the node to create
            @children : List of Constraint objects, each constraint contains a Set of Nodes
            @isRoot : boolean indicating whether the node is a root node or not
    """

    def __init__(self,name,parent,isRoot = False):
        """
            Pre :
                <name> : a string 
                <parent> : a Node Object
                <isRoot> : a boolean
            Post :
                /
        """
        self.name = name 
        self.parent = parent 
        self.children = [] 
        self.isRoot = isRoot


    def getAllChildrenName(self):
        """
            Pre :
                /
            Post :
                Returns a list of strinfs containing the name of every children of the current Node
        """
        toReturn = []

        for constraint in self.children:
            for child in constraint.nodeSet:
                toReturn.append(child.name)
        return toReturn

        
    def __eq__(self, other):
        """
            Pre :
                <other> : a Node Object
            Post :
                Returns True if the current Node and other are equal and False otherwise. Two Nodes are said
                Equal if they have the same name when they are root Nodes or if they have the same name,
                the same parents and the same childrent when they are not root Nodes
        """

        if not isinstance(other,Node):
            return False
        if len(self.children) != len(other.children):
            return False
        
        for i in range(len (self.children)):
            if self.children[i] not in other.children:
                
                return False
            
        if self.isRoot:
            return self.name == other.name
        
        return self.name == other.name and self.parent.name == other.parent.name
        
    def __str__(self):
        """
            Pre :
                /
            Post :
                Returns the string representation of the current Node. Here it is simply his name.
        """
        return self.name
    
    def __hash__(self):
        """
            Pre :
                /
            Post :
                Returns a hashed value of the name of the current Node
        """
        return hash(self.name)