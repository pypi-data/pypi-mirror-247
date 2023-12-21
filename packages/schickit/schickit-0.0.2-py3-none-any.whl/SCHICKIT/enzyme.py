import argparse
import os
import sys
import time
from utils.download import make_digest




def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-e', '--enzyme', help='enzyme to digest',required=True)
    parser.add_argument('-g', '--genome', help='choose from hg38,hg19,mm10,mm9',choices=['hg38','hg19','mm10','mm9'], required=True)
    parser.add_argument('-p', '--path', help='path to save index', required=True)
    args = parser.parse_args()
    
    make_digest(args.path, args.enzyme, args.genome)

if __name__ == '__main__':
    Time = time.time()
    main()
    print('=============time spen ', time.time() - Time, '===================')



