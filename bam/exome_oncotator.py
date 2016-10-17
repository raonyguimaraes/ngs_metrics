#!/usr/bin/env python
# -*- coding: utf-8 -*-

from multiprocessing import Pool
import subprocess
import shlex
import logging
import argparse
import datetime
import os

from subprocess import call

parser = argparse.ArgumentParser()

parser.add_argument("-i", "--input", help="VCF file")
parser.add_argument("-t", "--target", help="VCF file")
parser.add_argument("-o", "--output", help="Output folder")
parser.add_argument("-q", "--quality", help="Quality Score Threshold")
parser.add_argument("-d", "--depth", help="Depth of Coverage Threshold")


args = parser.parse_args()
 
vcf_file = args.input
target_file = args.target
output = args.output
quality = int(args.quality)
depth = int(args.depth)

if not os.path.exists(output):
    os.makedirs(output)

os.chdir(output)

base=os.path.basename(vcf_file)
base_name = os.path.splitext(base)[0]


gvcftools_path = "/home/ubuntu/projects/programs/gvcftools-0.16/bin"
vcftools_path = "/home/ubuntu/projects/programs/vcftools/vcftools-0.1.14/src"
bcftools_path = "/home/ubuntu/projects/programs/bcftools/bcftools-1.3.1"
snpeff_path = "/home/ubuntu/projects/programs/snpeff/snpEff"
oncotator_path = '/home/ubuntu/projects/input/oncotator/oncotator_v1_ds_Jan262014'
#/home/ubuntu/projects/programs/vcftools/vcftools-0.1.14/src/cpp/
#/home/ubuntu/projects/programs/vcftools/vcftools-0.1.14/src/perl/

#extract vcf from gvcf
print('extract vcf from gvcf')
#gzip -dc ../../input/WGC081270U.g.vcf.gz | ../../programs/gvcftools-0.16/bin/extract_variants | bgzip -c > WGC081270U.vcf.gz
command = """cat %s | %s/extract_variants > %s.variants.vcf""" % (vcf_file, gvcftools_path, base_name)
output = call(command, shell=True)
print(output)

#filter good quality
# command = "%s/bcftools filter -T %s -i'QUAL>100 && FMT/DP>100' %s.variants.vcf > %s.filtered.exons.q100.dp100.vcf" % (bcftools_path, target_file, base_name, base_name)
# output = call(command, shell=True)
# print(output)

# #filter good quality
# command = "%s/bcftools filter -T %s -i'QUAL>50 && FMT/DP>50' %s.variants.vcf > %s.filtered.exons.q50.dp50.vcf" % (bcftools_path, target_file, base_name, base_name)
# output = call(command, shell=True)
# print(output)
#filter good quality

command = "%s/bcftools filter -T %s -i'QUAL>%s && FMT/DP>%s' %s.variants.vcf > %s.filtered.exons.q%s.dp%s.vcf" % (bcftools_path, target_file, quality, depth, base_name, base_name, quality, depth)
output = call(command, shell=True)
print(output)

#clean_nonref
vcf_reader = open("%s.filtered.exons.q%s.dp%s.vcf" % (base_name, quality, depth))
vcf_writer = open("%s.oncotator.vcf" % (base_name), 'w')
for line in vcf_reader:
    # print(line)
    if line.startswith("#"):
        vcf_writer.writelines(line)
    else:
        variant = line.split('\t')
        alt = variant[4]
        alt = alt.replace(',<NON_REF>', '')
        variant[4] = alt
        vcf_writer.writelines("\t".join(variant))

vcf_writer.close()

command = 'oncotator -v --db-dir %s -i VCF %s.oncotator.vcf %s.tsv hg19' % (oncotator_path, base_name, base_name)
output = call(command, shell=True)
print(output)
