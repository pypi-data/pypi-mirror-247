import logging
import sys

from .pileup_util import pileup
from .util import ArgumentParser

logging.basicConfig(format="%(message)s", level=logging.INFO)
log = lambda message: logging.info(message)


VERSION = "2023-03-02"
HELP = f"""
usage: $ pileup-reads $INPUT $OUTPUT... $OPTIONS...

arguments:
  $INPUT ----------- path to input bam file
                     required, must be sorted and indexed
  $OUTPUT ---------- path to output file
                     required, may be wig(.gz), bedgraph(.gz) or bigwig
  -b --bin-size ---- output bin size in bp
                     optional, 10 by default
  -r --read-length - single read extension in bp (ignored if paired)
                     optional, 150 by default
  -c --chunk-size -- input read window size in bp
                     optional, 1000000 by default (better to keep as is)
  -d --def-value --- value to use for bins without coverage
                     optional, 0 by default
  -o --out-format -- output format as wig(.gz), bedgraph(.gz) or bigwig
                     optional, inferred from $OUTPUT by default
  -n --normalize --- normalization mode as count, cpm or enrichment
                     optional, count by default (no normalization)
  -p --parallel ---- number of parallel processes to launch
                     optional, 1 by default
  -h --help -------- print help message and exit
  -v --version ----- print version and exit (v. {VERSION})
"""



def main(raw_args):

    if "-h" in raw_args or "--help" in raw_args:
        sys.stderr.write(f"{HELP}\n")
        raise SystemExit(0)
    
    if "-v" in raw_args or "--version" in raw_args:
        sys.stderr.write(f"{VERSION}\n")
        raise SystemExit(0)

    parser = ArgumentParser()
    parser.add_argument("in_path")
    parser.add_argument("out_path")
    parser.add_argument("-b", "--bin-size", type=int, default=10)
    parser.add_argument("-r", "--read-length", type=int, default=150)
    parser.add_argument("-c", "--chunk-size", type=int, default=1000000)
    parser.add_argument("-d", "--def-value", type=float, default=0)
    parser.add_argument("-o", "--out-format", default=None)
    parser.add_argument("-n", "--normalize", default="count")
    parser.add_argument("-p", "--parallel", type=int, default=1)
    arguments = vars(parser.parse_args(raw_args))

    pileup(**arguments)
