# check that db, if supplied, has correct tables (add them if not)
# function that turns novel into tuples of ownership
# function that counts tuples for each possesive
# and returns word_tallys[]: total objects, total body, total internal, total external, total each area

class Word_tally:   #though easier to do this as a dict, allows for more complex class functions in future
    def __init__(self):
        self.total_owned = 0
        self.body_parts = {}    # body part : count

    def total(self):
        print("d")


class Ownership:
    def __init__(self, possesive, noun):  # , adjective):
        self.possesive = possesive
        self.noun = noun
        # self.adjective = adjective    #leave till next version


def read(user_input, display):
    words = get_words(user_input["Text location"])
    body_parts = get_words("body_parts.txt")
    display.variables["Length of text:"].set(len(words)+1)
    display.variables["Words processed:"].set("0")
    ownerships = []

    for i in range(len(words)):
        update_display(i, words, display)
        finds_ownerships(words, i, body_parts, ownerships)

    possesives = find_possesives(ownerships)
    tallies = make_tallies(ownerships, possesives)

    # for i in tallies.keys():
    #     for j in tallies[i].body_parts.keys():
        #    print(i, j, tallies[i].body_parts[j] )

def update_display(i, words, display):
    if i % 91 == 0 or i == (len(words)-1):
        display.variables["Words processed:"].set(i)
        display.variables["Current word:"].set(words[i])
        display.window.update()


def find_possesives(ownerships):

    found_possesives = []
    for i in ownerships:
        if i.possesive not in found_possesives:
            found_possesives.append(i.possesive)

    return found_possesives


def finds_ownerships(words, i, body_parts, ownerships):
    if i == len(words):
        return
    if is_possesive(words[i]):
        if words[i+1] in body_parts:
            ownerships.append(Ownership(words[i], words[i+1]))


def get_words(text_location):

    with open(text_location) as file:

        # in lower for simplifying later analysis
        text = file.read().lower()
        words = text.split()

    file.close()
    return words


def is_possesive(this_word):
    common_possesives = {"his", "her", "their", "my", "our", "your"}
    if this_word in common_possesives:
        return True

    # deals with different encodings
    elif this_word.endswith(("’s", "s’", "\'s", "s\'")):
        return True

    else:
        return False

def make_tallies(ownerships, possesives):
    tallies = dict.fromkeys(possesives)

    for i in tallies:
        tallies[i] = Word_tally()
        tallies[i].body_parts["tits"]=25
        print(i, tallies[i], tallies[i].body_parts)

    for i in ownerships:
        noun = i.noun
        owner = i.possesive
        
        if noun in tallies[owner].body_parts.keys(): 
            tallies[owner].body_parts[noun]+= 1
        else:
            tallies[owner].body_parts[noun] = 1
    
    for i in tallies:
        for j in tallies[i].body_parts:
            print (i, j, tallies[i].body_parts[j])
    
    return tallies


