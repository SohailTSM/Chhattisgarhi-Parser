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
                        if len(rhs) == 2 and rhs[0] in T[i][k] and ((rhs[1] in T[k + 1][j])):
                            T[i][j].add(lhs)
                        elif len(rhs) == 1 and rhs[0] in T[i][k]:
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


text = "रामलाल ह अपन मकान के ढलई करत रिहिस"


def main(text):
    try:
        path = str(pathlib.Path(__file__).parent.absolute())
        train_data = indian.tagged_sents(path + '/cg_tagged.txt')
        tnt_pos_tagger = tnt.TnT()
        tnt_pos_tagger.train(train_data)
        tagged_words = (tnt_pos_tagger.tag(nltk.word_tokenize(text)))
        tags = list(map(lambda x: x[1], tagged_words))
        if 'VM' in tags:
            np, vp = tags[: tags.index('VM')], tags[tags.index('VM'):]
        elif 'VAUX' in tags:
            np, vp = tags[: tags.index('VAUX')], tags[tags.index('VAUX'):]
        else:
            np = tags

        tokens = list(text.split(' '))
        tagged_data = {
            tagged_words[0][1]: [[tagged_words[0][0]]]
        }
        print("\n{}\n".format(tagged_words))

        for i in range(1, len(tagged_words)):
            if tagged_words[i][1] in tagged_data:
                tagged_data[tagged_words[i][1]].append([tagged_words[i][0]])
            else:
                tagged_data[tagged_words[i][1]] = [[tagged_words[i][0]]]

        r = {
            'S': [["NP", "VP"]],
            'NP': [np],
        }
        r['NP'] = toCNF(np, 'NP')
        if vp:
            r['VP'] = toCNF(vp, 'VP')

        r.update(tagged_data)
        s = """
        """

        for key, val in r.items():
            st = ""
            st += "{} -> ".format(key)
            for rhs in val:
                st += " ".join(map(lambda x: x if x.isupper()
                                   else "'{}'".format(x), rhs))
                if rhs != val[-1]:
                    st += " | "
            s += "\n{}".format(st)
        grammar = nltk.CFG.fromstring(s)
        parser = nltk.ChartParser(grammar)
        # for tree in parser.parse(tokens):
        #     tree.
        tree = (list(parser.parse(tokens))[0])
        a = tree2dict(tree)
        d = dict2obj(a)
        print(d)
        return cykParse(tokens, r)
    except Exception as e:
        print(e)


def dict2obj(d, key='S', parent=None):

    return {
        'name': key,
        'parent': parent,
        'children': list(map(lambda x: dict2obj(x, list(x.keys())[0], key) if type(x) is dict else {'name': x, 'parent': key}, d[key]))
    }


def tree2dict(tree):
    return {tree.label(): [tree2dict(t) if isinstance(t, nltk.tree.Tree) else t
                           for t in tree]}


print("\n{}\n".format(text))
main(text)
