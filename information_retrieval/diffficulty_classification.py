
import json
import pandas as pd



# we assume two sentences overlap if they satisified the following contditions: 
# 1) 50% of sent1 overlaps with sent2 
# or 
# 2) 50% of sent2 overlaps with sent1
def isOverlap(input_text, gold_text):
    A = input_text.lower().replace('/n','').strip().split()
    B = gold_text.lower().replace('/n','').strip().split()
    n = len(A)
    m = len(B)
 
    # Auxiliary dp[][] array
    dp = [[0 for i in range(m + 1)] for i in range(n + 1)]
 
    # Updating the dp[][] table
    # in Bottom Up approach
    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1):
 
            # If A[i] is equal to B[i]
            # then dp[j][i] = dp[j + 1][i + 1] + 1
            if A[i] == B[j]:
                dp[i][j] = dp[i + 1][j + 1] + 1
    maxm = 0
    # Find maximum of all the values
    # in dp[][] array to get the
    # maximum length
    for i in dp:
        for j in i:
            # Update the length
            maxm = max(maxm, j)
 

    if maxm/n >= 0.5:
        return True
    elif maxm/m >= 0.5:
        return True
    else:
        return False



# 1.We want to check whether the gold standard contains the curated keywords for the columns. Partition input into easy/hard samples.



#Keywords defined by the GoLab team for each of the 4 columns
keywords_tp = ["target population","beneficiaries", "service users", "participants", "eligible population", "eligibility criteria","cohort","clients"]
keywords_sd = ['study design','method','methodology','data collection','research design']
keywords_fd = ['outcomes payment','price','contract value','contract cap','rate card','incentive payment','costs','savings']
keywords_plo = ['results','outcomes achieved','impact']

keywords = {'Study design':keywords_sd,'Target population':keywords_tp,'Financial detail/costs':keywords_fd,'Person-level outcomes':keywords_plo}
easy_papers = {'Study design':[],'Target population':[],'Financial detail/costs':[],'Person-level outcomes':[]}
hard_papers = {'Study design':[],'Target population':[],'Financial detail/costs':[],'Person-level outcomes':[]}
missing_papers = {'Study design':[],'Target population':[],'Financial detail/costs':[],'Person-level outcomes':[]}


df_gold = pd.read_csv('information_retrieval/IR_theme_gold_standard_paragraphs.tsv',sep='\t',header = 0)


for column in keywords.keys():
    for i,gold_text in enumerate(list(df_gold[column])):
        if isinstance(gold_text,str):
            if any([keyword in gold_text.lower() for keyword in keywords[column]])==False:
                hard_papers[column].append(list(df_gold['Paper'])[i])
            else:
                easy_papers[column].append(list(df_gold['Paper'])[i])
                keyword_frequency = sum([keyword in gold_text.lower() for keyword in keywords[column]])
                print(column,list(df_gold['Paper'])[i],keyword_frequency)
                for keyword in keywords[column]:
                    if keyword in gold_text.lower():
                        print(keyword)

        else:
            missing_papers[column].append(list(df_gold['Paper'])[i])



# 2.Check if the tokenized text contains the gold standard in the appropriate format.


alarms = {'Study design':[],'Target population':[],'Financial detail/costs':[],'Person-level outcomes':[]}


with open('information_retrieval/focused_sample_paragraphs.jsonl','r') as f:
    full_papers = json.load(f)


for column in keywords.keys():
    print(column)
    for i,gold_text in enumerate(list(df_gold[column])):
        if isinstance(gold_text,str):  
            gold_highlights = gold_text.split('//')
            id = list(df_gold['Paper'])[i]
            
            for paper in full_papers:
                if paper['paper_id']==id:
                    break
            paragraphs = paper['paragraphs']
            
            alarm = 0
            for highlight in gold_highlights:
                k = 0
                for paragraph in paragraphs:
                    if highlight in paragraph.replace('\n',' '):
                        k = 1    
                if k == 0:
                    alarm += 1
            if alarm > 0:
                alarms[column].append((id,alarm,len(gold_highlights))) 



print('Alarm',alarms)  



#3 We want to check whether the paragraphs which contain the gold standard also contain the curated keywords for the columns. Partition input in to easy/hard samples.



easy_papers = {'Study design':[],'Target population':[],'Financial detail/costs':[],'Person-level outcomes':[]}
hard_papers = {'Study design':[],'Target population':[],'Financial detail/costs':[],'Person-level outcomes':[]}
missing_papers = {'Study design':[],'Target population':[],'Financial detail/costs':[],'Person-level outcomes':[]}


for column in keywords.keys():
    for i,gold_text in enumerate(list(df_gold[column])):
        if isinstance(gold_text,str):  
            gold_highlights = gold_text.split('//')
            id = list(df_gold['Paper'])[i]
  

            for paper in full_papers:
                if paper['paper_id']==id:
                    break
            paragraphs = paper['paragraphs']
            
            hits = 0
            for highlight in gold_highlights:   
                k = 0
                for paragraph in paragraphs:
                    if isOverlap(highlight,paragraph) == True:
                        k = 1
                        break
               
                if k == 1:
                    print('GOLD:',highlight)
                    print('PARAGRAPH:',paragraph)
                    print()
                    if any([keyword in ' '.join(paragraph.lower().split()) for keyword in keywords[column]])==False:
                        pass
                    else:
                        hits += 1
                                  
                else:
                    print('The gold highlight was not found')  
                    print('GOLD:',highlight) 

            if hits == 0:
                hard_papers[column].append(id)
            else:
                easy_papers[column].append((id,hits,len(gold_highlights)))    
                    
        else:
            missing_papers[column].append(list(df_gold['Paper'])[i])

print(easy_papers)
print(hard_papers)
print(missing_papers)





