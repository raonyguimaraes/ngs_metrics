#!/usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import call
import os

import argparse
parser = argparse.ArgumentParser()

parser.add_argument("-i", "--input", help="BAM file (can be the location on S3)")


args = parser.parse_args()
bam_file = args.input


print(bam_file)

#mock up
# bam_file = "../../../input/bam/test.recal.bam"


input_folder = "/home/ubuntu/projects/input/bam"

base=os.path.basename(bam_file)

if bam_file.startswith('s3://'):
    #download file to input folder
    command = "s3cmd get %s %s/" % (bam_file, input_folder)
    output = call(command, shell=True)
    print(output)
    bam_file = "%s/%s" % (input_folder, base)

# base_name = os.path.splitext(base)[0]
base_name = base.split('.')[0]
print(base_name)

memory_use = "15g"

human_reference = "/home/ubuntu/projects/input/b37/human_g1k_v37.fasta" #84 features
human_reference = "/home/ubuntu/projects/input/grch37/d5/hs37d5.fa" #86 features

#create one folder per sample
output_folder = "/home/ubuntu/projects/output/reports/bam/%s" % (base_name)
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

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
command = """/home/ubuntu/projects/programs/subread-1.5.1-Linux-x86_64/bin/featureCounts --donotsort -T 4 -p \
-a /home/ubuntu/projects/input/gtf/Homo_sapiens.GRCh37.75.gtf \
-o %s/%s.featureCounts.txt \
%s""" % (output_folder, base_name, bam_file)
# output = call(command, shell=True)
# print(output)

#bamtools
print('Running bamtools')
command = """/home/ubuntu/projects/programs/bamtools/bin/bamtools stats -in %s > %s/%s.bamtools.stats.txt""" % (bam_file, output_folder, base_name)
# output = call(command, shell=True)
# print(output)

print('Running DepthOfCoverage')
#gatk DepthOfCoverage
command = """
java -Xmx15g -jar %s/GenomeAnalysisTK.jar -T DepthOfCoverage \
-I %s \
-R %s \
-o %s/%s.DepthOfCoverage.txt \
-nt 4 \
--omitIntervalStatistics \
-ct 5 -ct 10 -ct 20 -ct 30 \
-log %s/%s.DepthofCoverage.log \
""" % (gatk_dir, bam_file, human_reference, output_folder, base_name, output_folder, base_name)
# output = call(command, shell=True)
# print(output)

#qualimap BamQC
print('Running qualimap BamQC')
command = """%s/qualimap bamqc \
--java-mem-size=6G \
-bam %s \
-outdir %s \
-nt 3
""" % (qualimap_dir, bam_file, output_folder)
output = call(command, shell=True)
print(output)
 
#samtools flagstat
print('Running samtools flagstat')
command = """%s/samtools flagstat %s > %s/%s.samtools.flagstat.txt
""" % (samtools_dir, bam_file, output_folder, base_name)
output = call(command, shell=True)
print(output)

# #picard
# print('Running CollectAlignmentSummaryMetrics')
# # #CollectAlignmentSummaryMetrics
# command = """
# java -jar -Xmx15g %s/picard.jar CollectAlignmentSummaryMetrics \
# I=%s \
# O=%s/%s.AlignmentSummaryMetrics.txt \
# R=%s \
# VALIDATION_STRINGENCY=SILENT""" % (picard_dir, bam_file, output_folder, base_name, human_reference)
# output = call(command, shell=True)
# print(output)

# print('Running CollectGcBiasMetrics')
# # #CollectGcBiasMetrics
# command = """
# java -jar -Xmx15g %s/picard.jar CollectGcBiasMetrics \
# I=%s \
# O=%s/%s.gc_bias_metrics.txt \
# R=%s \
# CHART=%s/%s.gc_bias_metrics.pdf \
# S=%s/%s.gc_bias_summary_metrics.txt \
# VALIDATION_STRINGENCY=SILENT""" % (picard_dir, bam_file, output_folder, base_name, human_reference, output_folder, base_name, output_folder, base_name)
# output = call(command, shell=True)
# print(output)

# print('Running CollectInsertSizeMetrics')
# #CollectInsertSizeMetrics
# command = """java -Xmx%s -jar %s/picard.jar CollectInsertSizeMetrics \
# I=%s \
# O=%s/%s.insert_size_metrics.txt \
# H=%s/%s.insert_size_histogram.pdf \
# M=0.5 \
# VALIDATION_STRINGENCY=SILENT""" % (memory_use, picard_dir, bam_file, output_folder, base_name, output_folder, base_name)
# output = call(command, shell=True)
# print(output)

# # #MeanQualityByCycle
# print('Running MeanQualityByCycle')
# command = """java -Xmx%s -jar %s/picard.jar MeanQualityByCycle \
# I=%s \
# O=%s/%s.mean_qual_by_cycle.txt \
# CHART=%s/%s.mean_qual_by_cycle.pdf \
# VALIDATION_STRINGENCY=SILENT """ % (memory_use, picard_dir, bam_file, output_folder, base_name, output_folder, base_name)
# output = call(command, shell=True)
# print(output)

# print('Running QualityScoreDistribution')
# # #QualityScoreDistribution
# command = """java -Xmx%s -jar %s/picard.jar QualityScoreDistribution \
# I=%s \
# O=%s/%s.qual_score_dist.txt \
# CHART=%s/%s.qual_score_dist.pdf \
# VALIDATION_STRINGENCY=SILENT """ % (memory_use, picard_dir, bam_file, output_folder, base_name, output_folder, base_name)
# output = call(command, shell=True)
# print(output)

# print('Running BamIndexStats')
# # #BamIndexStats
# command = """java -Xmx%s -jar %s/picard.jar BamIndexStats \
# I=%s \
# O=%s/%s.BamIndexStats.output.txt \
# VALIDATION_STRINGENCY=SILENT""" % (memory_use, picard_dir, bam_file, output_folder, base_name)
# output = call(command, shell=True)
# print(output)

# print('Running CollectHsMetrics')
#CollectHsMetrics
# command = """java -Xmx%s -jar %s/picard.jar CollectHsMetrics \
# I=%s \
# O=%s/%s.hs_metrics.txt \
# R=%s \
# BAIT_INTERVALS=%s \
# TARGET_INTERVALS=%s \
# VALIDATION_STRINGENCY=SILENT """ % (memory_use, picard_dir, bam_file, output_folder, base_name, human_reference, target_file, target_file)
# output = call(command, shell=True)
# print(output)


