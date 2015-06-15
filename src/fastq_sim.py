#!/usr/local/bin/python
from numpy.random import poisson, lognormal
from random import random
from math import log
from Bio import SeqIO
import sys

bases = ['A','T','C','G']

#---------Function: read_fasta
# 
#	Input: (filename) Name of fasta file
#	Output: (fas) Array of fasta objects from Biopython 
#
#	Notes:  Returns an array of Seq objects from BioPython module.  Can extract
#			sequence with fas[0].seq, or name with  fas[0].name
# 
#	TODO: 	
#		Try and Except opening file
#		Test if output file already exists and warn that it will be deleted?
#		
def read_fasta(filename):
	fas = SeqIO.parse(open(filename,'r'),'fasta')
	return fas

#---------Function: assign_error
# 
#	Input: (fasta) Raw FASTA Sequence, (mu) Mean of Errors 
#	Output: (errors) Array of error values associated with each base in fasta seq 
# 
#	TODO: 
#		Needs a more accurate method of calculating error
#		Perhaps assign QUAL score instead of error
def assign_error(seq, mu, sigma=1):
	errors = []
	for i in range(len(seq)):
		errors.append(lognormal(log(mu), sigma)) 
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
	for i in range(len(errors)):
		error = errors[i]
		QUAL = int(round(-10*log(error/(1-error),10)))   #These are mappings for Illumina 1.8+
		print QUAL
		fastq += chr(QUAL+33)
	return fastq

#---------Function: output_fastq_file
# 
#	Input: (new_seqs) Array of Errors , (quality_string) String of FASTQ ASCII characters
#	Output: --none-- Method Creates FASTQ file of modified sequence data
# 
#	TODO: 
#		
def output_fastq_file(outfile, name, sequence_string, quality_string):
	outfile.write('@'+name+"\n")
	outfile.write(sequence_string + "\n")
	outfile.write('+\n')
	outfile.write(quality_string+'\n')
	#print quality_string
	return 

#---------Function: main
# 
#	Input: (filename) string indicating the name of the FASTA file you want to simulate on 
#	Output: --none-- Runs all methods and creates FASTQ file of modified sequence data
# 
#	TODO: Add optional arguments (sequencing machine or errors for example)
#		
def main(filename):
	mean_error = 0.02  #Assume Sequencing Machine has 2% error
	
	sequences = read_fasta(filename)
	outfile = open(filename + ".FASTQ",'w')
	for sequence in sequences:
		sequence.errors = assign_error(sequence.seq, mean_error)
		sequence.new_seq = induce_error(sequence.seq,sequence.errors)
		sequence.qual = create_quality_string(sequence.errors)
		output_fastq_file(outfile, str(sequence.name), str(sequence.seq), str(sequence.qual))
	outfile.close()

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print "Usage: fastq_sim file.fasta"
		exit(1)
	main(sys.argv[1])