import math


class Word:
    def __init__(self, text="", aftW="", midW=""):
        self.text = text
        self.recommend = []
        if text == "":
            self.instances = 0
            self.context = {}
        else:
            self.instances = 1
            self.context = {aftW: {midW: 1}}

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
