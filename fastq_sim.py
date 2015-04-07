#!/usr/local/bin/python
from numpy.random import poisson

#---------Function: assign_error
# 
#	Input: Raw FASTA Sequence (fasta), Mean of Poisson Distribution (lamb)
#	Output: Array of error values associated with each base in fasta seq (errors)
# 
#	TODO: Needs a more accurate method of calculating error
def assign_error(fasta, lamb):
	global errors
	errors = []
	for base in fasta:
		errors.append(poisson(lamb)/100.0)
	return errors

def main():
	fasta_raw='ATATCGGATCTAGGATTCGGATTAGGAATTCGAAA'	
	mean_error = 2  #Assume Sequencing Machine has 2% error
	errors = assign_error(fasta_raw, mean_error)
	print errors

if __name__ == '__main__':
	main()