import sys
sys.path.append("..")

from CFReader import *
from Constraints import *
from MapReader import *
from SubModel import *
from SubModelsGenerator import *
import unittest

class ConnectedPairsTest(unittest.TestCase):

    def test_simple(self):
        contextFileName = "contexts.txt"
        featureFileName = "features.txt"
        mapFileName = "mapping.txt"
        
        ctxReadr = CFReader(contextFileName)
        featReader = CFReader(featureFileName)

        ctxTree = ctxReadr.readFile()
        featTree  = featReader.readFile()

        mapReader = MapReader(mapFileName, ctxTree,featTree)

        mapModel = mapReader.readFile()
        

        SMGen = SubModelsGenerator(featTree,ctxTree,mapModel)

        SMGen.genSubModelsList()
        SMList = SMGen.subModelList
        self.assertEqual(6, len(SMList))
        testCP = SMList[0]

        self.assertTrue(str(SMList[0]) in ["['UserAvailability', 'Available', 'Busy']\t{('Available',): {'FilterAvailable'}}\t['Feature', 'Mode', 'Receiving', 'Sending', 'MessageType', 'Layout', 'ContactSystem', 'FilterAvailable', 'TranslateMessage']","['UserAvailability', 'Available', 'Busy']\t{('Available',): {'Alarm'}, ('Busy',): {'Mute'}}\t['Mode', 'Alarm', 'Mute']"])
        self.assertTrue(str(SMList[1]) in ["['UserAvailability', 'Available', 'Busy']\t{('Available',): {'FilterAvailable'}}\t['Feature', 'Mode', 'Receiving', 'Sending', 'MessageType', 'Layout', 'ContactSystem', 'FilterAvailable', 'TranslateMessage']","['UserAvailability', 'Available', 'Busy']\t{('Available',): {'Alarm'}, ('Busy',): {'Mute'}}\t['Mode', 'Alarm', 'Mute']"])
        self.assertEqual(str(SMList[2]),"['Peripheral', 'HasMicrophone', 'HasCamera']\t{('HasMicrophone',): {'Vocal'}, ('HasCamera',): {'Picture'}}\t['MessageType', 'Text', 'Vocal', 'Picture', 'Video']")
        self.assertEqual(str(SMList[3]),"['Peripheral', 'HasMicrophone', 'HasCamera']['Context', 'UserAvailability', 'Localization', 'ElectronicDevice', 'Peripheral', 'HighConnection']\t{('HasCamera', 'HighConnection'): {'Video'}}\t['MessageType', 'Text', 'Vocal', 'Picture', 'Video']")
        self.assertEqual(str(SMList[4]),"['Context', 'UserAvailability', 'Localization', 'ElectronicDevice', 'Peripheral', 'HighConnection']\t{('Localization',): {'TranslateMessage'}}\t['Feature', 'Mode', 'Receiving', 'Sending', 'MessageType', 'Layout', 'ContactSystem', 'FilterAvailable', 'TranslateMessage']")
        self.assertEqual(str(SMList[5]),"['ElectronicDevice', 'Mobile', 'Computer']\t{('Mobile',): {'Simple'}, ('Computer',): {'Complex'}}\t['Layout', 'Simple', 'Complex']")



if __name__ == "__main__":
    unittest.main()