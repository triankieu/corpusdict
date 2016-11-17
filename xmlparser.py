import xml.etree.ElementTree

e = xml.etree.ElementTree.parse('E002905.xml').getroot()

for atype in e.findall('SENT'):
    enele = atype.find('TXT_E')
    vnele = atype.find('TXT_V')
    print(enele.text + ' ~= ' + vnele.text)
