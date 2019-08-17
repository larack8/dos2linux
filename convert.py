#! /usr/bin/env python
# coding=utf-8

import os
import sys

try:
    input = raw_input
except:
    pass


def usage():
    print('Usage:')
    print('\t  %s' %
          (' python dos2linux.py {linux2dos|dos2linux} {dirname|filename}'))


def err_exit(msg):
    if msg:
        print('%s' % msg)
    usage()
    sys.exit(0)


def getfiles(root):
    for dirpath, dirnames, filenames in os.walk(root):
        for filename in filenames:
            yield os.path.join(dirpath, filename)


def delete_file(file):
    if (os.path.exists(file)):
        os.remove(file)
        print('>>> delete %s ' % file)
    else:
        print(' !!! %s ' % file + ' not exists!')


def format_file(file, toformat='dos2linux'):
    print('>>> %s formatting: %s' % (toformat, file))
    if not os.path.isfile(file):
        print('ERROR: %s invalid normal file' % file)
        return
    if toformat == 'linux2dos':
        line_sep = '\r\n'
    else:
        line_sep = '\n'

    fpath, fname = os.path.split(file)
    shotname, extension = os.path.splitext(fname)
    tempfilename = fpath + os.path.sep + toformat + '-' + fname
    # print('>>> fpath: ' + fpath+", shotname: "+shotname+", extension: "+extension)
    with open(file, 'r') as fd:
        tmpfile = open(tempfilename, 'w+b')
        for line in fd:
            line = line.replace('\r', '')
            line = line.replace('\n', '')
            str = line + line_sep
            tmpfile.write(str.encode())
        tmpfile.close()
    print('>>> convert file: ' + tempfilename)
    # delete_file(file)
    # print('>>> rename ' + tempfilename + ' ->  %s ' % file)
    # os.rename(tempfilename, file)


def uni_format_proc(filename, toformat):
    if not toformat or toformat not in ['linux2dos', 'dos2linux']:
        err_exit('ERROR: %s: Invalid format param' % (toformat))
    if not filename or not os.path.exists(filename):
        err_exit('ERROR: %s: No such file or directory' % (filename))
    if os.path.isfile(filename):
        format_file(filename, toformat)
        return
    if os.path.isdir(filename):
        for file in getfiles(filename):
            uni_format_proc(file, toformat)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        err_exit('ERROR: Invalid arguments')
    uni_format_proc(filename=sys.argv[2], toformat=sys.argv[1])
