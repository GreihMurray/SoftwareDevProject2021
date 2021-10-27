import math


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
