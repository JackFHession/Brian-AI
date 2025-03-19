import torch
import torch.nn as nn

import numpy as np
import nltk
# nltk.download('punkt')
from nltk.stem.porter import PorterStemmer
stemmer = PorterStemmer()

import json

def tokenize(sentence):
    """
    split sentence into array of words/tokens
    a token can be a word or punctuation character, or number
    """
    return nltk.word_tokenize(sentence)


def stem(word):
    """
    stemming = find the root form of the word
    examples:
    words = ["organize", "organizes", "organizing"]
    words = [stem(w) for w in words]
    -> ["organ", "organ", "organ"]
    """
    return stemmer.stem(word.lower())


def bag_of_words(tokenized_sentence, words):
    """
    return bag of words array:
    1 for each known word that exists in the sentence, 0 otherwise
    example:
    sentence = ["hello", "how", "are", "you"]
    words = ["hi", "hello", "I", "you", "bye", "thank", "cool"]
    bog   = [  0 ,    1 ,    0 ,   1 ,    0 ,    0 ,      0]
    """
    # stem each word
    sentence_words = [stem(word) for word in tokenized_sentence]
    # initialize bag with 0 for each word
    bag = np.zeros(len(words), dtype=np.float32)
    for idx, w in enumerate(words):
        if w in sentence_words: 
            bag[idx] = 1

    return bag

class NeuralNet(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(NeuralNet, self).__init__()
        self.l1 = nn.Linear(input_size, hidden_size) 
        self.l2 = nn.Linear(hidden_size, hidden_size) 
        self.l3 = nn.Linear(hidden_size, num_classes)
        self.relu = nn.ReLU()
    
    def forward(self, x):
        out = self.l1(x)
        out = self.relu(out)
        out = self.l2(out)
        out = self.relu(out)
        out = self.l3(out)
        # no activation and no softmax at the end
        return out

class sheil_ai:
    def __init__(self, datapth):

        with open('./ltm/intents.json', 'r') as json_data:
            self.intents = json.load(json_data)

        self.FILE = datapth
        self.data = torch.load(self.FILE)
        self.input_size = self.data["input_size"]
        self.hidden_size = self.data["hidden_size"]
        self.output_size = self.data["output_size"]
        self.all_words = self.data['all_words']
        self.tags = self.data['tags']
        self.model_state = self.data["model_state"]

        self.device = torch.device('cpu')

        self.model = NeuralNet(self.input_size, self.hidden_size, self.output_size).to(self.device)
        self.model.load_state_dict(self.model_state)
        self.model.eval()

    def classify(self, msg):
        sentence = str(msg)
        sentence = tokenize(sentence)
        X = bag_of_words(sentence, self.all_words)
        X = X.reshape(1, X.shape[0])
        X = torch.from_numpy(X).to(self.device)

        output = self.model(X)
        _, predicted = torch.max(output, dim=1)

        tag = self.tags[predicted.item()]

        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]
        if prob.item() > 0.75:
            for intent in self.intents['intents']:
                if tag == intent["tag"]:
                    return intent
        else:
            return False


class IntentClassifier:
    def __init__(self):
        self.ai = sheil_ai("./ltm/data.pth")
    
    def say(self, message):
        return self.ai.classify(message)