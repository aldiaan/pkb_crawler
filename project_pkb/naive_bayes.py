import pandas as pd
import argparse
from collections import Counter


def predict_next(word):
    # list word2 yang mungkin
    next_word_list = list(dataset.loc[dataset["word1"] == word, ["word2", "freqs"]].itertuples())    
    prediction_count = {}

    # menghitung masing masing freqs word2
    for next_word in next_word_list:     
        if next_word.word2 in prediction_count:
            prediction_count[next_word.word2] += int(next_word.freqs)
        else:
            prediction_count[next_word.word2] = int(next_word.freqs)
        
    # total freqs
    total_freqs = 0
    for key in prediction_count:
        total_freqs += prediction_count[key]

    dup = prediction_count.copy()
   # naive bayes
   # p(w2|w1) = p(w1|w2) * p(w2)

   

    # p(w2)
    for key in prediction_count:
        prediction_count[key] /= total_freqs

    for key in prediction_count:
        x = 0
        for b in next_word_list:            
            if b.word2 == key:            
                x += int(b.freqs)    
        
        prediction_count[key] *= (x/dup[key])

    # cari yang p(w2|w1) nya maksimum    
    top_5 = Counter(prediction_count).most_common(5)    
    return top_5

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--data', type=str, help='letak dataset level2', metavar='')
x = parser.parse_args()
    
dataset = pd.read_csv(x.data)

while True:
    word1 = input("> masukan kata : ")
    word1 = word1.split()
    word1 = word1[len(word1) - 1]
    # paling kiri mempunyai kemungkinan paling besar
    print('next word prediction :')
    for word2 in predict_next(word1):
        print("    {} with score : {}".format(word2[0], word2[1]))
    print("\n")
    
