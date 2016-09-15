#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("echo", help="echo the string you use here")
args = parser.parse_args()
print(args.echo)

#extract vcf from gvcf
#vcftools metrics
#*coverage
#bcftools metrics
#snpeff
