import sys
sys.path.append("..")

from Tree import Tree
from Constraints import *

import unittest

class TreeTest(unittest.TestCase):
    def test_dummy_examples(self):
        tree = Tree("Context")
        
        self.assertEqual(tree.root.name,"Context")
        self.assertEqual(tree.root.parent,None)
        self.assertEqual(tree.root.children,[])
        

        tree.addConstraintGroup(["child1","child2","child3"],OrConstraint(),"Context")
        self.assertEqual(len(tree.root.children), 1)
        self.assertEqual(len(tree.flatList), 4)
        self.assertEqual(len(tree.root.children[0][0]), 3)
        self.assertEqual(tree.root.children[0][0][0].name, "child1")
        self.assertEqual(tree.root.children[0][0][1].name, "child2")
        self.assertEqual(tree.root.children[0][0][2].name, "child3")
        self.assertEqual(tree.get("notFound"),None)



    def test_txt_example1(self):
        tree = Tree("Context")
        tree.addConstraintGroup(["UserAvailability"],MandatoryConstraint(),"Context")
        self.assertEqual(len(tree.root.children), 1)
        self.assertEqual(len(tree.flatList), 2)
        self.assertEqual(len(tree.flatList), tree.size)
        self.assertEqual(len(tree.root.children[0][0]), 1)
        self.assertEqual(tree.root.children[0][0][0].name, "UserAvailability")

        tree.addConstraintGroup(["Peripheral"],OptionalConstraint(),"Context")
        self.assertEqual(len(tree.root.children), 2)
        self.assertEqual(len(tree.flatList), 3)
        self.assertEqual(len(tree.flatList), tree.size)
        self.assertEqual(len(tree.root.children[1][0]), 1)
        self.assertEqual(tree.root.children[1][0][0].name, "Peripheral")

        tree.addConstraintGroup(["Available","Busy"],AlternativeConstraint(),"UserAvailability")
        self.assertEqual(len(tree.flatList), 5)
        self.assertEqual(len(tree.flatList), tree.size)
        self.assertEqual(len(tree.get("UserAvailability").children),1)
        self.assertEqual(len(tree.get("UserAvailability").children[0][0]),2)
        self.assertEqual(tree.get("UserAvailability").children[0][0][0].name,"Available")
        self.assertEqual(tree.get("UserAvailability").children[0][0][1].name,"Busy")

        tree.addConstraintGroup(["HasCamera","HasMicrophone"],OrConstraint(),"Peripheral")
        self.assertEqual(len(tree.flatList), 7)
        self.assertEqual(len(tree.flatList), tree.size)
        self.assertEqual(len(tree.get("Peripheral").children),1)
        self.assertEqual(len(tree.get("Peripheral").children[0]),2)
        self.assertEqual(tree.get("Peripheral").children[0][0][0].name,"HasCamera")
        self.assertEqual(tree.get("Peripheral").children[0][0][1].name,"HasMicrophone")

    def test_txt_example2(self):
        tree = Tree("Feature")

        tree.addConstraintGroup(["Mode","MessageType"],MandatoryConstraint(),"Feature")
        self.assertEqual(len(tree.root.children), 1)
        self.assertEqual(len(tree.flatList), 3)
        self.assertEqual(len(tree.flatList), tree.size)
        self.assertEqual(len(tree.root.children[0][0]), 2)
        self.assertEqual(tree.root.children[0][0][0].name, "Mode")
        self.assertEqual(tree.root.children[0][0][1].name, "MessageType")

        tree.addConstraintGroup(["Alarm","Mute"],AlternativeConstraint(),"Mode")
        self.assertEqual(len(tree.flatList), 5)
        self.assertEqual(len(tree.flatList), tree.size)
        self.assertEqual(len(tree.get("Mode").children),1)
        self.assertEqual(len(tree.get("Mode").children[0][0]),2)
        self.assertEqual(tree.get("Mode").children[0][0][0].name,"Alarm")
        self.assertEqual(tree.get("Mode").children[0][0][1].name,"Mute")

        tree.addConstraintGroup(["Picture","Vocal"],OptionalConstraint(),"MessageType")
        self.assertEqual(len(tree.flatList), 7)
        self.assertEqual(len(tree.flatList), tree.size)
        self.assertEqual(len(tree.get("MessageType").children),1)
        self.assertEqual(len(tree.get("MessageType").children[0]),2)
        self.assertEqual(tree.get("MessageType").children[0][0][0].name,"Picture")
        self.assertEqual(tree.get("MessageType").children[0][0][1].name,"Vocal")
        
        tree.addConstraintGroup(["Text"],MandatoryConstraint(),"MessageType")
        self.assertEqual(len(tree.flatList), 8)
        self.assertEqual(len(tree.flatList), tree.size)
        self.assertEqual(len(tree.get("MessageType").children),2)
        self.assertEqual(len(tree.get("MessageType").children[1][0]),1)
        self.assertEqual(tree.get("MessageType").children[1][0][0].name,"Text")




if __name__ == "__main__":
    unittest.main()