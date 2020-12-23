# check that db, if supplied, has correct tables (add them if not)
# function that turns novel into tuples of ownership
# function that counts tuples for each possesive 
# and returns word_tallys[]: total objects, total body, total internal, total external, total each area

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

class Ownership:
    def __init__(self, possesive, noun): #, adjective):
        self.possesive = possesive
        self.noun = noun
        # self.adjective = adjective    #leave till next version

def read(user_input, display):
    words = get_words(user_input["Text location"])
    body_parts = get_words("body_parts.txt")
    
    display.variables["Length of text:"].set(len(words)+1)
    display.variables["Words processed:"].set("0")

    ownerships_cnt =0 #records total use of possesive pronouns
    ownerships = []

    for i in range(len(words)):
        
        #modulo is arbitrary, sets gui refresh rate
        if i % 91 == 0 or i == (len(words)-1):
            display.variables["Words processed:"].set(i)
            display.variables["Current word:"].set(words[i])
            display.window.update()
        
        finds_ownerships(words, i, ownerships_cnt, body_parts, ownerships)  # how does this manage to affect the ownerships list?????
    
    found_possesives = find_possesives(ownerships)

def find_possesives(ownerships):

    for i in ownerships:
        print(i.possesive)
    


def finds_ownerships(words, i, ownerships_cnt, body_parts, ownerships):
    if is_possesive(words[i]):
        ownerships_cnt = ownerships_cnt + 1

        if words[i+1] in body_parts:

            ownerships.append(Ownership(words[i], words[i+1]))


def get_words(text_location):
    with io.open(text_location, "r", encoding="utf-8") as file:
        
        #in lower for simplifying later analysis
        text = file.read().lower()
        words = text.split()
    
    file.close()
    return words

def is_possesive(this_word): # this is very simplistic, add named entities
    common_possesives = {"his", "her", "their", "my", "our", "your"}
    if this_word() in common_possesives:
        return True
    else:
        return False