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


human_reference = "/home/ubuntu/projects/input/b37/human_g1k_v37.fasta"

output_folder = "/home/ubuntu/projects/output/reports/bam"
samtools_dir = "/home/ubuntu/projects/programs/samtools-1.3.1"
picard_dir = "/home/ubuntu/projects/programs/picard"
gatk_dir = "/home/ubuntu/projects/programs/gatk"
qualimap_dir = "/home/ubuntu/projects/programs/qualimap/qualimap_v2.2"

#s3
#if bam file start with s3 download from s3

if not os.path.exists(bam_file+'.bai'):
    print('Indexing BAM')
    #index bam
    command = "%s/samtools index %s" % (samtools_dir, bam_file)
    output = call(command, shell=True)
    print(output)

#fastqc
#done already!

print('Running featureCounts')
#featureCounts
command = """/home/ubuntu/projects/programs/subread-1.5.1-Linux-x86_64/bin/featureCounts -T 4 -p \
-a /home/ubuntu/projects/input/gtf/Homo_sapiens.GRCh37.75.gtf \
-o %s/%s.featureCounts \
%s""" % (output_folder, base_name, bam_file)
# output = call(command, shell=True)
# print(output)

#bamtools
command = """/home/ubuntu/projects/programs/bamtools/bin/bamtools stats -in %s > %s/%s.bamtools.stats""" % (bam_file, output_folder, base_name)
# output = call(command, shell=True)
# print(output)

print('Running DepthOfCoverage')
#gatk DepthOfCoverage
command = """
java -Xmx15g -jar %s/GenomeAnalysisTK.jar -T DepthOfCoverage \
-I %s \
-R %s \
-o %s/%s.DepthOfCoverage \
-L %s \
-log %s/%s.DepthofCoverage.log \
""" % (gatk_dir, bam_file, human_reference, output_folder, base_name, target_file, output_folder, base_name)
# output = call(command, shell=True)
# print(output)

#picard
print('Running CollectAlignmentSummaryMetrics')
# #CollectAlignmentSummaryMetrics
command = """
java -jar -Xmx15g %s/picard.jar CollectAlignmentSummaryMetrics \
I=%s \
O=%s/%s.AlignmentSummaryMetrics \
R=%s \
VALIDATION_STRINGENCY=LENIENT """ % (picard_dir, bam_file, output_folder, base_name, human_reference)
output = call(command, shell=True)
print(output)

# #CollectGcBiasMetrics
# command = """
# java -jar %s/CollectGcBiasMetrics.jar \
# R=%s \
# I=%s \
# O=%s.b37_1kg.GcBiasMetrics \
# CHART=%s.b37_1kg.GcBiasMetrics.pdf \
# VALIDATION_STRINGENCY=LENIENT """ % (pic_dir, reference, input_file, filename, filename)
# os.system(command)

# #CollectInsertSizeMetrics
# command = """
# java -jar %s/CollectInsertSizeMetrics.jar \
# I=%s \
# O=%s.b37_1kg.CollectInsertSizeMetrics \
# H=%s.b37_1kg.CollectInsertSizeMetrics.pdf \
# VALIDATION_STRINGENCY=LENIENT """ % (pic_dir, input_file, filename, filename)
# os.system(command)

# #MeanQualityByCycle
# command = """
# java -jar %s/MeanQualityByCycle.jar \
# I=%s \
# O=%s.b37_1kg.MeanQualityByCycle \
# CHART=%s.b37_1kg.MeanQualityByCycle.pdf \
# VALIDATION_STRINGENCY=LENIENT """ % (pic_dir, input_file, filename, filename)
# os.system(command)

# #QualityScoreDistribution
# command = """
# java -jar %s/QualityScoreDistribution.jar \
# I=%s \
# O=%s.b37_1kg.QualityScoreDistribution \
# CHART=%s.b37_1kg.QualityScoreDistribution.pdf \
# VALIDATION_STRINGENCY=LENIENT """ % (pic_dir, input_file, filename, filename)
# os.system(command)

# #BamIndexStats
# command = """
# java -jar %s/BamIndexStats.jar \
# INPUT=%s \
# VALIDATION_STRINGENCY=LENIENT """ % (pic_dir, input_file)
# os.system(command)

# #CalculateHsMetrics WholeGenome or CalculateHsMetrics ????
# command = """
# java -jar -Xmx4g %s/CalculateHsMetrics.jar \
# INPUT=%s \
# OUTPUT=%s.b37_1kg.HsMetrics \
# BAIT_INTERVALS=%s \
# TARGET_INTERVALS=%s \
# VALIDATION_STRINGENCY=LENIENT """ % (pic_dir, input_file, filename, exon, exon)
# #os.system(command)

#qualimap BamQC

#samtools flagstat


