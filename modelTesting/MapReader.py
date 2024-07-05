from MappingModel import *
from Tree import *
from CFReader import *
import sys

class MapReader:

    """
    This class should contain only one method : fileReader. 

    It is used to create a MappingModel object in order to
    Represent the mapping between a context and a feature in 
    the CFModel

    """



    """
        Instance variables :
            @mappingFile : String containing the name of the mapping file
            @contextTree : Tree Object representing the tree containing all the contexts and their relations
            @featureTree : Tree Object representing the tree containing all the features and their relations
    """

    def __init__(self,mappingFile,contextTree,featureTree):
        """
            Pre :
                <mappingFile> : a string 
                <contextTree> : a Tree Object
                <featureTree> : a Tree Object
            Post :
                /
        """
        self.mappingFile = mappingFile
        self.contextTree = contextTree
        self.featureTree = featureTree


    def readFile(self):
        """
            Pre :
                /
            Post :
                Returns a MappingModel object representing the mapping between the contexte model and the feature model as described in the @mappingFile
        """
        file = open(self.mappingFile,'r')
        lineList = []
        lineCount = 1
        for line in file:
            if line != '\n':
                lineList.append((lineCount,line.rstrip()))
            lineCount+= 1

        file.close()

        mapping = MappingModel()

        for (lineNumber,line) in lineList:
            self.processLine(lineNumber,line,mapping)
        return mapping


        
    def processLine(self,lineNum,line,mapping):
        """
            Pre :
                <lineNum> : an integer representing the number of the line that is being processed
                <line>    : a string, this is the line that is being processed in the mapping file
                <mapping> : the MappingModel object that is being filled throughout the process
            Post :
                Reads the <line> and verifies its syntax in order to add a new entry in <mapping>
            Throws:
                @SyntaxError if <line> does not respect the following syntax : <ContextNode1>,<ContextNode2>,...-"ACTIVATES"-<FeatureNode1>,<FeatureNode2>,... .
                @ValuedError if the root is part of a mapping, if a context/feature does not exist or if a name containns non alphanumeric characters. 
        """
        splittedLine =  [split.strip() for split in line.split('-')]
        if len(splittedLine) != 3:
            sys.tracebacklimit=0
            raise SyntaxError ("SYNTAX ERROR on the following line ({}) in {} file:\n\t{}\n\nThe line does not respect the correct format <ContextNode1>,<ContextNode2>,...-\"ACTIVATES\"-<FeatureNode1>,<FeatureNode2>,... .".format(lineNum,self.mappingFile,line))
        

        # checks for the "ACTIVATES"
        activates = splittedLine[1]
        if activates != "ACTIVATES":
            sys.tracebacklimit = 0
            raise SyntaxError ("SYNTAX ERROR on the following line ({}) in {} file:\n\t{}\n\nExpected \"ACTIVATES \" but got {} instead.".format(lineNum,self.mappingFile,line,activates))
        
        #gets the contexts list
        ctxNameList = [ctxName.strip() for ctxName in splittedLine[0].split(",")]
        for ctxName in ctxNameList:
            if not ctxName.isalnum():
                sys.tracebacklimit = 0
                raise ValueError ("ValueError on the following line ({}) in {} file : \n\t{}\n\n <{}> must contain only alphanumeric characters and cannot contain any space character.".format(lineNum,self.mappingFile,line, ctxName))
            if ctxName == "Context":
                sys.tracebacklimit = 0
                raise ValueError ("ValueError on the following line ({}) in {} file : \n\t{}\n\n You cannot use the root of a tree in a mapping.".format(lineNum,self.mappingFile,line))
            if self.contextTree.get(ctxName) == None:
                sys.tracebacklimit = 0
                raise ValueError ("ValueError on the following line ({}) in {} file : \n\t{}\n\n Context {} not found in the context file.".format(lineNum,self.mappingFile,line, ctxName))

        #gets the features list
        featNameList = [featName.strip() for featName in splittedLine[2].split(",")]
        for feat in featNameList:
            if not feat.isalnum():
                sys.tracebacklimit = 0
                raise ValueError ("ValueError on the following line ({}) in {} file : \n\t{}\n\n <{}> must contain only alphanumeric characters and cannot contain any space character.".format(lineNum,self.mappingFile,line, feat))
            if feat == "Feature":
                sys.tracebacklimit = 0
                raise ValueError ("ValueError on the following line ({}) in {} file : \n\t{}\n\n You cannot use the root of a tree in a mapping.".format(lineNum,self.mappingFile,line))
            if self.featureTree.get(feat) == None:
                sys.tracebacklimit = 0
                raise ValueError ("ValueError on the following line ({}) in {} file : \n\t{}\n\n Feature {} not found in the feature file.".format(lineNum,self.mappingFile,line, feat))
            
        mapping.addEntry(ctxNameList,featNameList)

