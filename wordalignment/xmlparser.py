import xml.etree.ElementTree, os, sys, re
from sys import argv

#xml_file, destination_folder = argv
xml_files = argv[1]
destination_folder = argv[2]
if (not os.path.exists(destination_folder)):
    os.mkdir(destination_folder)

source_file = open(destination_folder + '/' + 'source', 'w')
target_file = open(destination_folder + '/' + 'target', 'w')

xml_file_array = xml_files.split(',')
try:
    for f in xml_file_array:
        e = xml.etree.ElementTree.parse(f).getroot()
        
        for atype in e.findall('SENT'):
            enele = atype.find('TXT_E')
            vnele = atype.find('TXT_V')
            source_file.write(enele.text.replace('\n', '') + '\r')
            #source_file.write('\n')
            target_file.write(vnele.text.replace('\n', '')+ '\r')
            #source_file.write('\n')
except:
    print('Error in writting files')
    sys.exit(0)
finally:
    source_file.close()
    target_file.close()
