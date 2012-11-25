from os import listdir, path
from NaiveBayesSpamDaemon.classifier import NaiveBayesOptionParser, NaiveBayesDaemonClassifier as nbc
from nltk.classify import accuracy

def test(options):
    ham_train = nbc.format_features(options.ham_dir, 'ham')
    spam_train = nbc.format_features(options.spam_dir, 'spam')

    training = ham_train[:-len(ham_train)/3]+spam_train[:-len(spam_train)/3]
    test = ham_train[-len(ham_train)/3:]+spam_train[-len(spam_train)/3:]

    nbclassifier = nbc(options)
    nbclassifier.training = training 
    nbclassifier._init_classifier()

    nbclassifier.classifier.show_most_informative_features(20)

    print "Accuracy: %f" % accuracy(nbclassifier.classifier, test)

if __name__=="__main__":
    parser = NaiveBayesOptionParser()
    (options, args) = parser.parse_args()
    test(options)
