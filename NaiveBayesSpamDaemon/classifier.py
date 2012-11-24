from os import listdir, path
import settings
import pika
import uuid
from nltk import NaiveBayesClassifier
from nltk.tokenize import word_tokenize

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
        return self.classifier.classify(self.get_word_features(message)) == 'spam'

class NaiveBayesDaemonClient(object):
    def __init__(self):
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
        while self.response is None:
            self.connection.process_data_events()
        return self.response == "True"
