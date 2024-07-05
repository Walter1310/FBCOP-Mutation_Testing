from Recommendation import *

"""
à chaque question créee (= chaque mutant) on appele la fonction add. 
La fonction add regarde d'abord si la question existe déja.
    si oui, on ajoute simplement les recommandations liées à la questions 
    sinon, on ajoute la question

    est-ou sur que la question ne peut pas avoir plusieur fois la même recommandation du coup?
        réponse : ici, on peut avoir plusieur fois la même recommandation dans la liste associée à la question
        mais dans le driver du questionnaire on a une liste globale de recommandations. Si une recommandation est
        déja dans cette liste elle n'est pas ajoutée du coup l'utilisateur ne verra qu'une seule fois cette recom.

    Pourquoi ne pas faire la vérification dés le début pour éviter d'avoir plusieurs fois la même recommandation
    en plusieurs exemplaires pour une questions.
        réponse : une même recom peut venir d'une autre questions du coup on doit obligaoirement faire une verif
        à la fin.
"""

class QuestionStore:
    def __init__(self):
        self.store = []

    def add(self, question):
        recommendation = Recommendation(question.ctxNameList, question.featNameList,question.appliedMutation)
        for askedQuestion in self.store:
            if (question.question == askedQuestion.question):
                # if this question is already in the store, we do not add the question but add a recommandation in the question
                if question.answer == ["yes","y"]:
                    askedQuestion.suggestion[True].append(recommendation)
                if question.answer == ["no","n"]:
                    askedQuestion.suggestion[False].append(recommendation)
                return
        
        if question.answer == ["yes","y"]:
            question.suggestion[True].append(recommendation)
        if question.answer == ["no","n"]:
            question.suggestion[False].append(recommendation)

        self.store.append(question)




    def __len__(self):
        return len(self.store)