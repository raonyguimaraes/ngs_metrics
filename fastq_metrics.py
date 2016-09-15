

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("echo", help="echo the string you use here")
parser.add_argument("-v", "--verbose", help="increase output verbosity")
args = parser.parse_args()
print(args.echo)

#fastqc
#fastq screener

