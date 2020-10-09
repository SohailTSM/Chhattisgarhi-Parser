import nltk
from nltk.tag import tnt
from nltk.corpus import indian

text = "रामलाल ह अपन मकान के ढलई करत रिहिस"
train_data = indian.tagged_sents('/home/tsm/Minor Project/cg_tagged.txt')
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
print(tagged_data)
