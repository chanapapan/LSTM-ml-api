import os
import numpy as np
import torch
from torch import nn
from torch.utils.data import Dataset
    
import re, string
from pythainlp.ulmfit import process_thai

LABEL_TO_INT = {'neu':0, 'pos':1, 'neg':2, 'q':3}
INT_TO_LABEL = {v:k for k,v in LABEL_TO_INT.items()}


# https://github.com/PyThaiNLP/wisesight-sentiment/blob/master/kaggle-competition/competition.ipynb
EMOJI = re.compile("["
    u"\U0001F600-\U0001F64F"  # emoticons
    u"\U0001F300-\U0001F5FF"  # symbols & pictographs
    u"\U0001F680-\U0001F6FF"  # transport & map symbols
    u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
    u"\U00002500-\U00002BEF"  # chinese char
    u"\U00002702-\U000027B0"
    u"\U00002702-\U000027B0"
    u"\U000024C2-\U0001F251"
    u"\U0001f926-\U0001f937"
    u"\U00010000-\U0010ffff"
    u"\u2640-\u2642" 
    u"\u2600-\u2B55"
    u"\u200d"
    u"\u23cf"
    u"\u23e9"
    u"\u231a"
    u"\ufe0f"  # dingbats
    u"\u3030"
                  "]+", re.UNICODE)

def replace_url(text):
    URL_PATTERN = r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""
    return re.sub(URL_PATTERN, 'xxurl', text)

def replace_rep(text):
    def _replace_rep(m):
        c,cc = m.groups()
        return f'{c}xxrep'
    re_rep = re.compile(r'(\S)(\1{2,})')
    return re_rep.sub(_replace_rep, text)

def process_text(text):
    #pre rules
    res = text.lower().strip()
    res = replace_url(res)
    res = replace_rep(res)
    
    PUNC  = string.punctuation
    res = ''.join([c for c in text if c not in PUNC])
    
    HASHTAG_PATTERN = r"#[a-zA-Z0-9ก-๙]+"
    res = re.sub(HASHTAG_PATTERN, "", res)
    
    MENTION_PATTERN = r"@[a-zA-Z0-9ก-๙]+"
    res = re.sub(MENTION_PATTERN, "", res)
    
    res = re.sub(EMOJI, "", res)
    
    res = [word for word in process_thai(res) if word and not re.search(pattern=r"\s+", string=word)]

    return res

def get_freer_gpu():
    os.system('nvidia-smi -q -d Memory |grep -A4 GPU|grep Free >gpu_free')
    memory_available = [int(x.split()[2]) for x in open('gpu_free', 'r').readlines()]
    gpu = f'cuda:{np.argmax(memory_available)}'
    if os.path.exists("gpu_free"):
        os.remove("gpu_free")
    else:
          print("The file does not exist") 
    return gpu


class MySentimentModel(nn.Module):
    def __init__(self, config, vocab, INT_TO_LABEL):
        super().__init__()
        self.vocab = vocab
        input_dim = len(self.vocab)
        PAD_IDX   = self.vocab['<pad>']
        
        self.embedding = nn.Embedding(input_dim, config['embed_dim'], padding_idx=PAD_IDX)
        self.lstm = nn.LSTM(input_size   = config['embed_dim'], 
                           hidden_size   = config['hidden_dim'], 
                           num_layers    = config['num_layers'], 
                           bidirectional = config['bidirectional'], 
                           dropout       = config['dropout'],
                           batch_first   = True)
        self.fc = nn.Linear(config['hidden_dim'] * 2, config['output_dim'])
        
    def forward(self, text, text_lengths):
        # text = (batch_size, seq len)
        embedded = self.embedding(text) # (batch_size, seq_len, embed_dim)
        
        # pack the padded sequences
        packed_embedded = nn.utils.rnn.pack_padded_sequence(embedded, text_lengths.to('cpu'), enforce_sorted=False, batch_first=True)

        packed_output, (hn, cn) = self.lstm(packed_embedded)
        
        # concat the final forward (hidden[-2,:,:]) and backward (hidden[-1,:,:]) hidden layers
        hn = torch.cat((hn[-2,:,:], hn[-1,:,:]), dim = 1)
        
        return self.fc(hn)
    
    def predict(self, text:str) -> str:
        text             = self.vocab(process_text(text))
        text             = torch.tensor(text).reshape(1,-1)
        text             = self.embedding(text)
        output, (hn, cn) = self.lstm(text)
        hn               = torch.cat((hn[-2,:,:], hn[-1,:,:]), dim = 1)
        output           = self.fc(hn)
        
        pred_class = torch.argmax(torch.softmax(output, dim=1), dim=1).detach().flatten().cpu().tolist()
        pred_class = [INT_TO_LABEL[pred] for pred in pred_class][0]
        
        return pred_class


    
