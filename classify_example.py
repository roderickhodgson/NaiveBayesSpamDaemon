#!/usr/bin/env python
from NaiveBayesSpamDaemon.classifier import NaiveBayesDaemonClient

client = NaiveBayesDaemonClient()
test_str = "Hello!"
print "Is \"%s\" spam? %d" % (test_str, client.is_message_spam(test_str))
