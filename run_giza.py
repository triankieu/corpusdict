import os, sys, glob, re
import configparser
import argparse as ap

def getArg(argument, default_value='', append_char=None):
    argument_value = default_value

    if (argument is not None):
        argument_value = argument

    if (append_char is not None and argument_value[-1] != append_char):
        argument_value += append_char

    return argument_value

def prepareBuildPath():
    if not os.path.isdir(build_path):
        os.mkdir(build_path)
    os.system('rm -f ' + build_path + '*.final')

config = configparser.RawConfigParser(allow_no_value=True)
config.read('giza.conf')
giza_home_conf = config.get('GIZA', 'giza_home')
build_path_conf = config.get('GIZA', 'build_path')
source_conf = config.get('GIZA', 'source_path', )
target_conf = config.get('GIZA', 'target_path')
source_name_conf = config.get('GIZA', 'source_name')
target_name_conf = config.get('GIZA', 'target_name')
source_language_conf = config.get('GIZA', 'source_language')
target_language_conf = config.get('GIZA', 'target_language')


giza_home_default = '/home/ryanhoang/giza-pp'

if (giza_home_conf is not None and giza_home_conf != '' ):
    giza_home_default = giza_home_conf

build_path_default = '/home/ryanhoang/PycharmProjects/corpusdict/data/'

if (build_path_conf is not None and build_path_conf != '' ):
    build_path_default = build_path_conf

parser = ap.ArgumentParser(description='Run GIZA++ arguments')
parser.add_argument('--gizaHome')
parser.add_argument('--buildPath')
parser.add_argument('--source')
parser.add_argument('--target')
parser.add_argument('--sourceName')
parser.add_argument('--targetName')
parser.add_argument('--s')
parser.add_argument('--t')
parser.add_argument('--sourceLanguage')
parser.add_argument('--targetLanguage')
parser.add_argument('--sl')
parser.add_argument('--tl')
args  = parser.parse_args()

giza_home = getArg(args.gizaHome, giza_home_default, '/')

''' build dir '''
build_path = getArg(args.buildPath, build_path_default, '/')
source = getArg(args.source)
if (source is None or source == ''):
    source = getArg(args.s)
if (source is None or source == ''):
    source = source_conf
target = getArg(args.target)
if (target is None or target == ''):
    target = getArg(args.t)
if (target is None or target == ''):
    target = target_conf

src_lang_type = getArg(args.sourceLanguage, '')
if (src_lang_type is None or src_lang_type == ''):
    src_lang_type = getArg(args.sl)

if (src_lang_type is None or src_lang_type == ''):
    src_lang_type = source_language_conf

trgt_lang_type = getArg(args.targetLanguage, '')
if (trgt_lang_type is None or trgt_lang_type == ''):
    trgt_lang_type = getArg(args.tl)

if (trgt_lang_type is None or trgt_lang_type == ''):
    trgt_lang_type = target_language_conf

source_name = getArg(args.sourceName)
target_name = getArg(args.targetName)

if (source_name is None or source_name == ''):
    source_name = source_name_conf

if (target_name is None or target_name == ''):
    target_name = target_name_conf

if (source_name is not None):
    source = build_path + source_name


if (target_name is not None):
    target = build_path + target_name

if (not (os.path.exists(source) and os.path.exists(target))):
    sys.exit(0)

prepareBuildPath()

print('Copying data files...')
sys.stdout.flush()

source_corpus_path = build_path + 'corpus.' + src_lang_type
target_corpus_path = build_path + 'corpus.' + trgt_lang_type

os.chdir(build_path)

os.system('cp ' + source + ' ' + source_corpus_path)
os.system('cp ' + target + ' ' + target_corpus_path)

print('Pre-processing corpus files...')
sys.stdout.flush()
final_src_file = 'corpus.clean.' + src_lang_type
final_dst_file = 'corpus.clean.' + trgt_lang_type
os.system(
    'tr \'[:upper:]\' \'[:lower:]\' < ' + source_corpus_path + ' > ' + build_path + final_src_file)
os.system(
    'tr \'[:upper:]\' \'[:lower:]\' < ' + target_corpus_path + ' >' + build_path + final_dst_file)

print('Starting for source->target...')
print('Running plain2snt...')
sys.stdout.flush()
os.system(giza_home + 'GIZA++-v2/plain2snt.out ' + build_path + final_src_file + ' ' + final_dst_file)
snt_file = build_path + final_src_file + '_' + final_dst_file + '.snt'
src_vcb_file = build_path + final_src_file + '.vcb'
dst_vcb_file = build_path + final_dst_file + '.vcb'

'''
    source -> target
'''

print('Running snt2cooc (source->target)...')
sys.stdout.flush()
cooc_file = build_path + final_src_file + '_' + final_dst_file + '.cooc'
os.system(giza_home + 'GIZA++-v2/snt2cooc.out ' + src_vcb_file + ' ' + dst_vcb_file + ' ' + snt_file + ' > ' + cooc_file)

print('Running mkcls...')
print(giza_home + 'mkcls-v2/mkcls -n10 -p' + build_path + final_src_file + ' -V' + src_vcb_file + '.classes')
sys.stdout.flush()
os.system(giza_home + 'mkcls-v2/mkcls -n10 -p' + build_path + final_src_file + ' -V' + src_vcb_file + '.classes')
os.system(giza_home + 'mkcls-v2/mkcls -n10 -p' + build_path + final_dst_file + ' -V' + dst_vcb_file + '.classes')

print('Run giza on source->target...')
sys.stdout.flush()
os.system(giza_home + 'GIZA++-v2/GIZA++ -S  ' + src_vcb_file + ' -T ' + dst_vcb_file + ' -C ' \
          + snt_file + ' -CoocurrenceFile ' + cooc_file + ' -o ' + build_path + trgt_lang_type + '_' + src_lang_type + '.align ' + ' > ' + build_path + 's_t_nohup.out')

'''
    target -> source
'''
print('Target->source...')
sys.stdout.flush()
snt_file = build_path + final_dst_file + '_' + final_src_file + '.snt'
cooc_file = build_path + final_dst_file + '_' + final_src_file + '.cooc'

print('Running snt2cooc (target->source)...')
sys.stdout.flush()
os.system(giza_home + 'GIZA++-v2/snt2cooc.out ' + src_vcb_file + ' ' + dst_vcb_file + ' ' + snt_file + ' > ' + cooc_file)

print('Run giza...')
sys.stdout.flush()
os.system(giza_home + 'GIZA++-v2/GIZA++ -S  ' + dst_vcb_file + ' -T ' + src_vcb_file + ' -C ' \
          + snt_file + ' -CoocurrenceFile ' + cooc_file + ' -o ' + build_path + src_lang_type + '_' + trgt_lang_type + '.align ' + ' > ' + build_path + 't_s_nohup.out')

print('DONE!')
