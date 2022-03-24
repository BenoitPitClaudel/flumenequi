#adapted from huggingface.co guide to Transformer models
import torch
import numpy as np
from transformers import BertForSequenceClassification, AdamW, AutoTokenizer, get_linear_schedule_with_warmup
from nlp import load_dataset

from torchinfo import summary

import time

import horovod.torch as hvd

def main():

    model = BertForSequenceClassification.from_pretrained("bert-large-uncased")
    #put model in train mode
    model.train()

    optimizer = AdamW( model.parameters(), lr=1e-5 )

    #def compute_metrics(pred):
    #    labels = pred.label_ids
    #    preds = pred.predictions.argmax(-1)
    #    precision, recall, f1, _ = precision_recall_fscore_support(labels, preds, average='binary')
    #    acc = accuracy_score(labels, preds)
    #    return {
    #        'accuracy': acc,
    #        'f1': f1,
    #        'precision': precision,
    #        'recall': recall
    #    }

    hvd.init()
    if torch.cuda.is_available():
        dev = "cuda:0"
        torch.cuda.set_device(hvd.local_rank())
    else:
        print("NO GPU - OH DEAR")
        dev = "cpu"
    
    device = torch.device(dev)

    model.to(device)

    optimizer = hvd.DistributedOptimizer(optimizer)

    hvd.broadcast_parameters(model.state_dict(), root_rank=0)
    hvd.broadcast_optimizer_state(optimizer, root_rank=0)


    dataset = load_dataset('imdb', split='train')

    tokenizer = AutoTokenizer.from_pretrained('bert-large-uncased')

    #print(dataset)

    #print(dataset[1])

    dataset = dataset.map(lambda e: tokenizer(e['text'], truncation=True, padding=True), batched=True)
    dataset.rename_column_("label", "labels")
    dataset.set_format(type='torch',columns=['input_ids', 'attention_mask', 'token_type_ids', 'labels'])
    dataloader = torch.utils.data.DataLoader(dataset,batch_size=8)
    print('Data Mapped')
    print(summary(model, input_size=(dataloader.batch_size, 512), dtypes=['torch.cuda.LongTensor']))
    #print(len(dataloader))
    #print(iter(dataloader).next())

    #train_dataset, test_dataset = load_dataset('imdb', split=['train', 'test'])
    #train_dataset = train_dataset.map(tokenize, batched=True, batch_size=32)
    #test_dataset = test_dataset.map(tokenize, batched=True, batch_size=len(train_dataset))
    #train_dataset.set_format('torch', columns=['input_ids', 'attention_mask', 'label'])
    #test_dataset.set_format('torch', columns=['input_ids', 'attention_mask', 'label'])

    #training_args = TrainingArguments(
    #    output_dir='./results',          # output directory
    #    num_train_epochs=3,              # total # of training epochs
    #    per_device_train_batch_size=32,  # batch size per device during training
    #    per_device_eval_batch_size=64,   # batch size for evaluation
    #    warmup_steps=500,                # number of warmup steps for learning rate scheduler
    #    weight_decay=0.01,               # strength of weight decay
    #    logging_dir='./logs',            # directory for storing logs
    #)

    epoch = 0

    #model = torch.nn.DataParallel(model)

    end = time.time()
    data = iter(dataloader)
    #print('Iterator Created')

    batch_time = AverageMeter('Time', ':6.3f')

    progress = ProgressMeter(
        len(dataloader),
        [batch_time],
        prefix="Epoch: [{}]".format(epoch))

    for i in range(len(data)):
        #logging
        sample = data.next()

        #print(sample['labels'], sample['input_ids'])
        
        #train here
        #print('Forward Pass')
        outputs = model(
            input_ids = sample['input_ids'].to(device),
            attention_mask = sample['attention_mask'].to(device), 
            token_type_ids = sample['token_type_ids'].to(device),
            labels = sample['labels'].to(device))
        #print('Loss')
        optimizer.zero_grad()
        loss = outputs.loss
        #print('Backwards Pass')
        loss.backward()
        #print('Optim')
        optimizer.step()

        batch_time.update(time.time() - end)
        end = time.time()
        progress.display(i)



#def tokenize(batch):
#    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
#    return tokenizer(batch['text'], padding=True, truncation=True)

class AverageMeter(object):
    """Computes and stores the average and current value"""
    def __init__(self, name, fmt=':f'):
        self.name = name
        self.fmt = fmt
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count

    def __str__(self):
        fmtstr = '{name} {val' + self.fmt + '} ({avg' + self.fmt + '})'
        return fmtstr.format(**self.__dict__)

class ProgressMeter(object):
    def __init__(self, num_batches, meters, prefix=""):
        self.batch_fmtstr = self._get_batch_fmtstr(num_batches)
        self.meters = meters
        self.prefix = prefix

    def display(self, batch):
        entries = [self.prefix + self.batch_fmtstr.format(batch)]
        entries += [str(meter) for meter in self.meters]
        print('\t'.join(entries))

    def _get_batch_fmtstr(self, num_batches):
        num_digits = len(str(num_batches // 1))
        fmt = '{:' + str(num_digits) + 'd}'
        return '[' + fmt + '/' + fmt.format(num_batches) + ']'

if __name__ == '__main__':
    main()

