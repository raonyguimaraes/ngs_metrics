#!/usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import call
import os

import argparse
parser = argparse.ArgumentParser()

parser.add_argument("-i", "--input", help="VCF file (can be the location on S3)")
parser.add_argument("-t", "--target", help="Target File")

args = parser.parse_args()
vcf_file = args.input
target_file = args.target

print(vcf_file, target_file)


base=os.path.basename(vcf_file)
base_name = os.path.splitext(base)[0]
print(base_name)

#create one folder per sample
output_folder = "/home/ubuntu/projects/output/reports/vcf/%s" % (base_name)
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

output_base = "%s/%s" % (output_folder, base_name)

memory_use = "15g"
gvcftools_path = "/home/ubuntu/projects/programs/gvcftools-0.16/bin"


#extract vcf from gvcf
#gzip -dc ../../input/WGC081270U.g.vcf.gz | ../../programs/gvcftools-0.16/bin/extract_variants | bgzip -c > WGC081270U.vcf.gz
command = """gzip -dc %s | %s/extract_variants | bgzip -c > %s.gz
""" % (vcf_file, gvcftools_path, output_base)
output = call(command, shell=True)
print(output)

#vcftools metrics
#*coverage
#bcftools metrics
#snpeff
