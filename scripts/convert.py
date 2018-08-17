# Parts of code borrrowed from:
# https://stackoverflow.com/questions/42835956/how-to-parse-a-txt-file-into-xml
import xml.dom.minidom as minidom
import xml.etree.ElementTree as ET
import itertools as it
import sys

# set default formatting to 'UTF8'
reload(sys)
sys.setdefaultencoding('utf8')

# Set up initial label bin - NounCollection -- DO NOT CHANGE
NC = ET.Element('NounCollection')
# Set up names for subelements
# elem under NounCollection -- DO NOT CHANGE
subelem1 = 'Nouns'

##########################################
######### ELEMENTS TO BE CHANGED #########
##########################################
# elem under subelem1 -- CHANGE BASED ON THE TYPE YOU ARE LABELLING
subelem2 = 'Other'  # Either Name, Other
# set file name
filename = 'FILE_NAME_HERE'

#######################
######### END #########
#######################

# open file
with open(filename) as f:
    lines = f.read().splitlines()

# for every line in input file
# add subelements
for line in it.groupby(lines):
    cell = ET.SubElement(NC, subelem1)
    el = ET.SubElement(cell, subelem2)
    el.text = str.encode(''.join(line[0]))

# prettify xml
formatedXML = minidom.parseString(ET.tostring(
                                  NC)).toprettyxml(indent=" ",
                                                   encoding='utf-8').strip()
# Display for debugging
print formatedXML

##########################################
######### ELEMENTS TO BE CHANGED #########
##########################################
# write the formatedXML to file.
with open("stuffs.xml", "w+") as f:
    f.write(formatedXML)
