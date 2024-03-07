#Import the libraries
import torch
import torch.nn as nn
import torch.nn.functional as F
import nltk
from torch.utils.data import Dataset
from torch.utils.data import DataLoader


def model_config(model):
    return {
        'model_name': model,
        'train_batch_size': 2,
        'val_batch_size': 2,
        'shuffe': True,
        'learning_rate': 5e-4,
        'epochs': 500,
        'train_steps': 1,
        'val_steps': 1,
        'checkpoint_frequency': 1,
    }

def tokenizer(text, min_occurance):
    tokens = nltk.word_tokenize(text.lower())
    vocab = set(tokens)
    return list(vocab)

def index_corpus(text):
    tokens = tokenizer(text)
    relation_word_index = {token : index for index, token in enumerate(sorted(tokens), 1)}
    relation_word_index['<unk>'] = 0
    return relation_word_index

def convert_word_number(text, relation_word_index):
    return [
        relation_word_index[token] if token in relation_word_index.keys() 
        else relation_word_index['<unk>'] for token in tokenizer(text)
        ]

def skipgram(sentence_batch, relation_word_index, MAX_SEQUENCE_LENGTH, skipgram_context_words):
    input_tensor, output_tensor = [], []

    for text in batch:
        text = text.strip()
        text_token_ids = convert(text, relation_word_index)

        if len(text_token_ids) < skipgram_context_words:
            continue
        
        if len(text_token_ids) > MAX_SEQUENCE_LENGTH:
            text_token_ids = text_token_ids[:MAX_SEQUENCE_LENGTH]
        
        for ids in range(len(text_token_ids)-skipgram_context_words*2)
            sequence = text_token_ids[ids: (ids + skipgram_context_words * 2 + 1)]

            context = sequence.pop(skipgram_context_words)
            target = sequence
        
            for output in target:
                output_tensor.append(output)
                input_tensor.append(context)
    
    target_tensor = torch.tensor(output_tensor, dtype = torch.long)
    context_tensor = torch.tensor(input_tensor, dtype = torch.long)

    return context_tensor, target_tensor

class w2v_Dataset(Dataset):
    def __init__(self, text):
        self.data = text
        self.vocab = tokenizer(self.data)
        self.relation_word_index = index_corpus(self.data)
        self.len = len(self.vocab)
        self.split = self.data.split('\n')
    
    def __getitem__(self, idx):
        return self.split[idx]
    
    def __len__(self):
        return len(self.split)

def dataloader_vocab(text, MAX_SEQUENCE_LENGTH, context, params, vocab= None):
    my_dataset = word2vec_dataset(text_doc)
    data_params = params
    dataloader = DataLoader(my_dataset, collate_fn=lambda x: skipgram(x, my_dataset.relation_word_index, MAX_SEQUENCE_LENGTH, context_words), **data_params)
    if not vocab:
        return dataloader, my_dataset.vocab
    else:
        return dataloader, vocab