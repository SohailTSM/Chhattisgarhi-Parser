import nltk
import pathlib
from nltk.tag import tnt
from nltk.corpus import indian

def toCNF(p, key):
    ret = []
    while len(p) > 2:
        ret.append([p[0], key])
        p.pop(0)
    ret.append(p)
    return ret

def cykParse(w, r):
    n = len(w)

    # Initialize the table
    T = [[set([]) for j in range(n)] for i in range(n)]

    # Filling in the table
    for j in range(0, n):

        # Iterate over the rules
        for lhs, rule in r.items():
            for rhs in rule:

                # If a terminal is found
                if len(rhs) == 1 and \
                        rhs[0] == w[j]:
                    T[j][j].add(lhs)

        for i in range(j, -1, -1):

            # Iterate over the range i to j + 1
            for k in range(i, j + 1):

                # Iterate over the rules
                for lhs, rule in r.items():
                    for rhs in rule:

                        # If a terminal is found
                        if len(rhs) == 2 and rhs[0] in T[i][k] and rhs[1] in T[k + 1][j]:
                            T[i][j].add(lhs)

    # If word can be formed by rules
    # of given grammar

    for i in range(n):
        for j in range(n):
            print(T[i][j], end=" ")
        print()

    if len(T[0][n-1]) != 0:
        print("\nYes, the given sentence belongs to CFG")
        return r
    else:
        print("\nNo, the given sentence does not belongs to CFG")
        return "cykError"

text = "हमन राजिम मेला गे रहेन"

def main(text):
    try:
        path = str(pathlib.Path(__file__).parent.absolute())
        train_data = indian.tagged_sents(path + '/cg_tagged.txt')
        tnt_pos_tagger = tnt.TnT()
        tnt_pos_tagger.train(train_data)
        tagged_words = (tnt_pos_tagger.tag(nltk.word_tokenize(text)))
        tags = list(map(lambda x: x[1], tagged_words))
        np, vp = tags[: tags.index('VM')], tags[tags.index('VM'):]
        tokens = list(text.split(' '))
        tagged_data = {
            tagged_words[0][1]: [[tagged_words[0][0]]]
        }

        for i in range(1, len(tagged_words)):
            if tagged_words[i][1] in tagged_data:
                tagged_data[tagged_words[i][1]].append([tagged_words[i][0]])
            else:
                tagged_data[tagged_words[i][1]] = [[tagged_words[i][0]]]

        r = {
            'S': [["NP", "VP"]],
            'NP': [np],
            'VP': [vp],
        }
        r.update(tagged_data)
        r['VP'] = toCNF(vp, 'VP')
        r['NP'] = toCNF(np, 'NP')
        return cykParse(tokens, r)
    except Exception as e:
        return e
    