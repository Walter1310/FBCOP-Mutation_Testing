"""
    Here we define constraints that will be used to put differents nodes in relation with their parents.

    This is done through an inheritance hierarchy where the super class is @Constraint and each possible
    constraint is a subclass.

    Each constraint is associated with a set of nodes corresponding to all the that are linked to a common
    parent with the same constraint. Therefore, each node will no directl point to its children but to a list
    of constraint encapsulating its children with the same constraint.
"""


class Constraint:

    

    """
        Instance variables:
            @nodeSet : Set object containing @Node objects linked to their parent by the same constraint
    """
    def __init__(self,nodeSet = None):
        """
            Pre :
                <nodeSet> : Set object containing @Node objects. Defined to None if not specified in the constructor
            Post :
                /
        """

        if nodeSet is None:
            self.nodeSet = set()
        else :
            self.nodeSet = nodeSet 

    def __str__ (self):
        """
            Pre :
                /
            Post :
                Return a String representation of the constraint with the following format:
                    (<number of nodes in the set){<name of each node in the set>}
        """
        toReTurn = "({})".format(len(self.nodeSet))+"{"
        for node in self.nodeSet:
            toReTurn += str(node)+ " "
        toReTurn += "}"

        return toReTurn
    
    def __eq__(self, other):
        """
            Pre :
                <other> : Constraint object to compare with the current instance
            Post :
                Returns True if the two @nodeSet are equivalent (contain the same element) and they have the same subclass of @Constraint.
                Return False otherwise
        """
        if type(other) == type(self):
            return self.nodeSet == other.nodeSet
        return False

    def isEmpty (self):
        """
            Pre :  
                /
            Post :
                Returns True if @nodeSet is empty (contains no element)
                Returns False otherwise
        """
        return len(self.nodeSet) == 0



"""
This class represents a Or constraint group. For this constraint to be respected, at least one of its node
must be activated.
"""
class OrConstraint(Constraint):
    """
    Instance variables
        see @Constaint
    """
    def __init__(self, nodeSet=None):
        """
            Pre :
                <nodeSet> : Set object containing @Node objects. Defined to None if not specified in the constructor
            Post :
                /
        """
        super().__init__(nodeSet = nodeSet)

    def __str__(self):
        """
            Pre :
                /
            Post :
                Return a String representation of the constraint with the following format:
                    Or(<number of nodes in the set){<name of each node in the set>}
        """
        return "Or"+ super().__str__()




"""
This class represents a And constraint group. For this constraint to be respected, all of its node
must be activated.
"""
class AndConstraint(Constraint):
    """
    Instance variables
        see @Constaint
    """
    def __init__(self, nodeSet=None):
        """
            Pre :
                <nodeSet> : Set object containing @Node objects. Defined to None if not specified in the constructor
            Post :
                /
        """
        super().__init__(nodeSet = nodeSet)


    def __str__(self):
        """
            Pre :
                /
            Post :
                Return a String representation of the constraint with the following format:
                    And(<number of nodes in the set){<name of each node in the set>}
        """
        return "And"+ super().__str__()




"""
This class represents a Alternative constraint group. For this constraint to be respected, only one of its node
must be activated.
"""
class AlternativeConstraint(Constraint):
    """
    Instance variables
        see @Constaint
    """
    def __init__(self, nodeSet=None):
        """
            Pre :
                <nodeSet> : Set object containing @Node objects. Defined to None if not specified in the constructor
            Post :
                /
        """
        super().__init__(nodeSet = nodeSet)


    def __str__(self):
        """
            Pre :
                /
            Post :
                Return a String representation of the constraint with the following format:
                    Alternative(<number of nodes in the set){<name of each node in the set>}
        """
        return "Alternative"+ super().__str__()


"""
This class represents a Mandatory constraint group. Mandatory constraints are such that they must be activated for the model to be correct.
"""
class MandatoryConstraint(Constraint):
    """
    Instance variables
        see @Constaint
    """
    def __init__(self, nodeSet=None):
        """
            Pre :
                <nodeSet> : Set object containing @Node objects. Defined to None if not specified in the constructor
            Post :
                /
        """
        super().__init__(nodeSet = nodeSet)


    def __str__(self):
        """
            Pre :
                /
            Post :
                Return a String representation of the constraint with the following format:
                    Mandatory(<number of nodes in the set){<name of each node in the set>}
        """
        return "Mandatory"+ super().__str__()



"""
This class represents a Optional constraint group. Optional constraints are such that they can be activated for the model to be correct
"""
class OptionalConstraint(Constraint):
    """
    Instance variables
        see @Constaint
    """
    def __init__(self, nodeSet=None):
        """
            Pre :
                <nodeSet> : Set object containing @Node objects. Defined to None if not specified in the constructor
            Post :
                /
        """
        super().__init__(nodeSet = nodeSet)


    def __str__(self):
        """
            Pre :
                /
            Post :
                Return a String representation of the constraint with the following format:
                    Optional(<number of nodes in the set){<name of each node in the set>}
        """
        return "Optional"+ super().__str__()
