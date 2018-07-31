nounType
=========

A type classifier that determines whether an entity is a Proper Name or Other.


Table of Contents
-----------------

* [Installation](#installation)
* [Usage](#usage)
* [Functionality](#functionality)

<a name="installation"></a> Installation
-----------------

The easiest way to install the library is
```
pip install git+git://github.com/trifacta/nounType
```

<a name="usage"></a> Usage
-----------------

Using this parser:

There are two main methods: `parse` and `tag`. 

* `parse` breaks the string into components and classifies each one.
* `tag` merges consecutive components and strips punctuation and classifies the string as a whole.

```Python
>>> import properName as pn

# Proper Name
>>> name = "Charles Smith"

>>> pn.parse(name)
[('Charles', 'Name'), ('Smith', 'Name')]

>>> pn.tag(name)
(OrderedDict([('Name', 'Charles Smith')]), 'Proper Name')


# Other
>>> item = 'apples and oranges'

>>> pn.parse(item)
[('apples', 'Other'), ('and', 'Other'), ('oranges', 'Other')]

>>> pn.tag(item)
(OrderedDict([('Other', 'apples and oranges')]), 'Other')
```

<a name="functionality"></a> Functionality
-----------------
### Proper Name & Training
For the sake of preventing overlap, a name excludes places, company names, addresses, phone numbers, common nouns and other similar categories, even if there are cross-cases (i.e. a noun like Paris can be both a place and a noun).

The name parser was created using [parserator](https://github.com/datamade/parserator) to create domain-specific probabilistic parsers using [python-crfsuite](https://github.com/scrapinghub/python-crfsuite)'s implementation of conditional random fields. The model itself was trained using an xml file where depending on how the entity was tokenized and classified could either be labeled as 'Proper Name' or 'Other'.

The classifer can deal with a variety of cases and forms of names including Proper Case, Upper Case, First Last and names including prefixes and/or suffixes.

### Classifier
A few of the features that the parser uses when tagging an entity include length of the entity, occurrence of special characters, such as 'at' sign (@), hyphens (-)  and punctuation (, or .) and the double [metaphone](https://en.wikipedia.org/wiki/Metaphone) phonetic encoding algorithm.
