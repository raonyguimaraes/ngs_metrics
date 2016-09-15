#!/usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import call
import os

import argparse
parser = argparse.ArgumentParser()

parser.add_argument("-i", "--input", help="GVCF.GZ file (can be the location on S3)")


args = parser.parse_args()
vcf_file = args.input

print(vcf_file)

input_folder = "/home/ubuntu/projects/input/vcf"

if vcf_file.startswith('s3://'):
    #download file to input folder
    command = "s3cmd get %s %s/" % (vcf_file, input_folder)
    output = call(command, shell=True)
    print(output)

base=os.path.basename(vcf_file)
# base_name = os.path.splitext(base)[0]
base_name = base.split('.')[0]
print(base_name)

die()    

#create one folder per sample
output_folder = "/home/ubuntu/projects/output/reports/vcf/%s" % (base_name)
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

output_base = "%s/%s" % (output_folder, base_name)

memory_use = "15g"
gvcftools_path = "/home/ubuntu/projects/programs/gvcftools-0.16/bin"
vcftools_path = "/home/ubuntu/projects/programs/vcftools/vcftools-0.1.14/src"
bcftools_path = "/home/ubuntu/projects/programs/bcftools/bcftools-1.3.1"
snpeff_path = "/home/ubuntu/projects/programs/snpeff/snpEff"
#/home/ubuntu/projects/programs/vcftools/vcftools-0.1.14/src/cpp/
#/home/ubuntu/projects/programs/vcftools/vcftools-0.1.14/src/perl/

#extract vcf from gvcf
print('extract vcf from gvcf')
#gzip -dc ../../input/WGC081270U.g.vcf.gz | ../../programs/gvcftools-0.16/bin/extract_variants | bgzip -c > WGC081270U.vcf.gz
command = """gzip -dc %s | %s/extract_variants | bgzip -c > %s.vcf.gz
""" % (vcf_file, gvcftools_path, output_base)
output = call(command, shell=True)
print(output)

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
command = "%s/bcftools stats %s.vcf.gz > %s.bcftools.stats.txt" % (bcftools_path, output_base, output_base)
output = call(command, shell=True)
print(output)

#snpeff
#extract vcf
print('extract vcf')
command = "bgzip -d -c %s.vcf.gz > %s.vcf" % (output_base, output_base)
output = call(command, shell=True)
print(output)

print('snpeff')
command = "java -Xmx5g -jar %s/snpEff.jar eff -stats %s.snpeff.full.html -i vcf GRCh37.75 %s.vcf > %s.snpeff.full.vcf" % (snpeff_path, output_base, output_base, output_base)
output = call(command, shell=True)
print(output)

# print('filtering')
# #filtering VCF
# command = "%s/bcftools filter -T %s %s.vcf > %s.filtered.exons.vcf" % (bcftools_path, target_file, output_base, output_base)
# output = call(command, shell=True)
# print(output)

# #filtered.exons.q50.dp50.vcf
# command = "%s/bcftools filter -T %s -i'QUAL>50 && FMT/DP>50' %s.vcf > %s.filtered.exons.q50.dp50.vcf" % (bcftools_path, target_file, output_base, output_base)
# output = call(command, shell=True)
# print(output)

# #WGC081270U.filtered.exons.q100.dp100.vcf
# command = "%s/bcftools filter -T %s -i'QUAL>100 && FMT/DP>100' %s.vcf > %s.filtered.exons.q100.dp100.vcf" % (bcftools_path, target_file, output_base, output_base)
# output = call(command, shell=True)
# print(output)

# command = "java -Xmx5g -jar %s/snpEff.jar eff -stats %s.snpeff.exons.html -i vcf GRCh37.75 %s.filtered.exons.vcf > %s.snpeff.exons.vcf" % (snpeff_path, output_base, output_base, output_base)
# output = call(command, shell=True)
# print(output)

# print('snpeff')
# command = "java -Xmx5g -jar %s/snpEff.jar eff -stats %s.snpeff.exons.q100.dp100.html -i vcf GRCh37.75 %s.filtered.exons.q100.dp100.vcf > %s.snpeff.exons.q100.dp100.vcf" % (snpeff_path, output_base, output_base, output_base)
# output = call(command, shell=True)
# print(output)

# print('bcftools stats')
# command = "%s/bcftools stats %s.filtered.exons.q100.dp100.vcf > %s.bcftools.stats.exons.q100.dp100.txt" % (bcftools_path, output_base, output_base)
# output = call(command, shell=True)
# print(output)

# print('plot vcf-stats')
# command = "%s/plot-vcfstats %s.bcftools.stats.exons.q100.dp100.txt -p %s" % (bcftools_path, output_base, output_base)
# output = call(command, shell=True)
# print(output)
