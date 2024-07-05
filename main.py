import sys
sys.path.append("modelTesting")

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
from DecisionNode import *

"""
inconcistencies :

3
7

4 :
pas de questions
"""

name = "/test7"

#print ("================Building Context model================")
ctxFileName = "modelFiles"+name+"/contexts.txt"
ctxReader = CFReader(ctxFileName)
ctxTree = ctxReader.readFile()
#print (ctxTree)


#print ("================Building Feature model================")
featFileName = "modelFiles"+name+"/features.txt"
featReader = CFReader(featFileName)
featTree = featReader.readFile()
#print (featTree)


#print ("================Building Mapping model================")
mapReader = MapReader("modelFiles"+name+"/mapping.txt",ctxTree, featTree)
mapModel = mapReader.readFile()
#print(mapModel)


#print ("=================Generating submodels=================")
subModelGen = SubModelsGenerator(featTree,ctxTree,mapModel)
subModelGen.genSubModelsList()
subModelList = subModelGen.subModelList
#for subModel in subModelList:
#    print(subModel)
print ("{} submodel(s) generated.".format(len(subModelList)))

questionStore = QuestionStore()
nMutants = 0

#start the static svisitor design pattern to generate mutants
#print ("=================Generating mutations=================")
for subModel in subModelList:
    #print(subModel)
    mapModel = subModel.mapModel
    featModel = subModel.featModel
    for ctxModel in subModel.ctxModelList:
        for ctxConstraint in ctxModel.root.children:
            for featConstraint in featModel.root.children:
                for mutation in Mutation.__subclasses__():
                    if mutation.is_applicable(subModel,ctxConstraint,featConstraint):
                        #print(str(mutation) + "->" + str(ctxConstraint)+","+str(featConstraint))
                        askedQuestion = mutation.visitSubModel(subModel,ctxConstraint,featConstraint)
                        nMutants += 1
                        #print (askedQuestion)
                        #print (subModel)
                        questionStore.add(askedQuestion)
    #print("***************************************")

print ("{} mutation(s) generated.".format(nMutants))
print ("{} question(s) to ask.".format(len(questionStore)))

#print ("==================Generated Questions=================")
for askedQuestion in questionStore.store:
    print (askedQuestion)



#decTree = DecisionTree(questionList)
#print (decTree)
#starting the questionnaire
    

unconsistentQuestions  = []
for askedQuestion in questionStore.store:
    if len(askedQuestion.suggestion[True]) > 0 and len(askedQuestion.suggestion[False]) >0:
        unconsistentQuestions.append(askedQuestion.question)


if len( unconsistentQuestions ) > 0:
    raise ValueError("Yes and No possible for the follwing questions :\n\t{}\nShould not be the case!!!!".format("\n\t".join(unconsistentQuestions)))
else:    
    print ("No inconsistencies")


strategyDict = {1 : NoOptimizationStrategy, 2 : DecisionTree(questionStore), 3: DecisionTreeBacktrack}

questionStrategy = None
while True:
    strategyNumber = input ("Which strategy do you want? Please enter the corresponding number.\n1. No optimization strategy\n2. Decision tree strategy\n3. Decision tree strategy with backtracking\n>>> ")
    if not strategyNumber.isnumeric():
        print ("invalid value")
        continue
    elif not int(strategyNumber) in strategyDict.keys():
        print("value not found")
        continue
    else:
        questionStrategy = strategyDict[int(strategyNumber)](questionStore)
        break

print (questionStrategy)
questionStrategy.applyAskingStrategy()
questionDict = questionStrategy.questionDict
#print (questionStrategy.questionDict)
#print (len(questionStrategy.questionDict))
questionStrategy.genRecommendations()


if (len(questionStrategy.recommendationList) == 0):
    print ("No recommendation needed :-)")
else :
    print("\nThere might be some errors in the model. Here is a list of recommendations that could fix them.")
    for recom in questionStrategy.recommendationList:
        print ("\t",recom)
    



"""
What to do now:
    - merge questions.
            - for each questions, we need a set of suggestions related to the answer of the user
                -> dictionary (yes or no) -> list of suggestions
    - instead of a simple list of questions, try to encapsulate it into a new kind of
      list that will take into account each different Question object
        - when we wan to add a question object, we check if the string in already there
        -if it is already presend, we put the usggestion in its dictionary
        -if not we add the question to the list and set up its dictionay

    The name of the enacapsulation could be 'QuestionStore' and contains a list or a set
    Each element of the store would be a new type of object called 'AskedQuestion'
"""


"""
Bug sur les questions qui fait qu'on peu avoir des cas ou on a oui et non dans les questions
-Bug résolu, il s'agissait d'une mutation AltTorOr qui se faisait dans la classe OrToOpt 
-On a donc des mutations qui ont du sens mais cela ne nous empêche pas d'avoir du oui et du non pour certaines questions.
-Dans le cas testé, on a plusieurs cas ou on a alternativemetn du OrToAlt et du OrToOpt surs les même contextes. 
    cela implique que deux mutations différentes sont faites sur les contextes et donc comme la réponse dépend de la mutation
    on peut avoir pour la même question plusieurs réponses contradictoires possible.
    ici on est dans un OrToAlt et un OrToOpt avec un or à droite et un opt à droite
-En vérifiant ce qui a été fait sur le code d'Audric, on se rend compte que le problème vient des requirements
    du programme directement
-J'ai supprimé les conditions dans les checks au niveau des mutations, les cas ou on a mand/opt à droite.
    Cela supprime les bugs apparent mais on a certains cas ou il n'y a pas de mutation à faire. (cf test4)
"""
