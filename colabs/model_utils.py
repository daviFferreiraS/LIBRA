import torch
import torch.nn as nn
import torch.autograd as autograd
import torch.optim as optim
import torch.nn.functional as F
import numpy as np
import random

'''
Returns batches of tensors with the target word and the context
'''
def get_batches(word_to_index, context, negative = False, batch_size = 100):
  random.shuffle(context)
  batches = []
  batch_target, batch_meaning, batch_negative= [], [], []

  if not negative:
    for i in range(len(context)):

      batch_target.append(word_to_index[context[i][0]])
      batch_meaning.append(word_to_index[context[i][1]])
      if (i+1) % batch_size or i == len(context) - 1:
        tensor_target = autograd.Variable(torch.from_numpy(np.array(batch_target)).long())
        tensor_meaning = autograd.Variable(torch.from_numpy(np.array(batch_meaning)).long())
        batches.append((tensor_target, tensor_meaning))
        batch_target, batch_meaning = [], []



  else:
    for i in range(len(context)):
      batch_target.append(word_to_index[context[i][0]])
      batch_meaning.append(word_to_index[context[i][1]])
      batch_negative.append(word_to_index[context[i][2]])
      
      if (i+1) % batch_size == 0 or i == len(context)-1:
          tensor_target = autograd.Variable(torch.from_numpy(np.array(batch_target)).long())
          tensor_meaning = autograd.Variable(torch.from_numpy(np.array(batch_meaning)).long())
          tensor_negative = autograd.Variable(torch.from_numpy(np.array(batch_negative)).long())
          batches.append((tensor_target, tensor_meaning, tensor_negative))
          batch_target, batch_meaning, batch_negative = [], [], []

  return batches

import itertools
from collections import Counter
from numpy.random import multinomial

def sample_negative(corpus, size):
  probability = {}
  word_counts = dict(Counter(list(itertools.chain.from_iterable(corpus))))
  normalizing_factor = sum([v**0.75 for v in word_counts.values()])

  for word in word_counts:
    probability[word] = word_counts[word]**0.75 / normalizing_factor

  words = np.array(list(word_counts.keys()))

  while True:
    word_list = []
    index = np.array(multinomial(size, list(probability.values())))
    for i, count in enumerate(index):
      for _ in range(count):
        word_list.append(words[i])
    yield word_list
