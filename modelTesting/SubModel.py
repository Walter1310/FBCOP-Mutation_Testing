"""
SubModelsGenerator : génère des SubModels objects

input : abres feat/contextes/mapping
output : liste d'objects SubModels

SubModels : -featuModel
                 -contextModel
                 -MappingModel
                 -plus si besoin

générer lec sm sur chaques lignes du mapping, implémenter une fonction __eq__ pour savoir si une sm est générer plusieurs fois en ne pas l'ajouter en double sur la liste
utiliser des sets pour garder les noeuds ensemble dans la sm

On doit pouvoir fusionner les mapping si deux sm on les même arbres (ajouter __eq__ pour les arbres)

"""

# Est ce que je dois fusionner A et B lorsque A est subset de B ou B est subset de A?

class SubModel:

    def __init__(self, featModel, ctxModelList, mapModel):
        #Change here, we use a lsit of ctxModels not just one
        self.ctxModelList = ctxModelList
        self.mapModel = mapModel
        self.featModel = featModel

    def findCtxModelFromNode(self, node):
        for ctxModel in self.ctxModelList:
            if ctxModel.get(node.name) != None:
                return ctxModel
        return None
    
    def findCtxModelFromConstraint(self, constraint):
        for Node in constraint.nodeSet:
            return self.findCtxModelFromNode(Node)
    
    def findCtxNodeFromName(self, nodeName):
        for ctxModel in self.ctxModelList:
            node = ctxModel.get(nodeName)
            if node != None:
                return node
        return None
    
    def __eq__(self,other):
        if not isinstance(other,SubModel):
            return False
        return self.featModel == other.featModel and len(self.ctxModelList) == len(other.ctxModelList) and all([ctxTree in other.ctxModelList for ctxTree in self.ctxModelList])
    
    def __str__(self):
        toReturn = ""
        for ctxModel in self.ctxModelList:
            toReturn += str(ctxModel)
            #toReturn+= '\n'
        
        toReturn+=str(self.mapModel.dict)
        toReturn+= "\n"
        toReturn+= str(self.featModel)
        
        return toReturn
    

    def copy(self):
        newCtxModelList = [ctxModel.copy() for ctxModel in self.ctxModelList]
        newFeatModel = self.featModel.copy()
        newMapModel = self.mapModel.copy()
        return SubModel(newFeatModel,newCtxModelList,newMapModel)
    
    def accept(self,visitor):
        visitor.visitSM(self)



"""
sub model:


Pre-processing : séparer les lignes du mapping qui contiennent plusieurs features.
-Parcourir chaque ligne du mapping
-pour chaque élément à gauche du mapping,
    si la contrainte associée es un mand ou un opt:
        faire un arbre avec uniquement la noeud et son parent
    sinon
        faire un arbre avec son parent et ses frères/soeur
-faire la même chose por l'élément à droite du mapping
-ajouter le mapping au sm créer
-Si un autre sm déjà existant contient EXACTEMENT TOUS ces contexts et features 
    (aka EXACTEMENT mếmes arbres à gauche et même arbre à droite), 
    supprimer le sm en cours de création et rajouter simplement le sous-mapping model
    au mapping model du sm déjà existant.
-Si ce n'est pas le cas, rajouter ce sm aux sms existants.
    
    
idée : ne pas créer de flattenList
for each key in MapModel:
    for each value in mapModel[key]:
        FeatSubTree = createSubModelFromList(key)
        CtxSubTree  = createSubModelFromList(value)
        sm = ConnecteedPair(FeatSubTree,CtxSubTree,MapModel(key,value))
        if there already is a sm with the same trees, only add map to the existing sm
        else add sm


Pre-processing : séparer les lignes du mapping qui contiennent plusieurs features.
-Parcourir chaque ligne du mapping
-Pour chaque ligne, créer un sm qui est un sous-modèle. Ce sous-modèle contient le(s) 
 context(s)+son parent+ses frères/soeurs dans le context model, 
 la feature+son parent+ses frères/soeurs dans le feature model, et cette ligne du mapping
 dans un mapping model. 
-Si un autre sm déjà existant contient EXACTEMENT TOUS ces contexts et features, 
 supprimer le sm en cours de création et rajouter simplement le sous-mapping model 
 au mapping model du sm déjà existant.
-Si ce n'est pas le cas, rajouter ce sm aux sms existants.
        
    
"""