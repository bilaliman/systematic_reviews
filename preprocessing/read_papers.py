import json
import pandas as pd

from nltk.tokenize import sent_tokenize


with open('full_dataset.json','r',encoding="utf8") as f:
    papers = json.load(f)

print(papers[0].keys())
column_y = pd.read_csv('Column_Y_results.tsv',sep='\t')
covidence = ['#17351','#17330','#17194','#17192','#17150','#2598', '#17271', '#17340']


#column_y['Target population (Y)'] = column_y['Target population (Y)'].apply(lambda x: len(sent_tokenize(x)) if pd.notnull(x) else 0)
column_y['Covidence#'] = column_y['Covidence#'].apply(lambda x: x.strip())

model_inputs = []
for cov in covidence:
    model_input = {}
    print(column_y[column_y['Covidence#']==cov]['Target population (Y)'])
    model_input['target_population'] = list(column_y[column_y['Covidence#']==cov]['Target population (Y)'])[0]
    for paper in papers:
        if paper['Covidence #']==cov:
            model_input['source'] = sent_tokenize(paper['Abstract'])
            model_input['paper_id'] = cov
            model_input['title'] = paper['Title']
            model_input['pdf_txt'] = paper['pdf_txt']
            model_inputs.append(model_input)

'''with open('sample.jsonl','w') as g:
    for model_input in model_inputs:
        json.dump(model_input,g)
        g.write('\n')   '''

with open('sample.jsonl','w') as g:
    json.dump(model_inputs,g)

            

