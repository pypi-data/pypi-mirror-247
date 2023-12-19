import os
from Blockporn.scripts import Scripted
#====================================================================

class Blocker:

    def __init__(self, block=None):
        self.cusom = block
        self.block = self.readblock()

#====================================================================

    def cloenlink(self, cleaned):
        emoonsond = cleaned.split("/")
        ouenoined = emoonsond[0]
        return ouenoined

#====================================================================

    def blocker(self, incoming):
        cleaned = self.cleanlink(incoming)
        matterd = self.cloenlink(cleaned)
        for blockers in self.block:
            if matterd == blockers:
                return True
        else:
            return False

#====================================================================
    
    def readblock(self):
        osem_path = os.path.abspath(os.path.dirname(__file__))
        file_path = os.path.join(osem_path, 'RECORDED/blocked.txt')
        with open(file_path, 'r') as filed:
            listed = filed.read().splitlines()
            listed.extend(self.cusom) if self.cusom else listed
            return listed

#====================================================================
    
    def cleanlink(self, incoming):
        if incoming.startswith(Scripted.DATA01):
             finals = incoming.replace(Scripted.DATA01, "", 1)
             return finals
        elif incoming.startswith(Scripted.DATA02):
             finals = incoming.replace(Scripted.DATA02, "", 1)
             return finals
        else:
             return incoming
        
#====================================================================
