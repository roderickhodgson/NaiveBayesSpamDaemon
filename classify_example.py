#!/usr/bin/env python
from NaiveBayesSpamDaemon.classifier import NaiveBayesDaemonClient

client = NaiveBayesDaemonClient()
check_str = lambda test_str: "Is \"%s\" spam? %s" % (test_str, "yes" if client.is_message_spam(test_str) else "no")

print check_str("Hello!")
print check_str("Our team is a unique producer of quality fake documents")
