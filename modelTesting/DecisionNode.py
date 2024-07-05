import copy as cp
from CFReader import *
from Constraints import *
from MappingModel import *
from MapReader import *
from Mutations import *
from Node import *
from Questions import *
from SubModel import *
from SubModelsGenerator import *
from Tree import *
from QuestionStore import *
from QStrategies import *
from collections import OrderedDict



class DecisionNode:
    """
    yes = To the left (True)
    no  = To the right (False)
    """


    def __init__(self,questionMask,predictedQuestions = OrderedDict(),questionDict = dict(),depth= 1):

        self.depth = depth

        empty = True
        for pair in questionMask.items():
            empty = empty and pair[1]

        if empty:
            self.isLeaf = True
            self.questionToAsk = "Nil"
            self.depthList = []
            self.predictedQuestions = predictedQuestions
            self.questionDict = questionDict
            self.left = None
            self.right = None
        else :
            
            self.isLeaf = False

            self.questionMask = {"yes" : cp.copy(questionMask),"no" : cp.copy(questionMask)}
            self.questionDict = {"yes" : cp.copy(questionDict), "no" : cp.copy(questionDict)}
            self.predictedQuestions = {"yes" : cp.copy(predictedQuestions),"no" : cp.copy(predictedQuestions)}


            self.questionToAsk = self.pick()

            for key in self.questionDict.keys():
                self.questionDict[key][self.questionToAsk] = key            

            self.propagateYes()
            self.propagateNo()

            self.left = DecisionNode(self.questionMask["yes"],predictedQuestions = self.predictedQuestions["yes"],questionDict=self.questionDict["yes"],depth= self.depth+1)
            self.right = DecisionNode(self.questionMask["no"],predictedQuestions = self.predictedQuestions["no"],questionDict=self.questionDict["no"],depth= self.depth+1)


            if self.left.isLeaf or self.right.isLeaf:
                self.depthList = self.left.depthList+[self.depth]+self.right.depthList
            else :
                self.depthList = self.left.depthList+self.right.depthList

        

    def propagateNo(self):
        for unAskedQuestion in self.questionMask["no"]:
            if self.questionMask["no"][unAskedQuestion]:
                continue
            unAskedCtxSet = set(unAskedQuestion.ctxNameList)
            unAskedFeatSet = set(unAskedQuestion.featNameList)
            for askedQuestion in self.questionDict["no"]:
                if isinstance(askedQuestion,OrToOpt):
                    continue
                askedCtxSet = set(askedQuestion.ctxNameList)
                askedFeatSet = set(askedQuestion.featNameList)
                if unAskedQuestion.isContextQuestion():
                    if askedQuestion.isContextQuestion() and askedCtxSet.issubset(unAskedCtxSet) and self.questionDict["no"][askedQuestion] == "no" :
                        self.applyAnswer( unAskedQuestion,"no")
                        break
                elif unAskedQuestion.isFeatureQuestion():
                    if askedQuestion.isFeatureQuestion() and askedFeatSet.issubset(unAskedFeatSet) and self.questionDict["no"][askedQuestion] == "no":
                        self.applyAnswer( unAskedQuestion,"no")
                        break
                elif unAskedQuestion.isTwoSided():
                    okCtx  = False
                    okFeat = False
                    if askedCtxSet.issubset(unAskedCtxSet) and len(askedCtxSet) !=0 and self.questionDict["no"][askedQuestion] == "no":
                        okCtx = True
                    if askedFeatSet.issubset(unAskedFeatSet) and  len(askedFeatSet) !=0 and self.questionDict["no"][askedQuestion] == "no":
                        okFeat = True
                    if okCtx or okFeat:
                        self.applyAnswer( unAskedQuestion,"no")
                        break
                else:
                    raise Exception("Unknown question type : should be either one sided or two sided!\n\t{}".format(str(unAskedQuestion)))


    def propagateYes(self):
        for unAskedQuestion in self.questionMask["yes"]:
            if self.questionMask["yes"][unAskedQuestion]:
                continue
            unAskedCtxSet = set(unAskedQuestion.ctxNameList)
            unAskedFeatSet = set(unAskedQuestion.featNameList)
            for askedQuestion in self.questionDict["yes"]:
                if isinstance(askedQuestion,OrToOpt):
                    continue
                askedCtxSet = set(askedQuestion.ctxNameList)
                askedFeatSet = set(askedQuestion.featNameList)
                if unAskedQuestion.isContextQuestion():
                    if askedQuestion.isContextQuestion() and unAskedCtxSet.issubset(askedCtxSet) and self.questionDict["yes"][askedQuestion] == "yes":
                        self.applyAnswer( unAskedQuestion,"yes")
                        break
                elif unAskedQuestion.isFeatureQuestion():
                    if askedQuestion.isFeatureQuestion() and unAskedFeatSet.issubset(askedFeatSet) and self.questionDict["yes"][askedQuestion] == "yes":
                        self.applyAnswer( unAskedQuestion,"yes")
                        break
                elif unAskedQuestion.isTwoSided():
                    okCtx  = False
                    okFeat = False
                    if unAskedCtxSet.issubset(askedCtxSet) and self.questionDict["yes"][askedQuestion] == "yes":
                        okCtx = True
                    if unAskedFeatSet.issubset(askedFeatSet) and self.questionDict["yes"][askedQuestion] == "yes":
                        okFeat = True
                    if okCtx and okFeat:
                        self.applyAnswer( unAskedQuestion,"yes")
                        break
                else:
                    raise Exception("Unknown question type : should be either one sided or two sided!\n\t{}".format(str(unAskedQuestion)))

     

    def pick(self):
        for pair in self.questionMask["yes"].items():
            if not pair[1]:
                self.questionMask["yes"][pair[0]] = True
                self.questionMask["no"][pair[0]] = True

                return pair[0]
        return None
        
    def applyAnswer(self, question,answer):
        self.questionMask[answer][question] = True
        self.questionDict[answer][question] = answer
        self.predictedQuestions[answer][question] = answer

    

    def __str__(self):
        if (self.questionToAsk == "Nil"):
            return "Nil"
        toReturn = ""
        toReturn += str(self.questionToAsk.id)+"-" + self.questionToAsk.question + "\n"
        for i in range (self.depth+1):
            toReturn += "\t"
        
        toReturn+=" No> " + str(self.right) + "\n"
        for i in range (self.depth+1):
            toReturn += "\t"
        toReturn += " Yes> "+str(self.left)

        return toReturn

