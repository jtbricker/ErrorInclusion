#!/usr/local/bin/python
from numpy.random import poisson
from random import random
from math import log
from Bio import SeqIO

bases = ['A','T','C','G']

#---------Function: assign_error
# 
#	Input: Raw FASTA Sequence (fasta), Mean of Poisson Distribution (lamb)
#	Output: Array of error values associated with each base in fasta seq (errors)
# 
#	TODO: 
#		Needs a more accurate method of calculating error
#		Perhaps assign QUAL score instead of error
def assign_error(fasta, lamb):
	errors = []
	for base in fasta:
		errors.append(poisson(lamb)/100.0)
	return errors


#---------Function: induce_error
# 
#	Input: (fasta) Raw FASTA Sequence, (errors) Associated Array of Errors
#	Output: (new_fasta) New FASTA Sequence with added errors
# 
#	TODO: 
#
def induce_error(fasta, errors):
	new_fasta = ""
	for i in range(len(fasta)):
		if random() < errors[i]:
			new_base = bases[int(random()*4)]
			while new_base == fasta[i]:
				new_base = bases[int(random()*4)]
			new_fasta += new_base
		else:
			new_fasta += fasta[i]
	return new_fasta

#---------Function: create_quality_string
# 
#	Input: (errors) Array of Errors 
#	Output: (fastq) String of ASCII characters representing error values in (errors)
# 
#	TODO: 
#		Add compatibility with other sequencers
def create_quality_string(errors):
	fastq = ""
	for error in errors:
		QUAL = int(round(-10*log(error/(1-error),10)))   #These are mappings for Illumina 1.8+
		fastq += chr(QUAL+33)
	return fastq

#---------Function: read_fasta
# 
#	Input: (filename) Name of fasta file
#	Output: (fas) Array of fasta objects from Biopython 
# 
#	TODO: 
#		
def read_fasta(filename):
	fas = SeqIO.parse(open(filename,'r'),'fasta')
	return fas

def main():
	fasta_raw='AAAAAAAAAA'	
	mean_error = 20  #Assume Sequencing Machine has 2% error
	
	fastaread_fasta('example.fasta')
	errors = assign_error(fasta_raw, mean_error)
	new_fasta = induce_error(fasta_raw,errors)
	fastq_quality_string = create_quality_string(errors)
	

if __name__ == '__main__':
	main()