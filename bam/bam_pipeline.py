#auto scaling version of bam metrics
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from multiprocessing import Pool
import subprocess
import shlex
import logging
import argparse
import datetime


parser.add_argument("-i", "--input", help="BAM files (can be the location on S3)", nargs='+')
parser.add_argument("-n", "--cores", help="Number of Cores to use")

bam_files = args.input
n_cores = int(args.cores)

log_file = "run.%s.log.txt" % (str(datetime.datetime.now()))

logging.basicConfig(filename=log_file,level=logging.DEBUG)

def run_command(command):
    process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            # print(output.strip())
            logging.info(output.strip())
    rc = process.poll()
    return rc

def fastqc(bam_file):
    command = "python bam_fastqc.py -i %s" % (bam_file)
    # run_command(command)
    print command
    # return x*x

if __name__ == '__main__':
    p = Pool(5)
    print(p.map(fastqc, bam_files))
