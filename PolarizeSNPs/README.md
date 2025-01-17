# PolarizeSNPs

This directory contains tools for polarizing SNPs in VCF files using an outgroup. Polarizing SNPs ensures that derived alleles are represented as `1` and ancestral alleles as `0`.

## Scripts

### `polarize_snps.py`
This script polarizes a VCF file by an outgroup. It adjusts the alleles so that the outgroup is set to `0/0` (if it is homozygous), and other alleles are adjusted accordingly. Sites with a heterozygous outgroup are skipped.

#### Features
- Supports gzipped and uncompressed VCF files.
- Skips sites with unknown or heterozygous outgroup states.
- Outputs a polarized VCF file.

#### Requirements
- Python 3.x
- `argparse`, `gzip`, `logging`

#### Usage
```bash
python polarize_snps.py <input_vcf> <outgroup> <output_vcf>
