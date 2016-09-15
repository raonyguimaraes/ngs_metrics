#!/usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import call
import os

import argparse
parser = argparse.ArgumentParser()

parser.add_argument("-i", "--input", help="GVCF.GZ file (can be the location on S3)")
parser.add_argument("-t", "--target", help="Target File")

args = parser.parse_args()
vcf_file = args.input
target_file = args.target

print(vcf_file, target_file)


base=os.path.basename(vcf_file)
# base_name = os.path.splitext(base)[0]
base_name = base.split('.')[0]
print(base_name)

#create one folder per sample
output_folder = "/home/ubuntu/projects/output/reports/vcf/%s" % (base_name)
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

output_base = "%s/%s" % (output_folder, base_name)

memory_use = "15g"
gvcftools_path = "/home/ubuntu/projects/programs/gvcftools-0.16/bin"
vcftools_path = "/home/ubuntu/projects/programs/vcftools/vcftools-0.1.14/src"
bcftools_path = "/home/ubuntu/projects/programs/bcftools/bcftools-1.3.1/"
#/home/ubuntu/projects/programs/vcftools/vcftools-0.1.14/src/cpp/
#/home/ubuntu/projects/programs/vcftools/vcftools-0.1.14/src/perl/

#extract vcf from gvcf
print('extract vcf from gvcf')
#gzip -dc ../../input/WGC081270U.g.vcf.gz | ../../programs/gvcftools-0.16/bin/extract_variants | bgzip -c > WGC081270U.vcf.gz
command = """gzip -dc %s | %s/extract_variants | bgzip -c > %s.vcf.gz
""" % (vcf_file, gvcftools_path, output_base)
# output = call(command, shell=True)
# print(output)

#index with tabix
command = """tabix -p vcf %s.vcf.gz""" % (output_base)
output = call(command, shell=True)
print(output)

print('vcftools stats')
#vcftools metrics
command = """%s/perl/vcf-stats %s.vcf.gz > %s.vcftools.stats.txt
""" % (vcftools_path, output_base, output_base)
output = call(command, shell=True)
print(output)

#*coverage
#bcftools metrics
print('bcftools stats')
command = "%s/bcftools stats %s.vcf.gz %s.bcftools.stats.txt" % (bcftools_path, output_base, output_base)
output = call(command, shell=True)
print(output)

#snpeff

