import pandas as pd
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--data', type=str, help='data user dalam network', metavar='')
x = parser.parse_args()

csv = pd.read_csv(x.data)

likes_count = {}

for acc in csv.account.unique():
    likes = csv.loc[csv["account"] == acc].likes
    likes_from_this_user = 0
    for like in likes:
        x = str(like).replace(",", "")
        likes_from_this_user += int(x)
    likes_count[acc] = likes_from_this_user

most = 0
most_liked_user = ""

for key in likes_count:
    if most < likes_count[key]:
        most_liked_user = key
        most = likes_count[key]

print("user {} mempunyai likes dengan total {}".format(most_liked_user, most))
