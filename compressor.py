# -*- coding: utf-8 -*-
__doc__ = "require http://yuilibrary.com/downloads/#yuicompressor in ~/jar/"
import sys
import subprocess
import os, os.path, shutil
from optparse import OptionParser


parser = OptionParser()
parser.add_option("-c", "--compressor", dest="compressor",
                  help="path to yuicompressor")
parser.add_option("-o", "--output", dest="out_file",
                  help="Output file")
parser.add_option("-t", "--type", dest="in_type",
                  default='js', help="js / css")
parser.add_option("-v", "--verbose", dest="verbose",
                  action="store_true", default=False,
                  help="Output file")

def main(args=None):
    opts, paths = parser.parse_args(args or sys.argv[1:])
    out_file = opts.out_file
    in_type = opts.in_type

    in_files = []

    if not out_file or not paths or not opts.compressor:
        parser.parse_args(['-h'])

    temp_file = '/tmp/compressor.tmp'

    for p in paths:
        if '*' in p:
            in_files.extend(glob.glob(p))
        else:
            in_files.append(p)

    temp = open(temp_file, 'wb')
    for f in in_files:
        fh = open(f)
        data = fh.read() + '\n'
        fh.close()

        temp.write(data)

        print '+ %s' % f
    temp.close()

    options = ['-o "%s"' % out_file,
               '--type %s' % in_type]

    if opts.verbose:
        options.append('-v')

    subprocess.call('java -jar "%s" %s "%s"' % (opts.compressor,
                                          ' '.join(options),
                                          temp_file), shell=True)

    org_size = os.path.getsize(temp_file)
    new_size = os.path.getsize(out_file)

    print '=> %s' % out_file
    print 'Original: %.2f kB' % (org_size / 1024.0)
    print 'Compressed: %.2f kB' % (new_size / 1024.0)
    print 'Reduction: %.1f%%' % (float(org_size - new_size) / org_size * 100)
    print ''

if __name__ == '__main__':
    main()

