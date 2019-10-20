import pandas as pd
import re
import math
import pymongo
import argparse

def normalize_post(text):
	str(text)
	text = text.lower()
	text = re.sub(r"(https://)?www.+\w+", "", text)
	# remove chara like : ®, ©, ™
	text = re.sub(r"[^\x00-\x7F]", " ", text)	
	# remove hashtag
	text = re.sub(r"#\w+", "", text)
	text = re.sub(r"_+", "", text)
	# remove non word like : !, ., <, etc.
	return re.sub(r"[^\w]", " ", text)

def word_counter(posts):
    arr = []
    ret = {}
    for post in posts:
        post = str(post)
        post = normalize_post(post)
        post = post.split()
        for i in range(len(post) - 1):
            arr.append(post[i] + " " + post[i+1])
    for i in range(len(arr)):
        if arr[i] in ret:
            ret[arr[i]] += 1
        else:
            ret[arr[i]] = 1
    return ret

def level2(path, output, host, save_db):	
	if save_db == None:
		save_db = False
	if host == None:
		host = "mongodb://localhost:27017/"

	
	csv1 = path
	c1 = pd.read_csv(csv1)
	c1.drop_duplicates(keep=False, inplace=True)
	# example of word_pairs variable 
	# word_pairs = {
	#     'some text' : 1,
	#     'im here' : 2
	# }

	df = {'uid' : [], 'word1' : [], 'word2' : [], 'freqs' : []}
	for i, id in enumerate(c1.account.unique()):
		
		post_by_this_id = c1.loc[c1['account'] == id].content
		word_pairs = word_counter(post_by_this_id)
		for key in word_pairs:
		    df['uid'].append(i)
		    k = key.split()
		    df['word1'].append(k[0])
		    df['word2'].append(k[1])
		    df['freqs'].append(word_pairs[key])
	gg = pd.DataFrame(df)
	if save_db:
		connection = pymongo.MongoClient(host)
		db = connection["pkb"]
		lvl2 = db["level2"]
		lvl2.insert_many(gg.to_dict('records'))
	else:
		gg.to_csv(output, index=False)

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', type=str, help='letak input file', metavar='')
parser.add_argument('--host', type=str, help='host mongodb', metavar='')
parser.add_argument('-o', '--output', type=str, help='letak output file', metavar='')
parser.add_argument('--save-db', help='save hasil scrap ke database (mongodb)', action='store_true', default=False)
x = parser.parse_args()

level2(x.input, x.output, x.host, x.save_db)

