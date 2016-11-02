#auto scaling version of bam metrics
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from multiprocessing import Pool
import subprocess
import shlex
import logging
import argparse
import datetime
from subprocess import call
import os

parser = argparse.ArgumentParser()

parser.add_argument("-i", "--input", help="FASTQC files (can be the location on S3)", nargs='+')
parser.add_argument("-n", "--cores", help="Number of Cores to use")

args = parser.parse_args()

fastq_files = args.input
n_cores = int(args.cores)

fastqc_dir = "/home/ubuntu/projects/programs/fastqc/FastQC/"
input_folder = "/home/ubuntu/projects/input/fastq"

def fastqc(fastq_file):

    print(fastq_file)
    base=os.path.basename(fastq_file)
    print(base)
    filename = base.split('.')[0]
    print(filename)
    
    #Download from S3
    command = "s3cmd get --continue %s %s/" % (fastq_file, input_folder)
    output = call(command, shell=True)
    print(output)
    fastq_file = "%s/%s" % (input_folder, base)
    print(fastq_file)

    #create output folder
    output_folder = "/home/ubuntu/projects/output/fastq/%s" % (filename)
    print(output_folder)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    #fastqc
    command = "%s/fastqc %s -o %s" % (fastqc_dir, fastq_file, output_folder)
    output = call(command, shell=True)
    print(output)

    #Delete FASTQ
    command = "rm %s" % (fastq_file)
    output = call(command, shell=True)
    print(output)

if __name__ == '__main__':
    p = Pool(n_cores)
    print(p.map(fastqc, fastq_files))
