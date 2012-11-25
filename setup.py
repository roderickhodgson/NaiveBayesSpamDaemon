from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='NaiveBayesSpamDaemon',
      version='0.1',
      description='Simple Naive-Bayes based classifications of comments/posts. Intended to run as daemon so classifier stays in memory.',
      url='http://github.com/roderickhodgson/NaiveBayesSpamDaemon',
      author='Roderick Hodgson',
      author_email='roderick.hodgson@googlemail.com',
      license='MIT',
      packages=['NaiveBayesSpamDaemon'],
      install_requires=[
          'pyyaml','nltk','pika','wsgiref'
      ],
      scripts=['bin/classifier_server'],
      zip_safe=False)

