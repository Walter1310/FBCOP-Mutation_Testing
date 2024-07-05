import sys
sys.path.append("..")

import unittest
from MappingModel import * 

class mappingModelTest(unittest.TestCase):

    def test_example(self):
        C1 = ["C1"]
        C2 = ["C2"]
        C3 = ["C1","C2"]
        C4 = ["C2","C1"]

        F1 = ["F1"]
        F2 = ["F2"]
        F3 = ["F3"]
        F4 = ["F4"]

        m = MappingModel()
        self.assertTrue(m.isEmpty())

        m.addEntry(C1,F1)
        self.assertFalse(m.isEmpty())
        m.addEntry(C2,F2)
        self.assertFalse(m.isEmpty())
        m.addEntry(C3,F3)
        self.assertFalse(m.isEmpty())
        m.addEntry(C4,F4)
        self.assertFalse(m.isEmpty())
        self.assertEqual(m.getSize(),3)

        self.assertEqual(m.getEntry(C3),set(["F3","F4"]))
        self.assertEqual(m.getEntry(C4),set(["F3","F4"]))
        self.assertEqual(m.getEntry(C3),m.getEntry(C4))
        self.assertEqual(m.getEntry(C1),set(F1))
        self.assertEqual(m.getEntry(C2),set(F2))


    def test_empty(self):
        m = MappingModel()

        self.assertEqual(m.getSize(),0)
        self.assertTrue(m.isEmpty())
        with self.assertRaises(ValueError):
            m.getEntry(["Foo"])

    def test_example_Audric(self):
        """
        The example can be found in the master thesis of Audric Deckers
        """ 
        C1 = ["Available"];                  F1 = ["FilterAvailable","Alarm"]
        C2 = ["Busy"];                       F2 = ["Mute"]
        C3 = ["HasMicrophone"];              F3 = ["Vocal"]
        C4 = ["HasCamera"];                  F4 = ["Picture"]
        C5 = ["HasCamera","HighConnection"]; F5 = ["Video"]
        C6 = ["Localization"];               F6 = ["TranslateMessage"]
        C7 = ["Mobile"];                     F7 = ["Simple"]
        C8 = ["Desktop"];                    F8 = ["Complex"]


        m = MappingModel()
        self.assertTrue(m.isEmpty())
        m.addEntry(C1,F1)
        self.assertEqual(m.getSize(),1)
        m.addEntry(C2,F2)
        self.assertEqual(m.getSize(),2)
        m.addEntry(C3,F3)
        self.assertEqual(m.getSize(),3)
        m.addEntry(C4,F4)
        self.assertEqual(m.getSize(),4)
        m.addEntry(C5,F5)
        self.assertEqual(m.getSize(),5)
        m.addEntry(C6,F6)
        self.assertEqual(m.getSize(),6)
        m.addEntry(C7,F7)
        self.assertEqual(m.getSize(),7)
        m.addEntry(C8,F8)
        self.assertEqual(m.getSize(),8)

        self.assertEqual(m.getEntry(C1),set(F1))
        self.assertEqual(m.getEntry(C2),set(F2))
        self.assertEqual(m.getEntry(C3),set(F3))
        self.assertEqual(m.getEntry(C4),set(F4))
        self.assertEqual(m.getEntry(C5),set(F5))
        self.assertEqual(m.getEntry(["HighConnection","HasCamera"]),set(F5))
        self.assertEqual(m.getEntry(C6),set(F6))
        self.assertEqual(m.getEntry(C7),set(F7))
        self.assertEqual(m.getEntry(C8),set(F8))

if __name__ == '__main__':
    unittest.main()