#!/usr/bin/env python

import sys
import gzip
import argparse
import logging

#script polarizes a vcf file by an outgroup so that derived alleles are 1, i.e. the outgroup is set 0/0 (if it is homozygous) and other alleles are adjusted if needed
#if outgroup is heterozygous, sites are skipped (not written to output)
#only for unphased vcf, but easy to adjust by changing the seperator



logging.basicConfig(level=logging.INFO)

def main(args):
    # Open the VCF files
    zipped = args.input_vcf.endswith(".gz")
    vcf = gzip.open(args.input_vcf, "rt") if zipped else open(args.input_vcf, "r")
    out = open(args.output_vcf, "w")#out = gzip.open(args.output_vcf, "wt") if zipped else open(args.output_vcf, "w")

    try:
        for line in vcf:
            if line[0] == "#":
                if line[1] != "#":
                    header = line.rstrip().split("\t")
                    try:
                        outidx = header.index(args.outgroup)
                    except ValueError:
                        logging.error(f"Outgroup {args.outgroup} not found in VCF header.")
                        sys.exit(1)
                out.write(line)
                continue

            line = line.rstrip().split("\t")
            outallele = line[outidx].split(":")[0]
            if outallele in {".", "./.", "0/1", "1/0", "0|1", "1|0", ".|."}:
                continue
            elif outallele in {"0/0", "0|0"}:
                out.write("\t".join(line) + "\n")
            elif outallele in {"1/1", "1|1"}:
                for i in range(9, len(line)):
                    gt = line[i].split(":")
                    if gt[0] in {".", "./.", "0/1", "1/0", "0|1", "1|0", ".|."}:
                        continue
                    gt[0] = "0/0" if gt[0] in {"1/1", "1|1"} else "1/1"
                    line[i] = ":".join(gt)
                out.write("\t".join(line) + "\n")
            else:
                logging.error(f"Unknown allelic state in outgroup: {outallele}")
                sys.exit(1)
    finally:
        vcf.close()
        out.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Polarize a VCF file by an outgroup.')
    parser.add_argument('input_vcf', help='Path to the input VCF file, can be gzipped.')
    parser.add_argument('outgroup', help='Name of the outgroup sample in the VCF file.')
    parser.add_argument('output_vcf', help='Path to the output VCF file.')
    args = parser.parse_args()

    main(args)
