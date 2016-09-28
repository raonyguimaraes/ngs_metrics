#!/usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import call, check_output#, run

import subprocess
import shlex 

import os
import time
import datetime
import argparse

import logging

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

parser = argparse.ArgumentParser()

parser.add_argument("-i", "--input", help="BAM files (can be the location on S3)")

args = parser.parse_args()

bam_file = args.input

print(bam_file)

input_folder = '/home/ubuntu/projects/input/bam'
base=os.path.basename(bam_file)
base_name = os.path.splitext(base)[0]

print(base, base_name)
output_folder = '/home/ubuntu/projects/output/bam/%s' % (base_name)
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

log_file = "/home/ubuntu/projects/output/logs/%s.download.run.%s.log.txt" % (base_name, str(datetime.datetime.now()).replace(' ', '_'))

logging.basicConfig(filename=log_file,level=logging.DEBUG)

def run_command(command):
    process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
            logging.info(output.strip())
    rc = process.poll()
    return rc

# your code
start_time = datetime.datetime.now()
logging.info("Start time: "+str(start_time))
# print(base_name)
# print(bam_file)


if bam_file.startswith('s3://'):
    #download file to input folder
    command = "s3cmd get --continue %s %s/" % (bam_file, input_folder)
    run_command(command)


if not os.path.exists(bam_file+'.bai'):
    #Download index
    command = "s3cmd get --continue %s.bai %s/" % (bam_file, input_folder)
    run_command(command)

bam_file = "%s/%s" % (input_folder, base)

print(bam_file)

# os.remove(bam_file)
finish_time = datetime.datetime.now()
logging.info("Finish time: "+str(finish_time))
logging.info("Time Taken: "+str(finish_time-start_time))
