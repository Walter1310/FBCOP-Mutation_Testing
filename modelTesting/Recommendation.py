class Recommendation:
    

    """
        Instance variables :
            @ctxNameList  : List containing names of the contexts that are involved in the recommendation
            @featNameList : List containing names of the features that are involved in the recommendation
            @mutation     : a mutated SubModel object related to the recommendation
    """

    def __init__(self, ctxNameList, featNameList, mutation):
        """
            Pre :
                <ctxNameList> : a list of strings
                <ctxNameList> : a list of strings
                <mutation>    : a SubModel object
            Post :
                /
        """
        self.ctxNameList = ctxNameList
        self.featNameList = featNameList
        self.mutation = mutation

    def showRecomMessages(self):
        """
            Pre :
               /
            Post :
                Create and returns the messsage to show to the user in order to propose modifications to apply on his model
        """
        if self.ctxNameList == [] and self.featNameList != []:
            return "Try to modify the constraint from the following feature(s) :{} with the following mutation : {}".format(self.printNameList(self.featNameList),str(self.mutation))
        elif self.ctxNameList != [] and self.featNameList == []:
            return "Try to modify the constraint from the following context(s) :{} with the following mutation : {}".format(self.printNameList(self.ctxNameList),str(self.mutation))
        elif self.ctxNameList != [] and self.featNameList != []:
            return "Try to modify the constraint from the following context(s) :{}  \n\t\tand the following feature(s) :{} with the following mutation : {}".format(self.printNameList(self.ctxNameList),self.printNameList(self.featNameList),str(self.mutation))

    def printNameList(self,lst):
        """
            Pre :
                <lst> : a list of strings
                
            Post :
                Returns a string in a more readable format lising all the names in <lst>.
        """
        if len(lst) == 1:
            return " " + lst[0]
        
        else :
            toReturn = ""
            for i in range(len(lst)-1):
                toReturn += " "+lst[i]
            return toReturn + " " + lst[-1]
        
    def __str__(self):
        """
            Pre :
                /
            Post :
                Returns the string representation of the current Recommendation. Here it is simple the message showed to the user
        """
        return self.showRecomMessages()
    


    def __eq__(self, other):
        """
            Pre :
                <other> : a Recommendation object
            Post :
                Returns True if the currents Recommendation and <other> have the same string representation.
        """
        return str(self) == str(other)