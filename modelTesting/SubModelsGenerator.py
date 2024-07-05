from SubModel import *
from MappingModel import *
from Constraints import *
import copy as cp
from Tree import Tree

class SubModelsGenerator:

    def __init__(self,featModel,ctxModel,mapModel):
        self.featModel = featModel
        self.ctxModel = ctxModel
        self.mapModel = mapModel
        self.subModelList = []

    
    def genSubModelsList(self):
        for ctxNameGroup in self.mapModel.getKeys():
            for featName in self.mapModel.getEntry(ctxNameGroup):
                #now we have a list of context and a feature name

                #we devide the contexts in two groups. 
                #The first group is with the nodes puted in a mandatory or optional constraint.
                #   In this group we do not take the parent into account as it is not yet relevant for the tree creation
                #The second group is with the parent name of nodes with any other type of constraint
                #   In the second group we assure that we get only once the name of each parent to not get twice the same tree in the sub model
                mandOptCtxNameList = [ctxName for ctxName in ctxNameGroup if type(self.ctxModel.getConstraintGroupFromName(ctxName)) in [MandatoryConstraint,OptionalConstraint]]
                otherCtxParentName = [self.ctxModel.getParentName(ctxName) for ctxName in ctxNameGroup if type(self.ctxModel.getConstraintGroupFromName(ctxName)) not in [MandatoryConstraint,OptionalConstraint]]
                otherCtxParentName = list(set(otherCtxParentName))

                
                ctxModelList = []

                #Adding context trees for mandOpt nodes
                for mandOptCtxName in mandOptCtxNameList:
                    parentName = self.ctxModel.getParentName(mandOptCtxName)
                    newModel = self.ctxModel.copyNodeWithOneChild(parentName,mandOptCtxName,type(self.ctxModel.getConstraintGroupFromName(mandOptCtxName))())
                    ctxModelList.append(newModel)

                #adding context trees for non other nodes
                for otherCtxParentName in otherCtxParentName:
                    parentNode = self.ctxModel.get(otherCtxParentName)
                    ctxModelList.append(self.createTree(parentNode))


                #Now, we have to do the same for the feature node
                featModel = None
                featConstraint = self.featModel.getConstraintGroupFromName(featName)
                if type(featConstraint) in [MandatoryConstraint,OptionalConstraint]:
                    parentName = self.featModel.getParentName(featName)
                    featModel = self.featModel.copyNodeWithOneChild(parentName,featName,type(featConstraint)())
                else:
                    featModel = self.createTree(self.featModel.getParent(featName))
                    

                
                

                subModel = MappingModel()
                subModel.addEntry(ctxNameGroup,[featName])
                
                currentSubModel = SubModel(featModel,ctxModelList,subModel)
                self.addSM(currentSubModel)




    """
    def genSubModelsList(self):
        for ctxNameGroup in self.mapModel.getKeys():
            for featName in self.mapModel.getEntry(ctxNameGroup):
                
                #need to get the list of parents for each context and make sure 
                #that we only have all unique parents 
                ctxParentListNotUnique = [self.ctxModel.get(ctxName).parent for ctxName in ctxNameGroup if type(self.ctxModel.getConstraintGroup(ctxName)) not in [MandatoryConstraint,OptionalConstraint] ]# add if constraint is not mand or optionals
                ctxParentOptOrMand = [self.ctxModel.get(ctxName).parent for ctxName in ctxNameGroup if type(self.ctxModel.getConstraintGroup(ctxName)) in [MandatoryConstraint,OptionalConstraint] ]

                ctxParentList = []#list containing each parent only once
                for parent in ctxParentListNotUnique:
                    if parent not in ctxParentList:
                        ctxParentList.append(parent)

                ctxTreeList = [self.createTree(parentNode) for parentNode in ctxParentList]
                #create trees for opt and mand then add them to ctxTreeList
                featTree = self.createTree(self.featModel.get(featName).parent) # here we have to act differently if we are in a opt or mand
                subModel = MappingModel()
                subModel.addEntry(ctxNameGroup,[featName])
                
                currentSubModel = SubModel(featTree,ctxTreeList,subModel)
                self.addSM(currentSubModel)
    """
                
    def createTree(self, parentNode):
        #creat a copy of a node and its children
        tree = Tree(parentNode.name)

        for child in parentNode.children:
            nodeSet = child.nodeSet
            nameList = [cp.copy(n.name) for n in nodeSet]
            contsraintCopy = type(child)
            tree.addConstraintGroup(nameList,contsraintCopy(),tree.root.name)
        return tree


    def addSM(self,subMod):
        for subModel in self.subModelList:
            if subModel == subMod:
                for key in subMod.mapModel.getKeys():
                    subModel.mapModel.addEntry(key,subMod.mapModel.getEntry(key))
                return
        self.subModelList.append(subMod)
        


    

"""
Prendre toute la liste de CPs existants. Pour chaque mutant qui existe, vérifier l'applicabilité (checkApplicability ou qqchose comme ça) de chaque CPAppliquer les mutations sur les CPs applicables
Modifié​[11/12 13:54] Pierre Martou
    Chaque mutant contient deux fonctions:
checkApplicability(CP) -> True/False)
applyMutation(CP) ->  mutatedCP
Modifié​[11/12 13:56] Pierre Martou
    (implement Visitor pattern to traverse CPs ?)
"""    
