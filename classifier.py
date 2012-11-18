from os import listdir, path
from nltk import NaiveBayesClassifier
from nltk.tokenize import word_tokenize
from nltk.classify import accuracy

import settings

def data_files(dir):
    return [path.join(dir, f) for f in listdir(dir) if f[0]!="."]

def get_word_features(file, string=None):
    if string:
        data = string
    else:
        with open(file, 'r') as f:
            data = f.read()
    words = word_tokenize(data)
    return {word: True for word in words}

def format_features(train_files, label):
    files = data_files(train_files)

    train_features = map(get_word_features, files)
    return [(f, label) for f in train_features]


def is_message_spam(message):
    ham_train = format_features(path.join(settings.train_dir, settings.ham_dir), 'ham')
    spam_train = format_features(path.join(settings.train_dir, settings.spam_dir), 'spam')

    training = ham_train+spam_train

    classifier = NaiveBayesClassifier.train(training)

    return classifier.classify(get_word_features(None, message)) == 'spam'



def test():
    ham_train = format_features(path.join(settings.train_dir, settings.ham_dir), 'ham')
    spam_train = format_features(path.join(settings.train_dir, settings.spam_dir), 'spam')

    training = ham_train[:-len(ham_train)/3]+spam_train[:-len(spam_train)/3]
    test = ham_train[-len(ham_train)/3:]+spam_train[-len(spam_train)/3:]

    classifier = NaiveBayesClassifier.train(training)

    classifier.show_most_informative_features(20)

    print "Accuracy: %f" % accuracy(classifier, test)

if __name__=="__main__":
    test()
