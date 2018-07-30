#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
from builtins import zip
from builtins import range
from past.utils import old_div

import pycrfsuite
import os
import re
import warnings
from collections import OrderedDict
import string
from doublemetaphone import doublemetaphone
from .ratios import ratios
from .gender import gender_names
import math


VOWELS_Y = tuple('aeiouy')
PREPOSITIONS = {'for', 'to', 'of', 'on'}

STREET_NAMES = {
    'allee', 'alley', 'ally', 'aly', 'anex', 'annex', 'annx', 'anx',
    'arc', 'arcade', 'av', 'ave', 'aven', 'avenu', 'avenue', 'avn', 'avnue',
    'bayoo', 'bayou', 'bch', 'beach', 'bend', 'bg', 'bgs', 'bl', 'blf',
    'blfs', 'bluf', 'bluff', 'bluffs', 'blvd', 'bnd', 'bot', 'bottm',
    'bottom', 'boul', 'boulevard', 'boulv', 'br', 'branch', 'brdge', 'brg',
    'bridge', 'brk', 'brks', 'brnch', 'brook', 'brooks', 'btm', 'burg',
    'burgs', 'byp', 'bypa', 'bypas', 'bypass', 'byps', 'byu', 'camp', 'canyn',
    'canyon', 'cape', 'causeway', 'causwa', 'causway', 'cen', 'cent',
    'center', 'centers', 'centr', 'centre', 'ci', 'cir', 'circ', 'circl',
    'circle', 'circles', 'cirs', 'ck', 'clb', 'clf', 'clfs', 'cliff',
    'cliffs', 'club', 'cmn', 'cmns', 'cmp', 'cnter', 'cntr', 'cnyn', 'common',
    'commons', 'cor', 'corner', 'corners', 'cors', 'course', 'court',
    'courts', 'cove', 'coves', 'cp', 'cpe', 'cr', 'crcl', 'crcle', 'crecent',
    'creek', 'cres', 'crescent', 'cresent', 'crest', 'crk', 'crossing',
    'crossroad', 'crossroads', 'crscnt', 'crse', 'crsent', 'crsnt', 'crssing',
    'crssng', 'crst', 'crt', 'cswy', 'ct', 'ctr', 'ctrs', 'cts', 'curv',
    'curve', 'cv', 'cvs', 'cyn', 'dale', 'dam', 'div', 'divide', 'dl', 'dm',
    'dr', 'driv', 'drive', 'drives', 'drs', 'drv', 'dv', 'dvd', 'est',
    'estate', 'estates', 'ests', 'ex', 'exp', 'expr', 'express', 'expressway',
    'expw', 'expy', 'ext', 'extension', 'extensions', 'extn', 'extnsn',
    'exts', 'fall', 'falls', 'ferry', 'field', 'fields', 'flat', 'flats',
    'fld', 'flds', 'fls', 'flt', 'flts', 'ford', 'fords', 'forest', 'forests',
    'forg', 'forge', 'forges', 'fork', 'forks', 'fort', 'frd', 'frds',
    'freeway', 'freewy', 'frg', 'frgs', 'frk', 'frks', 'frry', 'frst', 'frt',
    'frway', 'frwy', 'fry', 'ft', 'fwy', 'garden', 'gardens', 'gardn',
    'gateway', 'gatewy', 'gatway', 'gdn', 'gdns', 'glen', 'glens', 'gln',
    'glns', 'grden', 'grdn', 'grdns', 'green', 'greens', 'grn', 'grns',
    'grov', 'grove', 'groves', 'grv', 'grvs', 'gtway', 'gtwy', 'harb',
    'harbor', 'harbors', 'harbr', 'haven', 'havn', 'hbr', 'hbrs', 'height',
    'heights', 'hgts', 'highway', 'highwy', 'hill', 'hills', 'hiway', 'hiwy',
    'hl', 'hllw', 'hls', 'hollow', 'hollows', 'holw', 'holws', 'hrbor', 'ht',
    'hts', 'hvn', 'hway', 'hwy', 'inlet', 'inlt', 'is', 'island', 'islands',
    'isle', 'isles', 'islnd', 'islnds', 'iss', 'jct', 'jction', 'jctn',
    'jctns', 'jcts', 'junction', 'junctions', 'junctn', 'juncton', 'key',
    'keys', 'knl', 'knls', 'knol', 'knoll', 'knolls', 'ky', 'kys', 'la',
    'lake', 'lakes', 'land', 'landing', 'lane', 'lanes', 'lck', 'lcks', 'ldg',
    'ldge', 'lf', 'lgt', 'lgts', 'light', 'lights', 'lk', 'lks', 'ln', 'lndg',
    'lndng', 'loaf', 'lock', 'locks', 'lodg', 'lodge', 'loop', 'loops', 'lp',
    'mall', 'manor', 'manors', 'mdw', 'mdws', 'meadow', 'meadows', 'medows',
    'mews', 'mi', 'mile', 'mill', 'mills', 'mission', 'missn', 'ml', 'mls',
    'mn', 'mnr', 'mnrs', 'mnt', 'mntain', 'mntn', 'mntns', 'motorway',
    'mount', 'mountain', 'mountains', 'mountin', 'msn', 'mssn', 'mt', 'mtin',
    'mtn', 'mtns', 'mtwy', 'nck', 'neck', 'opas', 'orch', 'orchard', 'orchrd',
    'oval', 'overlook', 'overpass', 'ovl', 'ovlk', 'park', 'parks', 'parkway',
    'parkways', 'parkwy', 'pass', 'passage', 'path', 'paths', 'pike', 'pikes',
    'pine', 'pines', 'pk', 'pkway', 'pkwy', 'pkwys', 'pky', 'pl', 'place',
    'plain', 'plaines', 'plains', 'plaza', 'pln', 'plns', 'plz', 'plza',
    'pne', 'pnes', 'point', 'points', 'port', 'ports', 'pr', 'prairie',
    'prarie', 'prk', 'prr', 'prt', 'prts', 'psge', 'pt', 'pts', 'pw', 'pwy',
    'rad', 'radial', 'radiel', 'radl', 'ramp', 'ranch', 'ranches', 'rapid',
    'rapids', 'rd', 'rdg', 'rdge', 'rdgs', 'rds', 'rest', 'ri', 'ridge',
    'ridges', 'rise', 'riv', 'river', 'rivr', 'rn', 'rnch', 'rnchs', 'road',
    'roads', 'route', 'row', 'rpd', 'rpds', 'rst', 'rte', 'rue', 'run', 'rvr',
    'shl', 'shls', 'shoal', 'shoals', 'shoar', 'shoars', 'shore', 'shores',
    'shr', 'shrs', 'skwy', 'skyway', 'smt', 'spg', 'spgs', 'spng', 'spngs',
    'spring', 'springs', 'sprng', 'sprngs', 'spur', 'spurs', 'sq', 'sqr',
    'sqre', 'sqrs', 'sqs', 'squ', 'square', 'squares', 'st', 'sta', 'station',
    'statn', 'stn', 'str', 'stra', 'strav', 'strave', 'straven', 'stravenue',
    'stravn', 'stream', 'street', 'streets', 'streme', 'strm', 'strt',
    'strvn', 'strvnue', 'sts', 'sumit', 'sumitt', 'summit', 'te', 'ter',
    'terr', 'terrace', 'throughway', 'tl', 'tpk', 'tpke', 'tr', 'trace',
    'traces', 'track', 'tracks', 'trafficway', 'trail', 'trailer', 'trails',
    'trak', 'trce', 'trfy', 'trk', 'trks', 'trl', 'trlr', 'trlrs', 'trls',
    'trnpk', 'trpk', 'trwy', 'tunel', 'tunl', 'tunls', 'tunnel', 'tunnels',
    'tunnl', 'turn', 'turnpike', 'turnpk', 'un', 'underpass', 'union',
    'unions', 'uns', 'upas', 'valley', 'valleys', 'vally', 'vdct', 'via',
    'viadct', 'viaduct', 'view', 'views', 'vill', 'villag', 'village',
    'villages', 'ville', 'villg', 'villiage', 'vis', 'vist', 'vista', 'vl',
    'vlg', 'vlgs', 'vlly', 'vly', 'vlys', 'vst', 'vsta', 'vw', 'vws', 'walk',
    'walks', 'wall', 'way', 'ways', 'well', 'wells', 'wl', 'wls', 'wy', 'xc',
    'xg', 'xing', 'xrd', 'xrds'
}

LABELS = ['Name', 'Other']

# *****************************************************************************
# the XML tag for each labeled string
PARENT_LABEL = 'Nouns'
# the XML tag for a group of strings
GROUP_LABEL = 'NounCollection'
# the null XML tag
NULL_LABEL = 'Null'
# filename for the crfsuite settings file
MODEL_FILE = 'nouns_learned_settings.crfsuite'
# *****************************************************************************


try:
    TAGGER = pycrfsuite.Tagger()
    TAGGER.open(os.path.split(os.path.abspath(__file__))[0]+'/'+MODEL_FILE)
except IOError:
    TAGGER = None
    warnings.warn('You must train the model (parserator train [traindata] '
                  '[modulename]) to create the %s file before you can use the '
                  'parse and tag methods' % MODEL_FILE)


def parse(raw_string, type=None):
    if not TAGGER:
        raise IOError('\nMISSING MODEL FILE: %s\nYou must train the model '
                      'before you can use the parse and tag methods\nTo train '
                      'the model annd create the model file, run:\nparserator '
                      'train [traindata] [modulename]' % MODEL_FILE)

    tokens = tokenize(raw_string)
    if not tokens:
        return []

    features = tokens2features(tokens)

    tags = TAGGER.tag(features)
    return list(zip(tokens, tags))


def tag(raw_string, type=None):
    tagged = OrderedDict()
    for token, label in parse(raw_string):
        tagged.setdefault(label, []).append(token)
    tracker = {'Name':0, 'Other':0}

    for token in tagged:
        tracker[token] = sum([1 for i in tagged[token]])
        component = ' '.join(tagged[token])
        component = component.strip(' ,;')
        tagged[token] = component

    if 'Name' in tagged:
        if tracker['Name'] + tracker['Other'] >= 5 and tracker['Other'] > tracker['Name']:
            name_type = 'Other'
        else:
            name_type = 'Proper Name'
    else:
        name_type = 'Other'

    return tagged, name_type


def tokenize(raw_string):
    # this determines how any given string is split into its tokens
    # handle any punctuation you want to split on, as well as any punctuation
    # to capture

    if isinstance(raw_string, bytes):
        try:
            raw_string = str(raw_string, encoding='utf-8')
        except:
            raw_string = str(raw_string)

    re_tokens = re.compile(r"""
    \bc/o\b
    |
    [("']*\b[^\s\/,;#&()]+\b[.,;:'")]* # ['a-b. cd,ef- '] -> ['a-b.', 'cd,', 'ef']
    |
    [#&@/]
    """,
                           re.I | re.VERBOSE | re.UNICODE)

    tokens = re_tokens.findall(raw_string)

    if not tokens:
        return []

    return tokens


def tokens2features(tokens, check=False):
    # this should call tokenFeatures to get features for individual tokens,
    # as well as define any features that are dependent upon tokens
    # before/after
    initial = False
    feature_sequence = [tokenFeatures(tokens[0])]
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    if check and len(tokens[0]) == 1 and tokens[0].lower() in alphabet:
        initial = True
    previous_features = feature_sequence[-1].copy()

    seen_comma = False

    for token in tokens[1:]:
        # set features for individual tokens (calling tokenFeatures)
        token_features = tokenFeatures(token)
        if not seen_comma and previous_features['comma']:
            seen_comma = True
        if seen_comma:
            token_features['seen.comma'] = True
        current_features = token_features.copy()

        # features for the features of adjacent tokens
        feature_sequence[-1]['next'] = current_features
        token_features['previous'] = previous_features

        # FEATURES THAT ARE DEPENDENT UPON TOKENS BEFORE/AFTER
        # for example, a feature for whether a certain character has appeared
        # previously in the token sequence

        feature_sequence.append(token_features)
        previous_features = current_features

    if len(feature_sequence) > 1:
        # these are features for the tokens at the beginning and end of a
        # string
        feature_sequence[0]['rawstring.start'] = True
        feature_sequence[-1]['rawstring.end'] = True
        feature_sequence[1]['previous']['rawstring.start'] = True
        feature_sequence[-2]['next']['rawstring.end'] = True

    else:
        # a singleton feature, for if there is only one token in a string
        feature_sequence[0]['singleton'] = True

    return feature_sequence


def tokenFeatures(token):
    # defines a dict of features for an individual token
    if token in (u'&'):
        token_clean = token_abbrev = token

    else:
        token_clean = re.sub(r'(^[\W]*)|([^.\w]*$)', u'', token.lower())
        token_abbrev = re.sub(r'\W', u'', token_clean)

    metaphone = doublemetaphone(token_abbrev)

    features = {'nopunc': token_abbrev,
                'abbrev': token_clean.endswith('.'),
                'comma': token.endswith(','),
                'hyphenated': '-' in token_clean,
                'contracted': "'" in token_clean,
                'bracketed': bool(re.match(r'(["(\']\w+)|(\w+[")\'])', token) and not re.match(r'["(\']\w+[")\']', token)),
                'fullbracketed': bool(re.match(r'["(\']\w+[")\']', token)),
                'length': len(token_abbrev),
                'initial': len(token_abbrev) == 1 and token_abbrev.isalpha(),
                'has.vowels': bool(set(token_abbrev[1:]) & set(VOWELS_Y)),
                'just.letters': token_abbrev.isalpha(),
                'roman': set('xvi').issuperset(token_abbrev),
                'endswith.vowel': token_abbrev.endswith(VOWELS_Y),
                'digits': digits(token_abbrev),
                'metaphone1': metaphone[0],
                'metaphone2': metaphone[1],
                'more.vowels': vowelRatio(token_abbrev),
                'in.names': token_abbrev.upper() in ratios,
                'prepositions': token_abbrev in PREPOSITIONS,
                'first.name': ratios.get(token_abbrev.upper(), 0),
                'gender_ratio': gender_names.get(token_abbrev, False),
                'possessive': token_clean.endswith("'s"),
                'checkemail': '@' in token_abbrev
                }

    reversed_token = token_abbrev[::-1]
    for i in range(1, len(token_abbrev)):
        features['prefix_%s' % i] = token_abbrev[:i]
        features['suffix_%s' % i] = reversed_token[:i][::-1]
        if i > 4:
            break

    for tri_gram in ngrams(token_abbrev, 3):
        features[tri_gram] = True

    for four_gram in ngrams(token_abbrev, 4):
        features[four_gram] = True

    return features


def vowelRatio(token):
    n_chars = len(token)
    if n_chars > 1:
        n_vowels = sum(token.count(c) for c in VOWELS_Y)
        return old_div(n_vowels, float(n_chars))
    else:
        return False


def digits(token):
    if token.isdigit():
        return 'all_digits'
    elif set(token) & set(string.digits):
        return 'some_digits'
    else:
        return 'no_digits'


def ngrams(word, n=2):
    return (''.join(letters) for letters in zip(*[word[i:] for i in range(n)]))
