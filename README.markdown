## Introduction
A very simple Naive Bayes spam filter intended to run on posts submitted to a website before they are saved to DB. It can be trained by placing plain text ham files and spam files in the relevant directory.

At the moment it must be called explicitly. I plan to run it as a daemon and communicate with it synchronously, so it does not need to be trained each time a message is posted.

## Installation
- pip install nltk
- populate the train/spam and train/ham directories with basic text files of the relevant class
- ``python classifier.py`` will train over 2/3 of the data, and test over the remaining 1/3.

To use, simply call ``is_message_spam``, providing a text string as argument.

## Future Work
* Allow the provision of seperate training and testing sets.
* Function as a proper module.
* Implement a Daemon which will accept strings through a socket or message passing protocol and return a yes/no spam result.


## License
(The MIT License)

Copyright © 2012 Roderick Hodgson

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the ‘Software’), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED ‘AS IS’, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

