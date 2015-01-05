
0.2 (2015-01-31)
================

- initial support for Robotice Control(management Robotice through django admin)
- added platform utils for work with specific platforms (BB, RPi, ..)
- support for more db backends now only Redis is implemented, Mongo will be soon
- drivers was separated into own modules and removed from Robotice
- new global dependency oslo.config which provide tools for making unified CLI for every driver or something else
- support for more comparators, for now is implemented conditions comparator as stable and tested comparator(BaseComparator) and proof of concept for fuzzy comparator is available for testing
- support for new devices TSL2591 and TSL2561

0.1 (2014-08-25)
================

- refactoring, make first distribution