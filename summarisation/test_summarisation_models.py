import pandas as pd
import transformers

from transformers import pipeline, BartTokenizer, BartForConditionalGeneration


#Load test data using theme "Study Design"

papers = pd.read_csv('summarisation/test_data.tsv',sep='\t')
highlights =list(papers['Highlights extrated from papers relevant to Study Design'])
ids = list(papers['Paper'])
summaries = list(papers['Gold Standard Summary'])
titles = list(papers['Title'])

'''for i,highlight in enumerate(highlights):
    print(titles[i])
    print(summarizer(highlight))
    print()'''

# test off-the-shelf CiteSum model
summarizer = pipeline("summarization", model="yuningm/bart-large-citesum",max_length=40)

# Test fine-tuned CiteSum model
model = BartForConditionalGeneration.from_pretrained("summarisation/Citesum_finetuned_model")
tokenizer = BartTokenizer.from_pretrained("summarisation/Citesum_finetuned_model")

# Test BART model trained on XSum
#model2 = BartForConditionalGeneration.from_pretrained("facebook/bart-large-xsum")
#tokenizer2 = BartTokenizer.from_pretrained("facebook/bart-large-xsum")

avg_length = sum([len(highlight.split()) for highlight in highlights])/len(highlights)
print('Avg length of this field',avg_length/0.75)


for i, highlight in enumerate(highlights):
    input_tokens = tokenizer.batch_encode_plus([highlight],return_tensors='pt',max_length=1024)['input_ids']
    encoded_ids = model.generate(input_tokens,max_length=60,min_length=20,no_repeat_ngram_size=2)
    summary = tokenizer.decode(encoded_ids.squeeze(),skip_special_tokens=True)
    print(ids[i])
    print(summary)
