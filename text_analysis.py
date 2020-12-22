#define Word_tally class for returning final counts
# receive user input + tkvariable for updating display (maybe 2, one that 
# can be the words being processed?)
# check that db, if supplied, has correct tables (add them if not)
# load and test dictionaries
# function that turns novel into tuples of ownership
# function that counts tuples for each possesive 
# and returns word_tallys[]: total objects, total body, total internal, total external, total each area

import time  #for testing, delete
import io # used to open non-unicode files
class Word_tally:
    def __init__(self):
        self.total_owned = 0
        self.total_body = 0
        self.internal = 0
        self.feet = 0
        self.legs = 0
        self.hands = 0
        self.arms = 0
        self.nethers = 0
        self.torso = 0
        self.head = 0
        self.other = 0
    
    def total(self):
        self.total_body = (
        self.internal
        + self.feet
        + self.legs
        + self.hands
        + self.arms
        + self.nethers
        + self.torso
        + self.head
        + self.other 
        )

class ownership:
    def __init__(self, possesive, noun, adjective):
        self.possesive = possesive
        self.noun = noun
        self.adjective = adjective

def read(user_input, display):
    words = get_words(user_input["Text location"])
    #body_parts = get_words("body_parts.txt")
    
    display.variables["Length of text:"].set(len(words))
    display.variables["Words processed:"].set("0")


    for i in range(len(words)):
        if i % 45 == 0:
            display.variables["Words processed:"].set(i)
            display.variables["Current word:"].set(words[i])
            display.window.update()
        print(words[i])


def get_words(text_location):
    with io.open(text_location, "r", encoding="utf-8") as file:
        text = (file.read())
        words = text.split()
    file.close()
    return words

