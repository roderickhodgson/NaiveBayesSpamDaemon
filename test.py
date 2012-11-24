from os import listdir, path
import settings
from classifier import NaiveBayesDaemonClassifier as nbc
from nltk.classify import accuracy

def test():
    ham_train = nbc.format_features(path.join(settings.train_dir, settings.ham_dir), 'ham')
    spam_train = nbc.format_features(path.join(settings.train_dir, settings.spam_dir), 'spam')

    training = ham_train[:-len(ham_train)/3]+spam_train[:-len(spam_train)/3]
    test = ham_train[-len(ham_train)/3:]+spam_train[-len(spam_train)/3:]

    nbclassifier = nbc()
    nbclassifier.training = training 
    nbclassifier._init_classifier()

    nbclassifier.classifier.show_most_informative_features(20)

    print "Accuracy: %f" % accuracy(nbclassifier.classifier, test)

if __name__=="__main__":
    test()
