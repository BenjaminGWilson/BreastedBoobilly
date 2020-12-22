# this is a program for taking rough snapshots of gender representation in literary texts
# benjamin wilson, 2020, rhetoricalfigures.co.uk

words = []
noun_dictionary = []
adjective_dictionary = []
ownerships = []


def main():
    load_dictionaries_and_text()
        
    for i in range(len(words)):
        if is_possesive(i) == True:
            make_ownership(i)

class ownership:
    def __init__(self, possesive, noun, adjective):
        self.possesive = possesive
        self.noun = noun
        self.adjective = adjective
        
def load_dictionaries_and_text():
    global words
    file = open("test.txt")
    text = (file.read())
    words = text.split()
    file.close()
    print(words)
    
    global noun_dictionary
    file = open("noun_list.txt")
    text = (file.read())
    noun_dictionary = text.split()
    for i in words:
        i = i.lower
    file.close()

def is_possesive(this_word):
    common_possesives = {"his", "her", "their", "my"}
    if words[this_word].lower() in common_possesives:
        return True
    else:
        return False

def make_ownership(location):
    possesive = words[location]
    noun = identify_noun(location)
    adjective = identify_adjective(location, noun)
    
    test = ownership(possesive, noun, adjective)
    print(test.possesive, test.adjective, test.noun)

def identify_noun(location):
    this_word = words[location+1]
    this_word = this_word.lower()
    
    if '.' in this_word:
        if this_word.strip('.') in noun_dictionary:
            return this_word.strip('.')
        else:
            return None
    
    elif this_word in noun_dictionary:
        return this_word
    
    else:
        return identify_noun(location + 1)

def identify_adjective(location, noun):
    return None

main()