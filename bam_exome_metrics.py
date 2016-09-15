#!/usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import call
import os

import argparse
parser = argparse.ArgumentParser()

parser.add_argument("-i", "--input", help="BAM file (can be the location on S3)")
parser.add_argument("-t", "--target", help="Target File")

args = parser.parse_args()
bam_file = args.input
target_file = args.target

print(bam_file, target_file)

#mock up
# bam_file = "../../../input/bam/test.recal.bam"

base=os.path.basename(bam_file)
base_name = os.path.splitext(base)[0]
print(base_name)


output_folder = "/home/ubuntu/projects/output/reports/bam"
#s3
#if bam file start with s3 download from s3

#fastqc
#done!

#featurecounts

#Usage: featureCounts [options] -a <annotation_file> -o <output_file> input_file1 [input_file2] ...

## Required arguments:
  # -a <string>         Name of an annotation file. GTF/GFF format by default.
  #                     See -F option for more formats.

  # -o <string>         Name of the output file including read counts. A separate
  #                     file including summary statistics of counting results is
  #                     also included in the output (`<string>.summary')

  # input_file1 [input_file2] ...   A list of SAM or BAM format files.

command = """/home/ubuntu/projects/programs/subread-1.5.1-Linux-x86_64/bin/featureCounts -T 4 -p \
-a /home/ubuntu/projects/input/gtf/Homo_sapiens.GRCh37.75.gtf \
-o %s/%s \
%s""" % (output_folder, base_name, bam_file)
output = call(command, shell=True)
print(output)

#bamtools
#gatk
#picard
#qualimap
#samtools flagstat


