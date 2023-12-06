import torch
import torch.nn as nn
import torch.nn.functional as F

class Word2Vec(nn.Module):
  def __init__(self, embedding_size, vocab_size):
    super(Word2Vec, self).__init__()
    self.target_embeddings = nn.Embedding(vocab_size, embedding_size)
    self.context_embeddings = nn.Embedding(vocab_size, embedding_size)

  def forward(self, target_word, context_word):
    emb_target = self.target_embeddings(target_word)
    emb_context = self.context_embeddings(context_word)
    emb_product = torch.mul(emb_target, emb_context)
    emb_product = torch.sum(emb_product, dim=1)
    output = torch.sum(F.logsigmoid(emb_product))
    return -output


# versão do modelo q considera os exemplos negativos 
class Word2Vec_negative(nn.Module):
  def __init__(self, embedding_size, vocab_size):
    super(Word2Vec_negative, self).__init__()
    self.target_embeddings = nn.Embedding(vocab_size, embedding_size)
    self.context_embeddings = nn.Embedding(vocab_size, embedding_size)

  def forward(self, target_word, context_word, negative_example):
    emb_target = self.target_embeddings(target_word)
    emb_context = self.context_embeddings(context_word)
    emb_product = torch.mul(emb_target, emb_context)
    emb_product = torch.sum(emb_product, dim=1)
    output = torch.sum(F.logsigmoid(emb_product))
    # emb_negative = self.context_embeddings(negative_example)
    # emb_product = torch.bmm(emb_negative, emb_target.unsqueeze(2))
    emb_negative = self.target_embeddings(negative_example)
    emb_product = torch.mul(emb_negative, emb_context)
    emb_product = torch.sum(emb_product, dim=1)
    output += torch.sum(F.logsigmoid(-emb_product))
    return -output






# classe que vai calcular quando precisa parar o processo de aprendizado 
class EarlyStopping():
  def __init__(self, patience=5, min_percent_gain=1):
    self.patience = patience
    self.loss = []
    self.min_percent_gain = min_percent_gain/100.

  def update_loss(self, loss):
    self.loss.append(loss)
    if len(self.loss) > self.patience:
      del self.loss[0]

  def stop_training(self):
    if len(self.loss) == 1:
      return False

    gain = (max(self.loss) - min(self.loss)/max(self.loss))
    print(f"Ganho de custo: {round(100*gain,2)}")
    return gain < self.min_percent_gain