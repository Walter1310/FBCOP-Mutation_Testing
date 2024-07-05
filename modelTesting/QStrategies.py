from DecisionNode import *
from collections import OrderedDict


class QuestionStragies :

    def __init__(self,questionStore):
        self.questionStore = questionStore
        self.recommendationList = []
        self.questionDict = dict()

    def applyAskingStrategy(self):
        pass


    def askQuestion(self, question, end = "\nPlease Answer with one of the following : \"yes\", \"y\", \"no\", \"n\"\n>>> "):
        ans = None
        while True:
            ans = input(question + end)
            if ans in ["yes", "y", "no", "n"]:
                break
            else:
                print("\"{}\" is not a valid answer.".format(ans))
        return ans
        

    def separateQuestions(self):
        singleQuestions = []
        doubleQuestions = []
        for question in self.questionStore.store:
            nCtx = len(question.ctxNameList)
            nFeat= len(question.featNameList)
            if (nCtx != 0 and nFeat != 0):
                doubleQuestions.append(question)
            else:
                singleQuestions.append(question)

        return doubleQuestions,singleQuestions
    
    def genRecommendations(self):
        for question in self.questionDict.keys():
            if self.questionDict[question] == "yes":
                for recom in question.suggestion[True]:
                    if recom not in self.recommendationList:
                        self.recommendationList.append(recom)
            if self.questionDict[question] == "no":
                for recom in question.suggestion[False]:
                    if recom not in self.recommendationList:
                        self.recommendationList.append(recom)




class NoOptimizationStrategy(QuestionStragies):

    def __init__(self,questionStore):
        super().__init__(questionStore)
        self.nquestion = len(self.questionStore.store)

    def applyAskingStrategy(self):
        for question in self.questionStore.store:

            ans = self.askQuestion(question.question)
            

            if ans in ["yes", "y"]:
                self.questionDict[question] = "yes"
                #for recom in question.suggestion[True]:
                #    if recom not in self.recommendationList:
                #        self.recommendationList.append(recom)
            if ans in ["no", "n"]:
                self.questionDict[question] = "no"
                #for recom in question.suggestion[False]:
                #    if recom not in self.recommendationList:
                #        self.recommendationList.append(recom)

    
class DecisionTree(QuestionStragies):

    def __init__(self,questionStore) :
        super().__init__(questionStore)

        self.questionList =[]

        for question in questionStore.store:
            if question.isOneSided():
                self.questionList.append(question)

        for question in questionStore.store:
            if question.isTwoSided():
                self.questionList.append(question)

        for i in range(len(self.questionList)):
            self.questionList[i].id = i+1
            print (self.questionList[i]) 
        print("\n")


        self.questionMask = OrderedDict()
        for question in self.questionList:
            self.questionMask[question] = False
        
        self.root = DecisionNode(self.questionMask)
        self.nquestions = self.root.depthList
        print (self.nquestions)
        print (len(self.nquestions))


    def applyAskingStrategy(self):
        node = self.root
        while node.questionToAsk != "Nil":
            ans = self.askQuestion(node.questionToAsk.question)
            if ans in ["yes", "y"]:
                node = node.left
            if ans in ["no", "n"]:
                node  = node.right
        
        self.questionDict = node.questionDict



    def __str__(self):
        return str(self.root)
    

class DecisionTreeBacktrack(QuestionStragies):

    def __init__(self,questionStore) :

        super().__init__(questionStore)

        self.questionList =[]
        

        for question in questionStore.store:
            if question.isOneSided():
                self.questionList.append(question)

        for question in questionStore.store:
            if question.isTwoSided():
                self.questionList.append(question)

        for i in range(len(self.questionList)):
            self.questionList[i].id = i+1
            print (self.questionList[i]) 
        print("\n")


        self.questionMask = OrderedDict()
        for question in self.questionList:
            self.questionMask[question] = False
        
        self.root = DecisionNode(self.questionMask)
        self.nquestions = self.root.depthList
        print (self.nquestions)
        print (len(self.nquestions))


    def applyAskingStrategy(self):
        node = self.root
        while node.questionToAsk != "Nil":
            ans = self.askQuestion(node.questionToAsk.question)            
            if ans in ["yes", "y"]:
                node = node.left
            if ans in ["no", "n"]:
                node  = node.right
        
        self.questionDict = node.questionDict
        self.predictedQuestions = node.predictedQuestions

        if (len(self.predictedQuestions) == 0):
            return

        print("\nBased on your previous answers, we predicted the following answers to these questions:")

        qIndexes = list(self.predictedQuestions.keys())
        for i in range(len(qIndexes)):
            question = qIndexes[i]
            print("("+str(i+1)+")"+question.question + "\n>>> " +self.predictedQuestions[question])

        
        verifQuestion = "\nAre these anwers correct?"
        ans  = self.askQuestion(verifQuestion)
        if ans in ["no", "n"]:
            while True:
                reaskQuestion = "Can you tell us which answers are wrong by writing their number separated by a space? For instance, if questions 1 and 4 are wrong you can write \"1 4\".\n>>>"
                reaskAns = input(reaskQuestion)
                reaskIdx = self.parseIndexes(reaskAns)
                if type(reaskIdx) == list:
                    for index in reaskIdx:
                        q = qIndexes[index-1]
                        if self.questionDict[q] == "yes":
                            self.questionDict[q] = "no"
                        if self.questionDict[q] == "no":
                            self.questionDict[q] = "yes"
                    break
                else : 
                    print (reaskIdx)
        print (self.questionDict)


    def parseIndexes(self, idxStr):
        lst = idxStr.split(" ")
        toReturn = []
        for char in lst:
            if not char.isnumeric():
                return "Error : {} is not a valid number.\n".format(char)
            elif int(char) in toReturn:
                return "Error : {} is present multiple times in your list.\n".format(int(char))
            elif int(char) > len(self.predictedQuestions):
                return "Error : question n°{} does not exist.\n".format(int(char))
            else:
                toReturn.append(int(char))
        
        return toReturn


    def __str__(self):
        return str(self.root)


