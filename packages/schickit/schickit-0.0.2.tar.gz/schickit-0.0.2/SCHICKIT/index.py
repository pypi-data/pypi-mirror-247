import argparse
import os
import sys
import time
from utils.download import make_index







def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-g', '--genome', help='choose from hg38,hg19,mm10,mm9', choices=['hg38','hg19','mm10','mm9'],required=True)
    parser.add_argument('-a', '--aligner', help='choose from bowtie2, bwa',choices=['bowtie2', 'bwa'], required=True)
    parser.add_argument('-p', '--path', help='path to save index', required=True)
    parser.add_argument('-e', '--enzyme', help='enzyme to digest, you can input multiple enzyme,like: MboI,DpnII,BglII',required=True)
    args = parser.parse_args()
    
    make_index(args.path, args.genome, args.aligner, args.enzyme)

if __name__ == '__main__':
    Time = time.time()
    main()
    print('=============time spen ', time.time() - Time, '===================')



