f = open("dict/index.noun")
wordsread = (f.read())
splitwords = wordsread.split()
nonumsplitwords = [i for i in splitwords if i.isdigit() == False]
words = [i for i in nonumsplitwords if i.isalpha() == True]
cleanerwords = [i for i in words if i != 'n']

with open('noun_list.txt', 'w') as f:
    for item in cleanerwords:
        f.write("%s\n" % item)