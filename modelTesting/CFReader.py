import sys
from Constraints import *
from Tree import  Tree

"""
    This class is used to read a context/feature model file.

    -The file should be in .txt format 
    -Each line should have this format: <parent>/<constraint>/<children1>-<children2>/<children3>...
    -The file can contain emplty lines
    -The first word of the first line should be either "Context" or "Feature"
    -You can have spaces before and after '/'
    -You can have spaces before and after '-'
    -If a name is on the parent end and is not "Context" or "Feature", it must be in another line's children end
    -If a name is "Context" or "Feature" but not on the parent end, an error should be raised
    -A name can only contain alphanumeric characters
    -We can add a child to any node at any as long as the parent node already exists
"""

class CFReader:


    """
        @context and @feature are used to distinguish the case of a context file or a feature file to understand which
        file is read and therefore are used as class variables
    """
    context = 0
    feature = 1



    """
        Instance variables :
            @filename : String containing the name of the file to read
            @fileType : int specifying which type of file to read. Its value is either @context or @feature
    """

    def __init__(self, fileName):
        """
            Pre : 
                <filename> : string containing the path to a context or a feature file/
            Post:
                /
        """
        self.fileName = fileName
        self.fileType = self.context if fileName.endswith("contexts.txt") else self.feature


    def readFile(self):
        """
            Pre:
                /
            Post:
                Parses the file provided by @fileName and returns a @Tree containing representing either the context model or the feature model
            Throws:
                @SyntaxError if the root of the encoded tree is not "Context" or "Feature" or if the name of the root does not correspond to
                             the correct file.
        """

        file = open(self.fileName, 'r')
        lineList = []
        lineCount = 1
        for line in file:
            if line != '\n':
                lineList.append((lineCount,line.rstrip()))
            lineCount+= 1

        #Error cases
        if not (lineList[0][1].startswith('Context') )and self.fileType == self.context:
            sys.tracebacklimit=0 
            raise SyntaxError ("SYNTAX ERROR on the following line ({}) in {} file:\n\t{}\n\n{} expected, found {}.".format(lineList[0][0],self.fileName,line,"Context",lineList[0][1]))
        
        if not (lineList[0][1].startswith('Feature') )and self.fileType == self.feature:
            sys.tracebacklimit=0 
            raise SyntaxError ("SYNTAX ERROR on the following line ({}) in {} file:\n\t{}\n\n{} expected, found {}.".format(lineList[0][0],self.fileName,line,"Feature",lineList[0][1]))
        
        if self.fileType == self.context:
            tree = Tree("Context")
        else : tree = Tree("Feature")
        

        for (lineNum,line) in lineList:
            self.processLine(lineNum,line, tree)
        
        file.close()

        return tree



    def processLine(self, lineNum, line, tree):
        """
            Pre:
                <lineNum> : int representing the number of the line to parse
                <line>    : String corresponding to the line to parse
                <tree>    : @Tree object to whoich each parsed element in <line> will be added
            Post:
                Parses a <line> to detect the parent @Node, children @Node and the @Constraint that must be added to <tree>
            Throws:
                @SyntaxError when <line> does not respect the '/' separation between the parent, the constraint and the children
                @ValueError when the parent name contains non alphabetic characters
                @ValueError when the parent name is not present in <tree>
                @ValueError when the given constraint name in <line> does not match any known constraint
                @ValueError when the a child name contains non alphabetic characters
                @ValueError when there is a 'Context' or a 'Feature' appearing in the children part of <line>
                @ValueError when a given child already exists in <tree>
                
        """
        # no need to check if the fist line start with context or feature because it is already added in the tree so we will just raise an error if the parent is not found

        #<splittedLine> has the following shape = [parent,constraint,children]
        splittedLine =  [split.strip() for split in line.split('/')]
        if len(splittedLine) != 3:
            sys.tracebacklimit=0 
            raise SyntaxError ("SYNTAX ERROR on the following line ({}) in {} file:\n\t{}\n\nThe line does not respect the correct format <Parent>/<Constraint>/<Child1>-<Child2>-... .".format(lineNum,self.fileName,line))
        
        #get the parent
        parentName = splittedLine[0]
        if not parentName.isalnum():
            sys.tracebacklimit=0 
            raise ValueError ("Value ERROR on the following line ({}) in {} file : \n\t{}\n\n the parent must contain only alphanumeric characters and cannot contain any special character.".format(lineNum,self.fileName,line))
        
        parentNode = tree.get(parentName)
        

        if parentNode is None:
            sys.tracebacklimit = 0
            raise ValueError ("ValueError on the following line ({}) in {} file : \n\t{}\n\n Unknown parent name.".format(lineNum,self.fileName,line))
        

        #get the constraints
        constraintString = splittedLine[1]
        if constraintString == "Or":
            constraint = OrConstraint()
        elif constraintString == "And":
            constraint = AndConstraint()
        elif constraintString == "Alternative":
            constraint = AlternativeConstraint()
        elif constraintString == "Mandatory":
            constraint = MandatoryConstraint()
        elif constraintString == "Optional":
            constraint = OptionalConstraint()
        if constraintString not in ["Or", "And", "Alternative", "Mandatory", "Optional"]:
            sys.tracebacklimit = 0
            raise ValueError ("ValueError on the following line ({}) in {} file : \n\t{}\n\n Unknown constraint name : {}.".format(lineNum,self.fileName,line,constraintString))
        
        #get childrean and add them to the tree
        children = splittedLine[2]
        childrenList = [child.strip() for child in children.split('-')]

        for child in childrenList:
            if not child.isalnum():
                sys.tracebacklimit = 0
                raise ValueError ("ValueError on the following line ({}) in {} file : \n\t{}\n\n <{}> must contain only alphanumeric characters and cannot contain any special character.".format(lineNum,self.fileName,line, child))
            if child == "Context" or child == "Feature":
                sys.tracebacklimit = 0
                raise ValueError ("ValueError on the following line ({}) in {} file : \n\t{}\n\n <{}> must be at the top of the tree and therefore cannot be a child node.".format(lineNum,self.fileName,line, child))
            if tree.get(child) != None :
                sys.tracebacklimit = 0
                raise ValueError ("ValueError on the following line ({}) in {} file : \n\t{}\n\n <{}> already exists and therefore cannot have a second parent.".format(lineNum,self.fileName,line, child))
        
        tree.addConstraintGroup(childrenList, constraint, parentNode.name)


