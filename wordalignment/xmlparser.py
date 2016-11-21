import xml.etree.ElementTree, os, sys, re
import subprocess
from nltk.tokenize import word_tokenize
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

# source_token_file = open(destination_folder + '/' + 'source.tok', 'w')
# source_file = open(destination_folder + '/' + 'source', 'r')
# try:
#     lines = source_file.readlines()
#     for line in lines:
#         line_tokens = word_tokenize(line)
#         for token in line_tokens:
#             source_token_file.write(token + ' ')
#         source_token_file.write(os.linesep)
# except:
#     print('Error in writting files')
#     sys.exit(0)
# finally:
#     source_file.close()
#     source_token_file.close()

subprocess.Popen('/home/ryanhoang/Downloads/vntokenizer/vnTokenizer.sh %s %s %s %s'
                 % ('-i ' , destination_folder + '/' + 'source', '-o ' , destination_folder + '/' + 'source.tok'),
                 cwd=r'/home/ryanhoang/Downloads/vntokenizer/', shell=True)

subprocess.Popen('/home/ryanhoang/Downloads/vntokenizer/vnTokenizer.sh %s %s %s %s'
                 % ('-i ' , destination_folder + '/' + 'target', '-o ' , destination_folder + '/' + 'target.tok'),
                 cwd=r'/home/ryanhoang/Downloads/vntokenizer/', shell=True)
