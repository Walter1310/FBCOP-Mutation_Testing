import sys
sys.path.append("..")

from Constraints import *


"""
    This class represent a question that needs to be asked to the user. Each question come from a mutation applied on a @SubModel.
"""

class Question:


    """
        Instance variables :
            @question : String, contains the question that the user will see
            @answer : list of strings containing the correct answers to @question
            @mutant : @SubModel object, mutant associated to the question
            @appliedMutation : @Mutation object, the type of mutation applied to get @mutant
            @ctxNameList : List of strings containing the name of the contexts involved in the question
            @featNameList : List of strings containing the name of the features involved in the question
            @suggestion : Dictionarry containing suggestions for each possible answer for the question
    """

    def __init__(self, question, answer, mutant,appliedMutation,ctxNameList = [],featNameList = []):
        self.question = question
        self.answer = answer
        self.mutant = mutant
        self.appliedMutation = appliedMutation
        self.ctxNameList = ctxNameList
        self.featNameList = featNameList
        self.suggestion = {True : [], False : []}
        self.id = -1

    def applyAnswer(self, proposedAnswer):
        """
            Pre : 
                <proposedAnswer> : string containing the answer by the user
            Post:
                /
        """
        if proposedAnswer in ["yes", "y"]:
                for recom in self.suggestion[True]:
                    if recom not in self.recommendationList:
                        self.recommendationList.append(recom)
        if proposedAnswer in ["no", "n"]:
            for recom in self.suggestion[False]:
                if recom not in self.recommendationList:
                    self.recommendationList.append(recom)

        return proposedAnswer in self.answer
    

    
    def isContextQuestion(self):
        return len(self.ctxNameList)!= 0 and len(self.featNameList) == 0
    
    def isFeatureQuestion(self):
        return len(self.ctxNameList) == 0 and len(self.featNameList) != 0
    
    def isOneSided(self):
        return self.isContextQuestion() or self.isFeatureQuestion()
            
    def isTwoSided(self):
        return (len(self.ctxNameList)!= 0 and len(self.featNameList) != 0)
    
    
    def __str__(self):
        """
            Pre : 
                /
            Post:
                Returns the string representation of the question containing the question string with the answer and the mutation
        """

        toReturn ="("+str(self.id)+")" + self.question + "->" + str(self.answer) + "("+str(self.appliedMutation)+")"
        #toReturn = "********************************\n"+ "("+str(self.appliedMutation)+")"+"\n"+ str(self.ctxNameList) +"\n"+str(self.featNameList)+  "\n********************************"
        #toReturn += "\n"+str(self.mutant) + "\n\n\n"
        return toReturn

    
    