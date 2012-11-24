from os import listdir, path
from nltk import NaiveBayesClassifier
from nltk.tokenize import word_tokenize

import settings

class NaiveBayesDaemonClassifier(object):
    @staticmethod
    def data_files(dir):
        return [path.join(dir, f) for f in listdir(dir) if f[0]!="."]

    @staticmethod
    def get_word_features(data):
        words = word_tokenize(data)
        return {word: True for word in words}

    @staticmethod
    def get_word_features_from_file(file):
        with open(file, 'r') as f:
            data = f.read()
        return NaiveBayesDaemonClassifier.get_word_features(data)

    @staticmethod
    def format_features(location, label):
        files = NaiveBayesDaemonClassifier.data_files(location)

        features = map(NaiveBayesDaemonClassifier.get_word_features_from_file, files)
        return [(f, label) for f in features]


    def __init__(self):
        self.classifier = None

    def _init_classifier(self):
        self._prepare_train()
        self.classifier = NaiveBayesClassifier.train(self.training)


    def _prepare_train(self):
        self.ham_train = self.format_features(path.join(settings.train_dir, settings.ham_dir), 'ham')
        self.spam_train = self.format_features(path.join(settings.train_dir, settings.spam_dir), 'spam')

        self.training = self.ham_train+self.spam_train


    def is_message_spam(self, message):
        if self.classifier == None:
            self._init_classifier()
        return self.classifier.classify(get_word_features(message)) == 'spam'

