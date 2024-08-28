import pandas as pd
import json

avg_avg = 0
contents = pd.read_csv('information_retrieval/IR_theme_gold_standard_paragraphs.tsv',sep='\t')
for column in contents.columns:
    if 'Paper' in column:
        continue
    
    highlights = [x for x in list(contents[column]) if not pd.isna(x)]
    avg_length = sum([len(highlight.split()) for highlight in highlights])/len(highlights)
    print('Avg length of this field ',column,' : ',avg_length/0.75)
    avg_avg += avg_length/0.75
print(avg_avg/4) 



avg_paragraph = 0
with open('information_retrieval/focused_sample_paragraphs.jsonl') as f:
    papers = json.load(f)

for paper in papers:
    avg_paragraph+=sum([len(x.split())/0.75 for x in paper['paragraphs']])/len(paper['paragraphs'])

print('Avg token length of 5 paragraphs',5*avg_paragraph/len(papers))



