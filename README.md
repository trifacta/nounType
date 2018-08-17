nounType
=========

A type classifier that determines whether an entity is a Proper Name or Other.


Table of Contents
-----------------

* [Installation](#installation)
* [Usage](#usage)
* [(Re-)Training](#training)
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

<a name="training"></a> (Re-)Training
-----------------
Follow the below steps to re-train this model (as there is already trained crfsuite file):

1. Install [parserator](https://github.com/datamade/parserator) onto your computer.
```
pip install parserator
```
2. Prepare the XML file for the training data. 

* For help formatting and creating the XML file, there is a `scripts/convert.py` file that will create the file based on the tag you wish to use. Compilation of the seperate XML files will need to be done separately.
* Another way to create the training file is to use parserator's command line interface to manually label tokens. It uses values in first column, and it ignores all other columns. To start labeling, run 
```
parserator label [infile] [outfile] properName
``` 
For example, ```parserator label training/training.csv training/combined.xml properName```.

3. Once the XML File is created, to re-train the model, simply run the command 
```
parserator train [traindata] properName
```
Substitute `[traindata]` for the filepath to the XML file. For example, ` parserator train training/totalcomb_v2.xml properName`.


<a name="functionality"></a> Functionality
-----------------
### Proper Name & Training
For the sake of preventing overlap, a name excludes places, company names, addresses, phone numbers, common nouns and other similar categories, even if there are cross-cases (i.e. a noun like Paris can be both a place and a noun).

The name parser was created using [parserator](https://github.com/datamade/parserator) to create domain-specific probabilistic parsers using [python-crfsuite](https://github.com/scrapinghub/python-crfsuite)'s implementation of conditional random fields. The model itself was trained using an xml file where depending on how the entity was tokenized and classified could either be labeled as 'Proper Name' or 'Other'.

The classifer can deal with a variety of cases and forms of names including Proper Case, Upper Case, First Last and names including prefixes and/or suffixes.

### Classifier
A few of the features that the parser uses when tagging an entity include length of the entity, occurrence of special characters, such as 'at' sign (@), hyphens (-)  and punctuation (, or .) and the double [metaphone](https://en.wikipedia.org/wiki/Metaphone) phonetic encoding algorithm.
