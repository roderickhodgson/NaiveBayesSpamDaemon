## Introduction
A very simple Naive Bayes spam filter intended to run on posts submitted to a website before they are saved to DB. It can be trained by placing plain text ham files and spam files in the relevant directory, where each file represents a possible message.

It is designed to run in the background and called from a webapp or other via RPC.
## Dependencies
- pyyaml
- nltk
- pika
- wsgiref
- A working and running AMQP server

## Installation and use
- ``python setup.py install``
- ``python test.py --ham=[DIRECTORY CONTAINING HAM FILES] --spam=[DIRECTORY CONTAINING SPAM FILES]`` will train over 2/3 of the data, and test over the remaining 1/3.

You can use it directly, or via RPC to a server.

- **Directly**: Create an instance of ``NaiveBayesDaemonClassifier`` with spam and ham file directory locations as arguments, then call ``is_message_spam``, providing a text string as argument. The clasifier will be trained the first time you call ``is_message_spam`` for any given instance of ``NaiveBayesDaemonClassifier``.

- **RPC**: This is (in my opinion) a much better option for webapps. You could even run the classifier on a seperate machine. Run the binary ``classify_server --ham=[DIRECTORY CONTAINING HAM FILES] --spam=[DIRECTORY CONTAINING SPAM FILES]``, then, in your app, create an instance of ``NaiveBayesDaemonClient`` and call ``is_message_spam``, providing a text string as argument. (See ``classify_example.py`` for an example). This call will timeout after one second, classifying the content as ham (in case the server crashes or isn't running).


## Future Work
* Run server as upstart script
* Allow for remote rabbitMQ server
* Proper testing


## License
(The MIT License)

Copyright © 2012 Roderick Hodgson

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the ‘Software’), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED ‘AS IS’, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

