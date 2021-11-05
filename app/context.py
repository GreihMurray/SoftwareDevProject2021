import math
<<<<<<< HEAD
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
=======


class Word:
    def __init__(self, text="", prevW="", midW=""):
        self.text = text
        self.recommend = []
        if text == "":
            self.instances = 0
            self.context = {}
        else:
            self.instances = 1
            self.context = {prevW: {midW: 1}}
>>>>>>> 85486f7 (Development (#33))

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

<<<<<<< HEAD
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
=======
    def addContext(self, prevW, midW):
        if prevW in self.context:
            if midW in self.context[prevW]:
                self.context[prevW][midW] += 1
            else:
                self.context[prevW].update({midW: 1})
        elif self.context:
            self.context.update({prevW: {midW: 1}})
        else:
            self.context = {prevW: {midW: 1}}
        return
>>>>>>> 85486f7 (Development (#33))
