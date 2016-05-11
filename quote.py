import datetime
import os
import random
import sys
import uuid
import base64
import yaml
import re

import en

PROB = 0

class bnfQuoteDict:
    def __init__(self, file):
        self.grammar = yaml.load(open(file, 'r'))
        self.key = "<quote>"

    def generate(self, key, num):
        gram = self.grammar[key]

        if len(gram) == 1:
            i = 0
        else:
            i = random.randint(0, len(gram) - 1)

        string = ""

        if "<" not in gram[i]:
            string = gram[i]
        else:
            for word in gram[i].split():
                if "<" not in word:
                    string = string + word + " "
                else:
                    if "verb" in word and word != "<adverb>":
                        if "pverb" in word:
                            v = self.generate("<pverb>", 1).strip()
                        elif "nverb" in word:
                            v = self.generate("<nverb>", 1).strip()
                        else:
                            v = self.generate("<theme-verb>", 1).strip()

                        if random.randint(1, 100) < PROB:
                            v = self.generate("<theme-verb>", 1).strip()

                        if "verb-inf" in word:
                            string = string + en.verb.present_participle(v) + " "
                        elif "verb-pr" in word:
                            string = string + en.verb.present(v, person=3,
                                    negate=False) + " "
                        elif "verb-past" in word:
                            string = string + en.verb.past(v) + " "
                        else:
                            string = string + v + " "

                    elif "noun" in word:
                        if "pnoun" in word:
                            v = self.generate("<pnoun>", 1).strip()
                        elif "nnoun" in word:
                            v = self.generate("<nnoun>", 1).strip()
                        else:
                            v = self.generate("<noun>", 1).strip()

                        if random.randint(1, 100) < PROB:
                            v = self.generate("<theme-noun>", 1).strip()

                        if "pl" in word:
                            v = en.noun.plural(v)

                        string = string + v + " "

                    elif "person" in word:
                        v = self.generate("<person>", 1).strip()
                        if "pl" in word:
                            v = en.noun.plural(v)

                        string = string + v + " "

                    elif "adj" in word:
                        v = self.generate("<padj>",1)

                        if random.randint(1, 100) < PROB:
                            v = self.generate("<theme-adj>", 1).strip()

                        string = string + v + " "

                    elif "fruit" in word:
                        v = self.generate("<fruit>", 1).strip()
                        if "pl" in word:
                            v = en.noun.plural(v)

                        string = string + v + " "

                    elif "person" in word:
                        v = self.generate("<fruit>", 1).strip()
                        if "pl" in word:
                            v = en.noun.plural(v)

                        string = string + v + " "

                    else:
                        if "-pl" in word:
                            v = en.noun.plural(self.generate(
                                    word.replace("-pl",""),1))
                        else:
                            v = self.generate(word, 1)

                        string = string + v + " "
        return string

    def generatePretty(self, seed_str):
        random.seed(uuid.uuid5(uuid.NAMESPACE_DNS,seed_str).int)
        puncuation = [".", ".", ".", ".", "!", "?"]
        dontbreaks = ["of", "behind", "the", "when", "what", "why", "who", ",",
                      "your", "by", "like", "to", "you", "your", "a", "are",
                      "become", "newline"]

        quote = self.generate(self.key, 1)
        quote = quote.replace(" ,", ",")
        capitalize = False
        capitalizeNext = True
        breaks = 0

        quote2 = []
        foundFirstBreak = False
        for word in quote.replace("\n", "newline").split():
            quote2.append(word.lower())
            if random.randint(1, 100) < PROB and "newline" not in word and foundFirstBreak:
                isgood = True
                for dontbreak in list(dontbreaks + puncuation):
                    if dontbreak == word.lower():
                        isgood = False
                if isgood:
                    quote2.append("newline")
            if "newline" in word:
                foundFirstBreak = True

        quote3 = []
        beforeFirstBreak = True

        for word in quote2:
            if "newline" in word:
                breaks += 1
                beforeFirstBreak = False
            else:
                breaks = 0

            if word == "i" or "i'" in word:
                word = word.capitalize()
                capitalize = False

            if capitalizeNext:
                word = word.capitalize()

            if word == "." or word == "~" or word == "!":
                capitalizeNext = True
            else:
                capitalizeNext = False

            quote3.append(word)

            if not beforeFirstBreak:
                if breaks > 1:
                    capitalize = True
                if capitalize == True and "newline" not in word:
                    word = word.capitalize()
                    capitalize = False
                for punc in list(set(puncuation)):
                    if punc in word:
                        capitalize = True
                quote3.append(word)
                if random.randint(1, 100) < PROB and "newline" not in word:
                    isgood = True
                    for dontbreak in list(dontbreaks + puncuation):
                        if dontbreak == word.lower():
                            isgood = False
                    if isgood:
                        quote3.append(random.choice(puncuation))
                        capitalize = True

        fullPhrase = " ".join(quote3)

        fullPhrase = fullPhrase.replace(" a a", " an a")
        fullPhrase = fullPhrase.replace("newline .", ". newline")
        fullPhrase = fullPhrase.replace("newline ?", "? newline")
        fullPhrase = fullPhrase.replace("newline !", "! newline")
        fullPhrase = fullPhrase.replace("newline ,", ", newline")
        fullPhrase = fullPhrase.replace("newline", "\n")
        fullPhrase = fullPhrase.replace(" \n \n", "\n\n")
        fullPhrase = fullPhrase.replace("\n \n ", "\n\n")
        fullPhrase = fullPhrase.replace(" '", "'")

        for punc in list(set(puncuation)):
            fullPhrase = fullPhrase.replace(" " + punc, punc)
        for punc in list(set(puncuation)):
            fullPhrase = fullPhrase.replace(" " + punc, punc)
        for punc in list(set(puncuation)):
            fullPhrase = fullPhrase.replace(" " + punc, punc)

        fullPhrase = fullPhrase.replace(" ,", ",")
        fullPhrase = fullPhrase.replace("?.", "?")
        fullPhrase = fullPhrase.replace(".?", ".")
        fullPhrase = fullPhrase.replace(",.", ",")
        fullPhrase = fullPhrase.replace("!.", "!")
        fullPhrase = fullPhrase.replace("..", ".")
        fullPhrase = fullPhrase.replace("..", ".")
        fullPhrase = fullPhrase.replace("..", ".")

        lines = fullPhrase.split("\n")
        return lines[random.randint(0, (len(lines)-1))];

bnf = bnfQuoteDict('cfg.yaml')
