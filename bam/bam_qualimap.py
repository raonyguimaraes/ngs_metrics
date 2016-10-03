#auto scaling version of bam metrics
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from multiprocessing import Pool
import subprocess
import shlex
import logging
import argparse
import datetime
import os

parser = argparse.ArgumentParser()

parser.add_argument("-i", "--input", help="BAM files (can be the location on S3)", nargs='+')
parser.add_argument("-n", "--cores", help="Number of Cores to use")

args = parser.parse_args()

bam_files = args.input
n_cores = int(args.cores)
memory = '32'
qualimap_dir = "/home/ubuntu/projects/programs/qualimap/qualimap_v2.2"
# log_file = "/home/ubuntu/projects/output/logs/run.%s.log.txt" % (str(datetime.datetime.now()).replace(' ', '_'))
# logging.basicConfig(filename=log_file,level=logging.DEBUG)


def run_command(command):
    # print(command)
    process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
            # logging.info(output.strip())
    rc = process.poll()
    return rc

def qualimap(bam_file):
    # command = "python bam_fastqc.py -i %s" % (bam_file)
    input_folder = '/home/ubuntu/projects/input/bam'
    base=os.path.basename(bam_file)
    base_name = os.path.splitext(base)[0]
    bam_file = "%s/%s" % (input_folder, base)

    print(base, base_name)
    
    output_folder = '/home/ubuntu/projects/output/bam/%s' % (base_name)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    print('Running qualimap BamQC')
    command = """%s/qualimap bamqc \
    --java-mem-size=%sG \
    -bam %s \
    -outdir %s \
    -nt %s
    """ % (qualimap_dir, memory, bam_file, output_folder, n_cores)
    # output = call(command, shell=True)
    # print(output)
    run_command(command)
    # return x*x

if __name__ == '__main__':
    p = Pool(1)
    print(p.map(qualimap, bam_files))
