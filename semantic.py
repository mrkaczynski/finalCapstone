import spacy
nlp = spacy.load('en_core_web_md')
word1 = nlp("bird")
word2 = nlp("monkey")
word3 = nlp("banana")
print(word1.similarity(word2))
print(word3.similarity(word2))
print(word3.similarity(word1))

# Cat and monkey have the highest similarity, hypothesis being they are both animals.
# Tested bird inplace of cat and that link remained the highest similarity.

# comparing the two datasets (en_core_web_sm vs en_core_web_md) when running example code.
# the bigger dataset (md) consistenly found higher similarities.
# The warning below would occur when running the smaller dataset en_core_web_sm. Having word vectors allows the program to have 'multi-dimensional meaning representations of a word' and is likely the reason for stronger similarities found. 
# UserWarning: [W007] The model you're using has no word vectors loaded, so the result of the Doc.similarity method will be based on the tagger, parser and NER, which may not give useful similarity judgements. This may happen if you're using one of the small models, e.g. `en_core_web_sm`, which don't ship with word vectors and only use context-sensitive tensors. You can always add your own word vectors, or use one of the larger models instead if available.