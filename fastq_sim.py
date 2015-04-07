#!/usr/local/bin/python
from numpy.random import poisson
from random import random

bases = ['A','T','C','G']

#---------Function: assign_error
# 
#	Input: Raw FASTA Sequence (fasta), Mean of Poisson Distribution (lamb)
#	Output: Array of error values associated with each base in fasta seq (errors)
# 
#	TODO: Needs a more accurate method of calculating error
def assign_error(fasta, lamb):
	errors = []
	for base in fasta:
		errors.append(poisson(lamb)/100.0)
	return errors


#---------Function: induce_error
# 
#	Input: Raw FASTA Sequence (fasta), Associated Array of Errors (errors)
#	Output: New FASTA Sequence with added errors (new_fasta)
# 
#	TODO: 
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


def main():
	fasta_raw='AAAAAAAAAA'	
	mean_error = 20  #Assume Sequencing Machine has 2% error
	errors = assign_error(fasta_raw, mean_error)
	new_fasta = induce_error(fasta_raw,errors)
	print new_fasta

if __name__ == '__main__':
	main()