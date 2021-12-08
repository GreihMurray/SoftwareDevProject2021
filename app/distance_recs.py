def deleteChar(query, words, suggest):
    """
    Function that deletes a character from a word.
    For each character of the query, delete the entry and send to appendSuggest for further word checking.
    query     original user input
    words     set of acceptable words
    suggest   list for appending newWord
    """
    for i in range(len(query)):
        newWord = list(query)
        newWord.pop(i)
        newWord = ''.join(newWord)
        appendSuggest(newWord, words, suggest)

def addChar(query, alpha, words, suggest):
    """
    Function that adds a character to a word.
    For each character position of the query, add each entry from alpha between character entries and send to
    appendSuggest for further word checking.
    query     original user input
    alpha     pre-defined alphabet and symbols
    words     set of acceptable words
    suggest   list for appending newWord
    """
    for i in range(len(query) + 1):
        for c in alpha:
            newWord = list(query)
            newWord.insert(i, c)
            newWord = ''.join(newWord)
            appendSuggest(newWord, words, suggest)

def changeChar(query, alpha, words, suggest):
    """
    Function that changes a character in a word.
    For each character position of the query, change each entry using alpha and send to appendSuggest for further word
    checking.
    query     original user input
    alpha     pre-defined alphabet and symbols
    words     set of acceptable words
    suggest   list for appending newWord
    """
    for i in range(len(query)):
        for c in alpha:
            newWord = list(query)
            newWord[i] = c
            newWord = ''.join(newWord)
            if query[0].isupper() and not query.isupper():
                newWord = newWord.capitalize()
            appendSuggest(newWord, words, suggest)

def switchChar(query, words, suggest):
    """
    Function that switches neighboring characters in a word.
    For each pair of characters in the query, switch the two characters and send to appendSuggest for further word
    checking.
    query     original user input
    alpha     pre-defined alphabet and symbols
    words     set of acceptable words
    suggest   list for appending newWord
    """
    for i in range(len(query)-1):
        newWord = list(query)
        char1 = newWord[i]
        char2 = newWord[i+1]
        newWord[i] = char2
        newWord[i+1] = char1
        newWord = ''.join(newWord)
        if query[0].capitalize and not query.isupper():
            newWord = newWord.capitalize()
        appendSuggest(newWord, words, suggest)

def appendSuggest(newWord, words, suggest):
    """
    Function that appends words similar to a user query to a list.
    If the word can be found in the set of accepted words or the lowercase version can be found there, and it already
    hasn't been added, then add the word to a new list.
    newWord   a new entry being checked
    words     a set of acceptable words
    suggest   a list for appending newWord
    """
    if len(newWord) > 1:
        if (newWord in words or newWord[0].lower()+newWord[1:] in words) and newWord not in suggest:
            suggest.append(newWord)

class LanguageHelper:
    def __init__(self, words, lang):
        """
        Creates a set word list to be referenced.
        words    a file or list of words that are defined as acceptable
        """
        self._words = []
        self._lang = lang
        for w in words.keys():
            self._words.append(w.strip())

    def __contains__(self,query):
        """
        Overrides the "in" conditional to return true or false if in words file from __init__.
        query    user input word
        """
        if query in self._words:
            return True
        else:
            return False

    def getSuggestions(self, query):
        """
        Returns a list of suggestions in response to the user query.
        Depending on the capitalization of the queried word, the suggestion list will return either capitalized or
        lowercase words. The words that are returned also correspond to either being one deleted character, one added
        character, one changed character, or a pair of switched characters away from the original.
        query    user input word
        """
        # Initial Set-Up
        alph_dict = {}
        alph_dict['English'] = "abcdefghijklkmnopqrstuvwxyz'-"
        alph_dict['Irish'] = "briathmósoedcuáfíglnzúépvxjyq-'"
        suggest = []

        # If all uppercase letters...
        if query.isupper():
            alphaU = self._lang.upper()
            deleteChar(query, self._words, suggest)
            addChar(query, alphaU, self._words, suggest)
            changeChar(query, alphaU, self._words, suggest)
            switchChar(query, self._words, suggest)

        # If first letter is uppercase...
        if query[0].isupper() and not query[1:].isupper():
            # remove all cases of capitalization after first letter
            fixed = []
            for q in query[1:]:
                fixed.append(q.lower())
            query = query[0]+''.join(fixed)

            deleteChar(query, self._words, suggest)
            addChar(query, alph_dict[self._lang], self._words, suggest)
            changeChar(query, alph_dict[self._lang], self._words, suggest)
            switchChar(query, self._words, suggest)

        # If all lowercase letters...
        if query.capitalize() in self._words:
            # quick check for uppercase version of word
            appendSuggest(query.capitalize(), self._words, suggest)

        deleteChar(query, self._words, suggest)
        addChar(query, alph_dict[self._lang], self._words, suggest)
        changeChar(query, alph_dict[self._lang], self._words, suggest)
        switchChar(query, self._words, suggest)

        # Sort and return
        suggest.sort()
        return suggest

    def getSuggestionsExtra(self, word):
        """
        Returns a list of suggestions in response to the user query.
        Depending on the capitalization of the queried word, the suggestion list will return either capitalized or
        lowercase words. The words that are returned also correspond to being multiple changes away.
        word    user input word
        """
        # Run the getSuggestions method with the user query
        suggest = self.getSuggestions(word)

        # Run the getSuggestions method again with each of the answers
        # generated from the getSuggestions method
        suggestExtra = []
        for s in suggest:
            answer = self.getSuggestions(s)
            suggestExtra.append(answer)

        # Sort the suggestions
        suggestExtra = sum(suggestExtra,[])
        suggestExtra.sort()

        # Identify all duplicates
        result = []
        for x in suggestExtra:
            if x not in result:
                result.append(x)

        # Return the result
        return result