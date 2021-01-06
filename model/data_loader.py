from torchtext import data
from transformers import AutoTokenizer
import torch


def load_datasets():
    # initialize bert fast (rust) tokenizer from hugging face
    tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased', use_fast=True)

    # pad: [PAD] and unk: [UNK] by default, so convert to indices 
    PAD = tokenizer.convert_tokens_to_ids(tokenizer.pad_token)
    UNK = tokenizer.convert_tokens_to_ids(tokenizer.unk_token)

    # using torchtext to load in dataset
    sentiment = data.Field(sequential=False, 
                       use_vocab=False, 
                       batch_first=True, 
                       dtype=torch.int)

    review = data.Field(use_vocab=False, 
                        tokenize=tokenizer.encode, 
                        include_lengths=False, 
                        batch_first=True, 
                        pad_token=PAD, 
                        unk_token=UNK)

    fields = [
        ('review', review),
        ('sentiment', sentiment)
    ]

    # load training/validation datasets
    train_ds, validate_ds, test_ds = data.TabularDataset.splits(path='./data', 
                                                                train='train.csv', 
                                                                validation='validate.csv', 
                                                                test='test.csv',
                                                                format='csv', 
                                                                fields=fields, 
                                                                skip_header=True)
    
    print("Finished loading datasets.")     # let me know we're still kicking

    return train_ds, validate_ds, test_ds


def get_iterators():
    train_ds, validate_ds, test_ds = load_datasets()

    # work on cpu or gpu (this will run SLOW on cpu)
    device = 'cpu'
    if torch.cuda.is_available():
        device = 'cude:0'

    # training, validation, and testing iterators
    tr_iter, val_iter = data.BucketIterator.splits(datasets=(train_ds, validate_ds),
                                                   sort_key=lambda x: len(x.review), 
                                                   device=device, 
                                                   batch_sizes=(64, 64),
                                                   sort_within_batch=True, 
                                                   repeat=False)

    tst_iter = data.Iterator(test_ds, batch_size=64, device=device, train=False,
                             shuffle=False, sort=False)

    return tr_iter, val_iter, tst_iter