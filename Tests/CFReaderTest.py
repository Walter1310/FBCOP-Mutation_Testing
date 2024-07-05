import sys
sys.path.append("..")

from CFReader import *
from Tree import *
from Constraints import *

import unittest

class TestCFReader(unittest.TestCase):

    def test_simple_context(self):
        fileName = "contexts.txt"
        reader = CFReader(fileName)
        ctxtree = reader.readFile()
        self.assertEqual(ctxtree.size,7)

        self.assertNotEqual(ctxtree.get("Context"),None)
        self.assertNotEqual(ctxtree.get("UserAvailability"),None)
        self.assertNotEqual(ctxtree.get("Peripheral"),None)
        self.assertNotEqual(ctxtree.get("Available"),None)
        self.assertNotEqual(ctxtree.get("Busy"),None)
        self.assertNotEqual(ctxtree.get("HasCamera"),None)
        self.assertNotEqual(ctxtree.get("HasMicrophone"),None)

        self.assertEqual(ctxtree.root.name, "Context")
        self.assertEqual(len(ctxtree.root.children),2)

        self.assertEqual(ctxtree.root.children[0][0][0].name,"UserAvailability")
        self.assertEqual(ctxtree.root.children[1][0][0].name,"Peripheral")
        self.assertEqual(len(ctxtree.get("UserAvailability").children),1)
        self.assertEqual(len(ctxtree.get("UserAvailability").children[0][0]),2)
        self.assertEqual(ctxtree.get("UserAvailability").children[0][0][0].name,"Available")
        self.assertEqual(ctxtree.get("UserAvailability").children[0][0][1].name,"Busy")

        self.assertEqual(len(ctxtree.get("Peripheral").children),1)
        self.assertEqual(len(ctxtree.get("Peripheral").children[0][0]),2)
        self.assertEqual(ctxtree.get("Peripheral").children[0][0][0].name,"HasCamera")
        self.assertEqual(ctxtree.get("Peripheral").children[0][0][1].name,"HasMicrophone")


    def test_simple_features(self):
        filename = "features.txt"
        reader = CFReader(filename)

        featTree = reader.readFile()
        self.assertEqual(featTree.size,8)

        self.assertNotEqual(featTree.get("Feature"),None)
        self.assertNotEqual(featTree.get("Mode"),None)
        self.assertNotEqual(featTree.get("MessageType"),None)
        self.assertNotEqual(featTree.get("Alarm"),None)
        self.assertNotEqual(featTree.get("Mute"),None)
        self.assertNotEqual(featTree.get("Picture"),None)
        self.assertNotEqual(featTree.get("Vocal"),None)
        self.assertNotEqual(featTree.get("Text"),None)

        self.assertEqual(featTree.root.name, "Feature")
        self.assertEqual(len(featTree.root.children),1)

        self.assertEqual(len(featTree.root.children[0][0]),2)
        self.assertEqual(featTree.root.children[0][0][0].name,"Mode")
        self.assertEqual(featTree.root.children[0][0][1].name,"MessageType")

        self.assertEqual(len(featTree.get("Mode").children),1)
        self.assertEqual(len(featTree.get("Mode").children[0][0]),2)
        self.assertEqual(featTree.get("Mode").children[0][0][0].name,"Alarm")
        self.assertEqual(featTree.get("Mode").children[0][0][1].name,"Mute")

        self.assertEqual(len(featTree.get("MessageType").children),2)
        self.assertEqual(len(featTree.get("MessageType").children[0][0]),2)
        self.assertEqual(len(featTree.get("MessageType").children[1][0]),1)
        self.assertEqual(featTree.get("MessageType").children[0][0][0].name,"Picture")
        self.assertEqual(featTree.get("MessageType").children[0][0][1].name,"Vocal")
        self.assertEqual(featTree.get("MessageType").children[1][0][0].name,"Text")



if __name__ == "__main__":
    unittest.main()