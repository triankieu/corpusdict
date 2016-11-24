import os
import sys
import configparser
import argparse as ap
import subprocess

from wordalignment import gizaproperty


def getarg(argument, default_value='', append_char=None):
    argument_value = default_value

    if argument is not None:
        argument_value = argument

    if append_char is not None and argument_value[-1] != append_char:
        argument_value += append_char

    return argument_value


def preparebuildpath(build_path):
    if not os.path.isdir(build_path):
        os.mkdir(build_path)
    # os.system('rm -f ' + build_path + '*.final')
    subprocess.call(['rm', '-f', build_path + '*.final'])


def loadgizaproperties():
    giza_properties = gizaproperty.GizaProperty()

    config = configparser.RawConfigParser(allow_no_value=True)
    config.read('giza.conf')
    giza_home_conf = config.get('GIZA', 'giza_home')
    if giza_home_conf is not None and giza_home_conf != '':
        giza_properties.giza_home = giza_home_conf

    build_path_conf = config.get('GIZA', 'build_path')

    if build_path_conf is not None and build_path_conf != '':
        giza_properties.build_path = build_path_conf

    source_conf = config.get('GIZA', 'source_path', )
    target_conf = config.get('GIZA', 'target_path')
    source_name_conf = config.get('GIZA', 'source_name')
    target_name_conf = config.get('GIZA', 'target_name')
    source_language_conf = config.get('GIZA', 'source_language')
    target_language_conf = config.get('GIZA', 'target_language')
    out_path_conf = config.get('GIZA', 'out_path')

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
    parser.add_argument('--out')
    args = parser.parse_args()

    giza_properties.giza_home = getarg(args.gizaHome, giza_properties.giza_home, '/')
    giza_properties.build_path = getarg(args.buildPath, giza_properties.build_path, '/')
    giza_properties.out_path = getarg(args.out, out_path_conf, '/')
    source = getarg(args.source)
    if source is None or source == '':
        giza_properties.source = getarg(args.s)
    if giza_properties.source is None or giza_properties.source == '':
        giza_properties.source = source_conf

    target = getarg(args.target)
    if target is None or target == '':
        giza_properties.target = getarg(args.t)
    if giza_properties.target is None or giza_properties.target == '':
        giza_properties.target = target_conf

    src_lang_type = getarg(args.sourceLanguage, '')
    if src_lang_type is None or src_lang_type == '':
        giza_properties.src_lang_type = getarg(args.sl)

    if giza_properties.src_lang_type is None or giza_properties.src_lang_type == '':
        giza_properties.src_lang_type = source_language_conf

    trgt_lang_type = getarg(args.targetLanguage, '')
    if trgt_lang_type is None or trgt_lang_type == '':
        giza_properties.trgt_lang_type = getarg(args.tl)

    if giza_properties.trgt_lang_type is None or giza_properties.trgt_lang_type == '':
        giza_properties.trgt_lang_type = target_language_conf

    source_name = getarg(args.sourceName)
    target_name = getarg(args.targetName)

    if source_name is None or source_name == '':
        giza_properties.source_name = source_name_conf

    if target_name is None or target_name == '':
        giza_properties.target_name = target_name_conf

    if giza_properties.source_name is not None:
        giza_properties.source = giza_properties.build_path + giza_properties.source_name

    if giza_properties.target_name is not None:
        giza_properties.target = giza_properties.build_path + giza_properties.target_name

    return giza_properties


def dowordalignment(source, target, output):
    print('Call dowordalignment')

    giza_properties = loadgizaproperties()

    if source is not None:
        giza_properties.source = source

    if target is not None:
        giza_properties.target = target

    if output is not None:
        giza_properties.out_path = output

    if not (os.path.exists(giza_properties.source) and os.path.exists(giza_properties.target)):
        print('Source or target is not selected.')
        return

    preparebuildpath(giza_properties.build_path)

    print('Copying data files...')
    sys.stdout.flush()

    source_corpus_path = giza_properties.build_path + 'corpus.' + giza_properties.src_lang_type
    target_corpus_path = giza_properties.build_path + 'corpus.' + giza_properties.trgt_lang_type

    os.chdir(giza_properties.build_path)

    os.system('cp ' + giza_properties.source + ' ' + source_corpus_path)
    os.system('cp ' + giza_properties.target + ' ' + target_corpus_path)

    print('Pre-processing corpus files...')
    sys.stdout.flush()
    final_src_file = 'corpus.clean.' + giza_properties.src_lang_type
    final_dst_file = 'corpus.clean.' + giza_properties.trgt_lang_type
    os.system(
        'tr \'[:upper:]\' \'[:lower:]\' < ' + source_corpus_path + ' > ' + giza_properties.build_path + final_src_file)
    os.system(
        'tr \'[:upper:]\' \'[:lower:]\' < ' + target_corpus_path + ' >' + giza_properties.build_path + final_dst_file)

    print('Starting for source->target...')
    print('Running plain2snt...')
    sys.stdout.flush()
    os.system(
        giza_properties.giza_home + 'GIZA++-v2/plain2snt.out '
        + giza_properties.build_path + final_src_file + ' ' + final_dst_file)
    snt_file = giza_properties.build_path + final_src_file + '_' + final_dst_file + '.snt'
    src_vcb_file = giza_properties.build_path + final_src_file + '.vcb'
    dst_vcb_file = giza_properties.build_path + final_dst_file + '.vcb'

    '''
        source -> target
    '''

    print('Running snt2cooc (source->target)...')
    sys.stdout.flush()
    cooc_file = giza_properties.build_path + final_src_file + '_' + final_dst_file + '.cooc'
    os.system(
        giza_properties.giza_home + 'GIZA++-v2/snt2cooc.out '
        + src_vcb_file + ' ' + dst_vcb_file + ' ' + snt_file + ' > ' + cooc_file)

    print('Running mkcls...')
    print(
        giza_properties.giza_home + 'mkcls-v2/mkcls -n10 -p'
        + giza_properties.build_path + final_src_file + ' -V' + src_vcb_file + '.classes')
    sys.stdout.flush()
    os.system(
        giza_properties.giza_home + 'mkcls-v2/mkcls -n10 -p'
        + giza_properties.build_path + final_src_file + ' -V' + src_vcb_file + '.classes')
    os.system(
        giza_properties.giza_home + 'mkcls-v2/mkcls -n10 -p'
        + giza_properties.build_path + final_dst_file + ' -V' + dst_vcb_file + '.classes')

    print('Run giza on source->target...')
    sys.stdout.flush()
    os.system(giza_properties.giza_home + 'GIZA++-v2/GIZA++ -S  ' + src_vcb_file + ' -T ' + dst_vcb_file + ' -C '
              + snt_file + ' -CoocurrenceFile ' + cooc_file
              + ' -o ' + giza_properties.build_path + giza_properties.trgt_lang_type
              + '_' + giza_properties.src_lang_type + '.align ' + ' > ' + giza_properties.build_path + 's_t_nohup.out')

    '''
        target -> source
    '''
    print('Target->source...')
    sys.stdout.flush()
    snt_file = giza_properties.build_path + final_dst_file + '_' + final_src_file + '.snt'
    cooc_file = giza_properties.build_path + final_dst_file + '_' + final_src_file + '.cooc'

    print('Running snt2cooc (target->source)...')
    sys.stdout.flush()
    os.system(
        giza_properties.giza_home + 'GIZA++-v2/snt2cooc.out '
        + src_vcb_file + ' ' + dst_vcb_file + ' ' + snt_file + ' > ' + cooc_file)

    print('Run giza...')
    sys.stdout.flush()
    os.system(giza_properties.giza_home + 'GIZA++-v2/GIZA++ -S  '
              + dst_vcb_file + ' -T ' + src_vcb_file + ' -C '
              + snt_file + ' -CoocurrenceFile ' + cooc_file
              + ' -o ' + giza_properties.out_path + giza_properties.src_lang_type
              + '_' + giza_properties.trgt_lang_type + '.align ' + ' > ' + giza_properties.out_path + 't_s_nohup.out')

    print('DONE!')


# dowordalignment()
