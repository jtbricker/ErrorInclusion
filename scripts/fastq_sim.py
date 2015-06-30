#!/usr/local/bin/python
import numpy.random as npr
from math import log
import sys
import numpy as np
import fastq_filter as ff

bases = ['A','T','C','G']
seed = npr.randint(0, 4294967295)
kseed = 828459089
npr.seed(seed)
#print seed


#---------Function: assign_error
# 
#	Input: (fasta) Raw FASTA Sequence, (mu) Mean of Errors 
#	Output: (errors) Array of error values associated with each base in fasta seq 
# 
#	TODO: 
#		Needs a more accurate method of calculating error
#		Perhaps assign QUAL score instead of error
#		Assign error based on position in sequence
def assign_error(seq, alpha=1.2, beta=58.8, sigma=1):
	errors=npr.beta(alpha, beta, len(seq)) 
	#import matplotlib.pyplot as plt 
	#plt.hist(errors,bins=np.linspace(0,1,1000))
	#plt.show()
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
		if npr.random() < errors[i]:
			new_base = bases[int(npr.random()*4)]
			while new_base == fasta[i]:
				new_base = bases[int(npr.random()*4)]
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
		try:
			QUAL = int(round(-10*log(error/(1-error),10)))   #These are mappings for Illumina 1.8+
		except:
			print 'Some kind of math error.  Random seed:  ' + str(seed)
			print 'Tried to run code: int(round(-10*log(error/(1-error),10)))'
			print error
			exit(1)
		#print QUAL+33>=33
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
	#mean_error = 0.02  #Assume Sequencing Machine has 2% error
	
	names, sequences = ff.get_fasta_sequences(filename)
	errors = []
	new_sequences = []
	quals = []
	outfile = open(filename[0:filename.lower().rfind('.fasta')] + ".fastq",'w')
	for i in range(len(sequences)):
		errors.append(assign_error(sequences[i]))
		new_sequences.append(induce_error(sequences[i],errors[i]))
		quals.append(create_quality_string(errors[i]))
		output_fastq_file(outfile, str(names[i]), str(sequences[i]), str(quals[i]))
	outfile.close()

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print "Usage: fastq_sim file.fasta"
		exit(1)
	main(sys.argv[1])