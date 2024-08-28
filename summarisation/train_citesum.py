import json
import os

from transformers import BartForConditionalGeneration, AutoModel, AutoTokenizer, DataCollatorForSeq2Seq,BartTokenizer 
from transformers import Trainer, TrainingArguments
from sentence_transformers import SentenceTransformer, util
from datasets import load_dataset



def pp_text(text):
    text = text.replace('\n',' ').replace('\t',' ').replace('//','')
    text = text.lower()
    return text


def preprocess_function(examples):
    inputs = pp_text(examples["Input"])
    model_inputs = tokenizer(inputs, max_length=1024, truncation=True)
    labels = tokenizer(examples["Study design summary"], max_length=128, truncation=True)
    model_inputs["labels"] = labels["input_ids"]
    return model_inputs





#____Train CiteSum model_____
dir_path = 'summarisation'
model = BartForConditionalGeneration.from_pretrained("yuningm/bart-large-citesum")
tokenizer = BartTokenizer.from_pretrained("yuningm/bart-large-citesum")

training_args = TrainingArguments(
    output_dir= os.path.join(dir_path,'Citesum_finetuned_model'),          # output directory
    num_train_epochs=20,              # total number of training epochs
    per_device_train_batch_size=1,  # batch size per device during training
    per_device_eval_batch_size=1,   # batch size for evaluation
    warmup_steps=500,                # number of warmup steps for learning rate scheduler
    weight_decay=0.01,               # strength of weight decay
    logging_dir= os.path.join(dir_path,'BART_model/logs'),            # directory for storing logs
    logging_steps=10,
)


datafiles ='summarisation/train_data.csv'
dataset = load_dataset('csv', data_files=datafiles, split='train')
tokenized_dataset = dataset.map(preprocess_function,batched=False)




data_collator = DataCollatorForSeq2Seq(tokenizer=tokenizer, model=model)

trainer = Trainer(
    model=model,                         # the instantiated Transformers model to be trained
    args=training_args,                  # training arguments, defined above
    train_dataset=tokenized_dataset,         # training dataset
    tokenizer = tokenizer,
    data_collator=data_collator,
)

trainer.train()
trainer.save_state()
trainer.save_model()
