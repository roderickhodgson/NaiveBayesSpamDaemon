from os import listdir, path
import codecs
import pika
import uuid
from time import time
from nltk import NaiveBayesClassifier
from nltk.tokenize import word_tokenize
from optparse import OptionParser

class NaiveBayesOptionParser(OptionParser):
    def __init__(self):
        OptionParser.__init__(self)
        self.add_option("-s", "--spam", dest="spam_dir", default="spam",
                          help="Directory containing plaintext files for each spam message")
        self.add_option("-m", "--ham", dest="ham_dir", default="ham",
                          help="Directory containing plaintext files for each ham message")


class NaiveBayesDaemonClassifier(object):

    @staticmethod
    def data_files(dir):
        if not path.isdir(dir):
            raise IOError('Directory "%s" does not exist. Have you specified the correct spam and ham directories at the command line' % dir)
        return [path.join(dir, f) for f in listdir(dir) if f[0]!="."]

    @staticmethod
    def get_word_features(data):
        words = word_tokenize(data)
        return {word: True for word in words}

    @staticmethod
    def get_word_features_from_file(file):
        with codecs.open(file, 'r', encoding='utf-8') as f:
            data = f.read()
        return NaiveBayesDaemonClassifier.get_word_features(data)

    @staticmethod
    def format_features(location, label):
        files = NaiveBayesDaemonClassifier.data_files(location)

        features = map(NaiveBayesDaemonClassifier.get_word_features_from_file, files)
        return [(f, label) for f in features]


    def __init__(self, options):
        self.classifier = None
        self.training = None
        self.options = options

    def _init_classifier(self):
        if not self.training:
            self._prepare_train()
        self.classifier = NaiveBayesClassifier.train(self.training)


    def _prepare_train(self):
        self.ham_train = self.format_features(self.options.ham_dir, 'ham')
        self.spam_train = self.format_features(self.options.spam_dir, 'spam')

        self.training = self.ham_train+self.spam_train


    def is_message_spam(self, message):
        if self.classifier == None:
            self._init_classifier()
        if isinstance(message, str):
            message = message.encode('utf-8')
        return self.classifier.classify(self.get_word_features(message)) == 'spam'

class NaiveBayesDaemonClient(object):
    def __init__(self):
        self.timeout = 1 #timeout after 5 seconds

        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='localhost'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def is_message_spam(self, message):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key='naive_bayes_rpc_queue',
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,
                                         correlation_id = self.corr_id,
                                         ),
                                   body=message)
        start = time()
        while self.response is None:
            if time()-start > self.timeout:
                return False
            self.connection.process_data_events()
        return self.response == "True"
