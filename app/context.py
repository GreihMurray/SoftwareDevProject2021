import math
import json


class Word:
    def __init__(self, text="", recommend=[], instances=0, context={}):
        self.text = text
        self.recommend = recommend
        if instances == 0 and text != "":
            self.instances = 1
        else:
            self.instances = instances
        self.context = context

    def setText(self, inArg):
        self.text = inArg
        return

    def setInstances(self, inArg):
        self.instances = math.floor(inArg)
        return

    def incrmtInstances(self):
        self.instances += 1
        return

    def addRecommendation(self, word):
        self.recommend.append(word)
        return

    def addContext(self, aftW, midW):
        self.incrmtInstances()
        if aftW in self.context:
            if midW in self.context[aftW]:
                self.context[aftW][midW] += 1
            else:
                self.context[aftW].update({midW: 1})
        elif self.context:
            self.context.update({aftW: {midW: 1}})
        else:
            self.context = {aftW: {midW: 1}}
        return

def loadDictionary(filename):
    f = open(filename)
    text = f.read()
    f.close()

    db_dict = json.loads(text)
    filtDictionary = {}
    for word in db_dict:
        filtDictionary.update({word: Word(**db_dict[word])})
    return filtDictionary