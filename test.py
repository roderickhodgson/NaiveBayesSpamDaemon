from os import listdir, path
from NaiveBayesSpamDaemon.classifier import NaiveBayesDaemonClassifier as nbc
from nltk.classify import accuracy
from optparse import OptionParser

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
    parser = OptionParser()
    parser.add_option("-s", "--spam", dest="spam_dir", default="spam",
                      help="Directory containing plaintext files for each spam message")
    parser.add_option("-m", "--ham", dest="ham_dir", default="ham",
                      help="Directory containing plaintext files for each ham message")

    (options, args) = parser.parse_args()
    test(options)
