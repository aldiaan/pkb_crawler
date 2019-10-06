import re
import csv

def convert_bytes(num):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0

def save_to_csv(path, datas, mode):        
    if (mode == 'w'):
        with open(path, 'w', encoding='utf-8') as f:                        
            w = csv.DictWriter(f, ["account", "content", "tags", "likes", "comment"])        
            w.writeheader()
            w = csv.writer(f)
            for data in datas:
                row = [data['account'], data['content'], data['tags'], data['likes'], data['comment']]                            
                w.writerow(row)
    if (mode == 'a'):
        with open(path, 'a+', encoding='utf-8') as f:
            writer = csv.writer(f)
            for data in datas:
                row = [data['account'], data['content'], data['tags'], data['likes'], data['comment']]                            
                writer.writerow(row)

def remove_tags(text):
    return re.sub(r"#\w+", '', text)

def words_pair(text):
    text = text.lower()
    result = re.sub(r"[^#\w']", ' ', text).split()
    tags = re.findall(r'#\w+', text)
    result = [x for x in result if x not in tags]    
    words_pair = []
    if len(result) > 1:
        for i in range(len(result) - 1):            
            words_pair.append(result[i] + ' ' + result[i+1])

    return words_pair

def tags_counter(text):
    text = text.lower()

    tags = re.findall(r'#\w+', text)
    
    return tags

