
# Parserator LINK: /usr/local/lib/python2.7/site-packages/parserator/training.py
python

import properName as pn, pandas as pd, numpy as np

def nameclassifier(data):
    ftotal = len(data)
    idx = ftotal
    count = 0
    data = data[: idx]
    total = len(data)
    for name in data:
        name = str(name)
        try:
            parsed = pn.tag(name)
            if(parsed[1] != "Proper Name"):
                # print(name)
                count += 1
                # print(name)
            # else:
            #     print(name)
        except Exception:
            count += 1
    threshold = 1.0 * count / total
    print(count)
    print(threshold)
    return threshold < 0.3

###########  SALESFORCE  ###########

df = pd.read_csv('../probablepeople/SFDC_-_names___2.csv', header=None)

nameclassifier(df[0])
nameclassifier(df[1])
nameclassifier(df[2])
nameclassifier(df[3])
nameclassifier(df[4])
nameclassifier(df[5])
nameclassifier(df[6])
nameclassifier(df[7])


# >= 5
> 5

0.
F, 1.0
F, 1.0

1.
F, 0.9097
F, 0.9097

2.
T, 0.207760366699
T, 0.207760366699

3.
T, 0.205372561561
T, 0.205329922183

4.  ### !!!
T, 0.0170202181715
T, 0.0169633656682
5.
T, 0.0649468784422
T, 0.0648331734357
6.
T, 0.0413601961411
T, 0.0412749173862
7.
F, 0.507394378709
F, 0.507394378709

###########  ELECTION  ###########

df2 = pd.read_csv("cm.txt", delimiter='|', header=None)
df2[0].head()
nameclassifier(df2[0])
df2[1].head()
nameclassifier(df2[1])  # T, when F (0.173671875)
df2[2].head()
nameclassifier(df2[2])
df2[3].head()
nameclassifier(df2[3])
df2[4].head()
nameclassifier(df2[4])
df2[5].head()
nameclassifier(df2[5])
df2[6].head()
nameclassifier(df2[6])
df2[7].head()
nameclassifier(df2[7])
df2[8].head()
nameclassifier(df2[8])  # T, when supposed to be F
df2[9].head()
nameclassifier(df2[9])  # T, when supposed to be F
df2[10].head()
nameclassifier(df2[10])
df2[11].head()
nameclassifier(df2[11])  # T, when supposed to be F


0
F, 0.999921875
F, 0.999921875

1
F, 0.52015625
F, 0.414375
2
T, 0.113203125
T, 0.111015625

3
F, 0.6525
F, 0.578671875

4
F, 0.961015625
F, 0.958046875

5
F, 0.695625
F, 0.695625

6
F, 0.8878125
F, 0.8878125

7
F, 0.999921875
F, 0.999921875

8
F, 0.999921875
F, 0.999921875

9
F, 1.0
F, 1.0

10
F, 0.677734375
F, 0.677734375

11
F, 0.999921875
F, 0.999921875


###########  TWITTER JSON  ###########

df3 = pd.read_json('twitter.json', lines=True)
df3 = df3[:100]
df3 = pd.io.json.json_normalize(df3['twitter'])

c = df3.columns


def utf(val):
    return val.encode('utf-8')

cols = np.take(df3.columns, [3, 5, 8])

df3[c[0]].head()
nameclassifier(df3[c[0]])
df3[c[1]].head()
nameclassifier(df3[c[1]])
df3[c[2]].head()
nameclassifier(df3[c[2]])
df3[c[3]].head()
df3[c[3]] = df3[c[3]].apply(utf)
nameclassifier(df3[c[3]]) ###
df3[c[4]].head()
nameclassifier(df3[c[4]])
df3[c[5]].head()
df3[c[5]] = df3[c[5]].apply(utf)
nameclassifier(df3[c[5]]) ###
df3[c[6]].head()
nameclassifier(df3[c[6]])
df3[c[7]].head()
nameclassifier(df3[c[7]])
df3[c[8]].head()
df3[c[8]] = df3[c[8]].apply(utf)
nameclassifier(df3[c[8]]) ###


df2=df2.iloc[1:]


def tokenize(raw_string):
    if isinstance(raw_string, bytes):
        try:
            raw_string = str(raw_string, encoding='utf-8')
        except:
            raw_string = str(raw_string)
    re_tokens = re.compile(
        r"""     \bc/o\b
    |
    [("']*\b[^\s\/,;#&()]+\b[.,;:'")]* # ['a-b. cd,ef- '] -> ['a-b.', 'cd,', 'ef']
    |
    [#&@/] """, re.I | re.VERBOSE | re.UNICODE)
    tokens = re_tokens.findall(raw_string)
    tokens = re_tokens.findall(raw_string)
    if not tokens:
        return []
    return tokens




df = pd.read_csv('../probablepeople/SFDC_-_names___2.csv', header=None)


def nc(data):
    ftotal = len(data)
    idx = ftotal
    count = 0
    data = data[: idx]
    total = len(data)
    for name in data:
        name = str(name)
        try:
            parsed = pp.tag(name)
            # print(parsed)
            if(parsed[1] != "Person"):
                count += 1
        except Exception:
            count += 1
    threshold = 1.0 * count / total
    print(count)
    print(threshold)
    return threshold < 0.3

nc(df2[0])
nc(df2[1])
nc(df2[2])
nc(df2[3])
nc(df2[4])
nc(df2[5])
nc(df2[6])
nc(df2[7])
nc(df2[8])
nc(df2[9])
nc(df2[10])
nc(df2[11])
nc(df2[12])
nc(df2[13])
nc(df2[14])




def tokenize(raw_string):
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

count = 0
for i in df[5]:
    x = tokenize(i)
    if pn.tag(x)[1] = 'Proper Name':
        cnt+=1
count




