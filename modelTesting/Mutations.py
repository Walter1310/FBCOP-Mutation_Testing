import sys
sys.path.append("..")

from Constraints import *
from Questions import *


"""
    these classes contain visitors of the visitor design pattern. The chosen dp works as follow : the visited elements are the sub models presviously created and are visited by a function
    of the visitors to see wheter a mutation should apply or not. If this functions returns True, then the mutation is applied.

    The First class is the class @Mutation, this class is the mother class of every possible mutation. It contains a few utilitary methods useful to apply a mutation. It also contains two 
    abstract methods to assert the need of a mutation and to apply a mutation on a @Submodel. 

    Note that all the methods here are static. This allows us to not instanciate each @Mutation if we want to visit a submodel. In order to visit a submodel, we can use the @Mutation class
    with the __subclasses__() built-in class methods that iterates through each one of its subclasses.
"""


class Mutation:

    def findConstraints(subModel,contextNode, featureNode):
        """
            Pre :
                <subModel>    : The @SubModel obect in which we have to find the constraints
                <contextNode> : The @Node object contained in the context @Constraint object that we have to find
                <featureNode> : The @Node object contained in the feature @Constraint object that we have to find
            Post :
                Returns two Constraint objects. One is the constraint that contains <contextNode> and the second one is the constraint that contains <featureNode>.
        """
        
        ctxModel = subModel.findCtxModelFromNode(contextNode)
        featModel = subModel.featModel
        
        ctxConstraint = ctxModel.getConstraintGroup(contextNode)
        featConstraint = featModel.getConstraintGroup(featureNode)

        return ctxConstraint,featConstraint
    
    def applyRegularMutation(targetModel,sourceConst,targetConst):
        """
            Pre :
                <targetModel>    : A @SubModel object representing the model in which we apply the mutation
                <sourceConst>    : A @Constraint object that represent the constraint that we are mutating
                <targetConst>    : A @Constraint object that represent the constraint after the mutation
            Post :
                Returns the same SubModel object as the input but with a mutated constraint. The mutation is performed by removing the <sourceConst> and putting instead the <targetConst> with
                the same Nodes inside.
        """

        targetModelRootNode = targetModel.root
        targetModelRootNode.children.remove(sourceConst)
        targetModel.addConstraintGroup([node.name for node in sourceConst.nodeSet],targetConst,targetModelRootNode.name)
        return targetConst
    
    def genQuestion(ctxModel,ctxConst,featConst,targetConst,expectedAnswer,newSubModel,appliedMutation,context,feature):
        """
            Pre :
                <ctxModel>        : A @Tree object, contains the context model related to the question to create
                <ctxConst>        : A @Constraint object, contains the context constraint related to the question to create
                <featConst>       : A @Constraint object, contains the feature constraint related to the question to create
                <targetConst>     : A @Constraint object, contains the target constraint related to the question to create
                <expectedAnswer>  : A string list, contains all correct answers to the question
                <newSubModel>     : A @Submodel object, the submodel on which the mutation should be applied
                <appliedMutation> : A @Mutation object, the mutation to apply on <newSubModel> 
                <context>         : A boolean value, indicates if the question concerns context nodes or not
                <feature>         : A boolean value, indicates if the question concerns feature nodes or not
            Post :
                Returns a @Question object corresponding to a question that has to be created from a mutation on a submodel.
        """
        
        if (context and feature):
            #context and features
            newConstraint = Mutation.applyRegularMutation(newSubModel.featModel,featConst,targetConst)
            featNodeNameList = [node.name  for node in newConstraint.nodeSet]
            newConstraint = Mutation.applyRegularMutation(ctxModel,ctxConst,type(targetConst)())
            ctxNodeNameList = [node.name  for node in newConstraint.nodeSet]
            
            if type(appliedMutation) == OrToOpt:
                question = "Is it possible for {} contexts and for {} features to be deactivated simultaneously?".format(', '.join(ctxNodeNameList),', '.join(featNodeNameList))
            else :
                question = "Is it possible for {} contexts and for {} features to be activated simultaneously?".format(', '.join(ctxNodeNameList),', '.join(featNodeNameList))

            return Question(question,expectedAnswer,newSubModel,appliedMutation,ctxNameList = ctxNodeNameList,featNameList = featNodeNameList)
        elif (not context and feature):
            #features
            newConstraint = Mutation.applyRegularMutation(newSubModel.featModel,featConst,targetConst)
            nodeNameList = [node.name  for node in newConstraint.nodeSet]

            if type(appliedMutation) == OrToOpt:
                question = "Is it possible for {} and {} features to be deactivated simultaneously?".format(', '.join(nodeNameList[:-1]),nodeNameList[-1])
            else :
                question = "Is it possible for {} and {} features to be activated simultaneously?".format(', '.join(nodeNameList[:-1]),nodeNameList[-1])

            return Question(question,expectedAnswer,newSubModel,appliedMutation,featNameList = nodeNameList)
        elif (context and not feature):
            #context
            newConstraint = Mutation.applyRegularMutation(ctxModel,ctxConst,targetConst)
            nodeNameList = [node.name  for node in newConstraint.nodeSet]

            if type(appliedMutation) == OrToOpt:
                question = "Is it possible for {} and {} contexts to be deactivated simultaneously?".format(', '.join(nodeNameList[:-1]),nodeNameList[-1])
            else :
                question = "Is it possible for {} and {} contexts to be activated simultaneously?".format(', '.join(nodeNameList[:-1]),nodeNameList[-1])

            return Question(question,expectedAnswer,newSubModel,appliedMutation,ctxNameList = nodeNameList)
        else :
            raise ValueError("The mutation has to be applied on a context and/or on a feature")

    def is_applicable(subModel,ctxConstraint, featConstraint):
        """
            Pre :
                <subModel>       : A @SubModel object, represent to submodel to check in which we would like to apply a mutation
                <ctxConstraint>  : A @Constraint object, represent the constraint to check on the context side of <subModel>
                <featConstraint> : A @Constraint object, represent the constraint to check on the feature side of <subModel>
            Post :
                Returns True if the mutation can be appplied on <subModel> based on the type of <ctxConstraint> and <ctxConstraint>
        """
        pass

    def visitSubModel(subModel,ctxConstraint, featConstraint):
        """
            Pre :
                <subModel>       : A @SubModel object, the model in which we will aplly the mutation
                <ctxConstraint>  : A @Constraint object, the constraint that we will mutate
                <featConstraint> : A @Constraint object, the constraint to which we will mutate
            Post :
                Returns a @Question object containing the mutated <subModel> based on the type of <ctxConstraint> and <ctxConstraint>.
                Note : the mutation is made from a copy of <subModel> because we can appy different mutations on the same @SubModel.
            Throws:
                @ValueError if the combination of <ctxConstraint> and <ctxConstraint> does not fit for this mutation
        """
        pass

class OrToAlt(Mutation):

    def __str__(self):
        """
            Pre :
                /
            Post :
                Returns the string representation of the mutation (i.e. the name of the mutation)
        
        """

        return "Or-To-Alt"

    def is_applicable(subModel,ctxConstraint, featConstraint):
        """
        when there is a or in the feature and alt in the ctx ->feature
        when there is a or in the ctx and alt in the feature ->ctx
        when they are both or ->ctx+feature
        when there is a or in the context and a mand or opt in feature ->ctx
        """

        return (isinstance(ctxConstraint,AlternativeConstraint) and isinstance(featConstraint,OrConstraint) ) or \
            (isinstance(ctxConstraint,OrConstraint) and isinstance(featConstraint,AlternativeConstraint)) or\
            (isinstance(ctxConstraint,OrConstraint) and isinstance(featConstraint,OrConstraint))or\
            (isinstance(ctxConstraint,OrConstraint) and (isinstance(featConstraint,MandatoryConstraint) or isinstance(featConstraint,OptionalConstraint)))


    def visitSubModel(subModel,ctxConstraint, featConstraint):
        newSubModel = subModel.copy()
        ctxModel = newSubModel.findCtxModelFromConstraint(ctxConstraint)
        targetConstraint = AlternativeConstraint()
        appliedMutation = OrToAlt()
        feature = False
        context = False
        expectedAnswer = None

        if isinstance(ctxConstraint,AlternativeConstraint) and isinstance(featConstraint,OrConstraint):
            expectedAnswer = ["no","n"]
            feature = True
        
        elif isinstance(ctxConstraint,OrConstraint) and isinstance(featConstraint,AlternativeConstraint):
            expectedAnswer = ["no","n"]
            context = True
        
        elif isinstance(ctxConstraint,OrConstraint) and isinstance(featConstraint,OrConstraint):
            expectedAnswer = ["no","n"]
            feature = True
            context = False
        
        elif isinstance(ctxConstraint,OrConstraint) and (isinstance(featConstraint,MandatoryConstraint) or isinstance(featConstraint,OptionalConstraint)):
            expectedAnswer = ["no","n"]
            context = True
        else :
            raise ValueError("Unknown constraint combination for an Or-To-Alt")
            
        return Mutation.genQuestion(ctxModel,ctxConstraint,featConstraint,targetConstraint,expectedAnswer,newSubModel,appliedMutation,context,feature)
        

class AltToOr(Mutation):

    def __str__(self):
        """
            Pre :
                /
            Post :
                Returns the string representation of the mutation (i.e. the name of the mutation)
        
        """

        return "Alt-To-Or"

    def is_applicable(subModel,ctxConstraint, featConstraint):
        """
        When there is a alt on both sides ->ctx+feature
        When there is a alt in the context and a or in the feature ->ctx
        When there is a alt in the feature and a or in the context ->feature
        when there is a alt in the context and a mand or opt in feature ->ctx
        """
        return (isinstance(ctxConstraint,AlternativeConstraint) and isinstance(featConstraint,AlternativeConstraint)) or\
                (isinstance(ctxConstraint,AlternativeConstraint) and isinstance(featConstraint,OrConstraint)) or\
                (isinstance(ctxConstraint,OrConstraint) and isinstance(featConstraint,AlternativeConstraint)) or\
                (isinstance(ctxConstraint,AlternativeConstraint) and (isinstance(featConstraint,MandatoryConstraint) or isinstance(featConstraint,OptionalConstraint)))

    def visitSubModel(subModel,ctxConstraint, featConstraint):
        newSubModel = subModel.copy()
        ctxModel = newSubModel.findCtxModelFromConstraint(ctxConstraint)
        targetConstraint = OrConstraint()
        appliedMutation = AltToOr()
        feature = False
        context = False
        expectedAnswer = None

        if isinstance(ctxConstraint,AlternativeConstraint) and isinstance(featConstraint,OrConstraint):
            expectedAnswer = ["yes","y"]
            context = True

        elif isinstance(ctxConstraint,OrConstraint) and isinstance(featConstraint,AlternativeConstraint):
            expectedAnswer = ["yes","y"]
            feature = True
            
        elif isinstance(ctxConstraint,AlternativeConstraint) and isinstance(featConstraint,AlternativeConstraint):
            expectedAnswer = ["yes","y"]
            context = True
            feature = True

        elif isinstance(ctxConstraint,AlternativeConstraint) and (isinstance(featConstraint,MandatoryConstraint) or isinstance(featConstraint,OptionalConstraint)):
            expectedAnswer = ["yes","y"]
            context = True
        else :
            raise ValueError("Unknown constraint combination for an Alt-To-Or")

        return Mutation.genQuestion(ctxModel,ctxConstraint,featConstraint,targetConstraint,expectedAnswer,newSubModel,appliedMutation,context,feature)
    
class OrToOpt(Mutation):

    def __str__(self):
        """
            Pre :
                /
            Post :
                Returns the string representation of the mutation (i.e. the name of the mutation)
        
        """
        
        return "Or-To-Opt"

    def is_applicable(subModel,ctxConstraint, featConstraint):
        """
        when they are both or ->ctx+feature
        when there is a or in the context and a mand or opt in feature ->ctx
        """
        return (isinstance(ctxConstraint,OrConstraint) and isinstance(featConstraint,OrConstraint)) or\
                (isinstance(ctxConstraint,OrConstraint) and (isinstance(featConstraint,MandatoryConstraint) or isinstance(featConstraint,OptionalConstraint)))

    def visitSubModel(subModel,ctxConstraint, featConstraint):
        newSubModel = subModel.copy()
        ctxModel = newSubModel.findCtxModelFromConstraint(ctxConstraint)
        targetConstraint = OptionalConstraint()
        appliedMutation = OrToOpt()
        feature = False
        context = False
        expectedAnswer = None

        if isinstance(ctxConstraint,OrConstraint) and isinstance(featConstraint,OrConstraint):
            feature = True
            context = True
            expectedAnswer = ["yes","y"]

        elif isinstance(ctxConstraint,OrConstraint) and (isinstance(featConstraint,MandatoryConstraint) or isinstance(featConstraint,OptionalConstraint)) :
            context = True
            expectedAnswer = ["yes","y"]
        else :
            raise ValueError("Unknown constraint combination for an Or-To-Opt")    
        
        return Mutation.genQuestion(ctxModel,ctxConstraint,featConstraint,targetConstraint,expectedAnswer,newSubModel,appliedMutation,context,feature)


class ManToOpt(Mutation):

    def __str__(self):
        """
            Pre :
                /
            Post :
                Returns the string representation of the mutation (i.e. the name of the mutation)
        
        """
        
        return "Man-To-Opt"

    def is_applicable(subModel,ctxConstraint, featConstraint):
        """
        When there is a mand on the context and a optional in the feature ->ctx
        """

        return isinstance(ctxConstraint,MandatoryConstraint) and isinstance(featConstraint,OptionalConstraint)

    def visitSubModel(subModel,ctxConstraint, featConstraint):
        newSubModel = subModel.copy()
        ctxModel = newSubModel.findCtxModelFromConstraint(ctxConstraint)
        targetConstraint = OptionalConstraint()
        newConstraint = Mutation.applyRegularMutation(ctxModel,ctxConstraint,targetConstraint)
        nodeNameList = [node.name  for node in newConstraint.nodeSet]
        return Question("Does {} have to be activated in any configuration?".format(nodeNameList[0]),["no","n"],newSubModel,ManToOpt(),ctxNameList = nodeNameList)
        
#class OptToMan(Mutation):
#
#    def __str__(self):
#        """
#            Pre :
#                /
#            Post :
#                Returns the string representation of the mutation (i.e. the name of the mutation)
#        
#        """
#        
#        return "Opt-To-Man"

#    def is_applicable(subModel,ctxConstraint, featConstraint):
#        """
#        When there is a mand on the optional and a context in the feature ->ctx
#        """
#        return isinstance(ctxConstraint,OptionalConstraint) 

#    def visitSubModel(subModel,ctxConstraint, featConstraint):
#        newSubModel = subModel.copy()
#        ctxModel = newSubModel.findCtxModelFromConstraint(ctxConstraint)
#        targetConstraint = MandatoryConstraint()
#        newConstraint = Mutation.applyRegularMutation(ctxModel,ctxConstraint,targetConstraint)
#        nodeNameList = [node.name  for node in newConstraint.nodeSet]
#        return Question("Does {} have to be activated in any configuration?".format(nodeNameList[0]),["yes","y"],newSubModel,OptToMan(),ctxNameList = nodeNameList)