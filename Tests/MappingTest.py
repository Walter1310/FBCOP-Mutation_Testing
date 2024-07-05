import sys
sys.path.append("..")

from Tree import Tree
from CFReader import *
from Constraints import *
from MapReader import *
import unittest

class Mappingtest(unittest.TestCase):
    
    def test_simple_mapping(self):
        ctxReader = CFReader("contexts.txt")
        featReader = CFReader("features.txt")
        ctxTree = ctxReader.readFile()
        featTree = featReader.readFile()

        mapReader = MapReader("mapping.txt",ctxTree, featTree)
        mapModel = mapReader.readFile()

        self.assertTrue(not mapModel.isEmpty())
        self.assertEqual(mapModel.getSize(),4)


        self.assertTrue("Alarm" in mapModel.getEntry(["Available"]))
        self.assertTrue("Picture" in mapModel.getEntry(["Available"]))
        self.assertEqual(len(mapModel.getEntry(["Available"])),2)

        self.assertTrue("Mute" in mapModel.getEntry(["Busy"]))
        self.assertEqual(len(mapModel.getEntry(["Busy"])),1)



if __name__ == "__main__":
    unittest.main()