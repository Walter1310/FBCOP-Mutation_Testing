import copy as cp

"""
    This classP provides an encapsulation to use dictionary more easily in the context feature mapping

    When provided a list of features/contexts to MappingModel object sorts that list
    Alphabetically and then used as a key to acces the dictionary.

    Example of usage for the following context-feature mapping where Cx are contexts 
    and Fx are features: 

    C1 -> F1
    C2 -> F2
    C1, C2 -> F3
    C2, C1 -> F4

    The dictionary contains the following pairs of key-value:

    [C1] : [F1]
    [C2] : [F2]
    [C1,C2] : [F3,F4]

    If the caller uses the MappingModel with either [C1,C2] or [C2,C1], the model will return
    [F3,F4]

"""
class MappingModel:

    def __init__(self):
        """
            Pre :
                /
            Post :
                /
        """
        self.dict = {}
        self.__size = 0

    def getSize(self):
        """
            Pre:
                /
            Post :
                Returns an int value representing the number of keys in the dictionary
        """
        return self.__size
    
    def getKeys(self):
        """
            Pre :
                /
            Post :
                Returns a list constaining lists of Strings representing the name of each context nodes used in a relation
        """
        return [list(key) for key in self.dict.keys()]

    def isEmpty(self):
        """
            Pre :
                /
            Post :
                Returns True if the dictionary is empty. False otherwise
        """
        return self.__size == 0

    def addEntry(self,contextNameList,featureNameList):
        """
            Pre: 
                <contextList>  : a List of Strings representing a context name
                <featuresList> : a List of Strings representing features name
            Post : 
                Put all the names in <featuresList> into a Set object and adds an alphabetically sorted version of <contextList> in the
                dictionary (if not present) mapped to all elements of the created Set object.
        """
        contextNameTuple = tuple(sorted(contextNameList))

        if contextNameTuple in self.dict.keys():
            for featureName in featureNameList:
                self.dict[contextNameTuple].add(featureName)
        else :
            self.dict[contextNameTuple] = set(featureNameList)
            self.__size += 1
    
    def getEntry(self,contextNameList):
        """
            Pre :
                <contextNameList> : a List of context names
            Post : 
                Returns the set of feature names associated to <contextNameList>
            Throws:
                @ValueError when <contextList> does not exists as a key in @dict
        """
        contextNameTuple = tuple(sorted(contextNameList))
        if contextNameTuple not in self.dict.keys():
            raise ValueError
        else :
            return self.dict[contextNameTuple]
    
    def copy(self):
        """
            Pre :
                /
            Post : 
                Returns a copy of the current instance.
        """
        newMapModel = MappingModel()
        keyList =[cp.copy(key) for key in self.getKeys()] 
        for key in keyList:
            newMapModel.addEntry(key,cp.copy(self.getEntry(key)))
        return newMapModel

    def __str__(self):
        """
            Pre :
                /
            Post :
                Returns a String representation of the mapping model with the following format for each pair of context,feature:
                    (<all context names>)->{corresponding features}
        """
        keyList = self.getKeys()
        toReturn = ""

        for key in keyList:
            toReturn += str(tuple(key)) + "->" + str(self.getEntry(key))+"\n"

        return toReturn