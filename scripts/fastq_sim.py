#!/usr/local/bin/python
import numpy.random as npr
from math import log
import sys
import numpy as np
import fastq_filter as ff
import matplotlib.pyplot as pl

bases = ['A','T','C','G']
seed = npr.randint(0, 4294967295)
kseed = 828459089
npr.seed(seed)
#print seed
PLOT = 0   #Change to 1 to plot a histogram of the errors of the first sequence



#---------Function: assign_error
# 
#	Input: (fasta) Raw FASTA Sequence, (mu) Mean of Errors 
#	Output: (errors) Array of error values associated with each base in fasta seq 
# 
#	TODO: 
#		Needs a more accurate method of calculating error
#		Perhaps assign QUAL score instead of error
#		Assign error based on position in sequence
def assign_error(seq, mu):
	beta = 1
	alpha = (beta * mu) / (1 - mu)
	errors= npr.beta(alpha, beta, len(seq)) 
	global PLOT
	if PLOT:
		plot_errors(errors)
		PLOT = 0;
	return errors


#---------Function: plot_errors
#
#	Input: (errors) Array of Sequence Errors
#	Output: (none) Displays histogram of errors
def plot_errors(errors): 
	pl.hist(errors,bins=np.linspace(0,1,100))
	pl.show()



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
		if error == 0.0:
			error = 1E-100
		# print("whats the prob?:" + str(prob))
		try:
			QUAL = int(round(-10*log(error,10)))   #These are mappings for Illumina 1.8+
			if (QUAL > 41): 
				QUAL = 41
		except:
			print 'Some kind of math error.  Random seed:  ' + str(seed)
			print 'Tried to run code: int(round(-10*log(error,10)))'
			print error
			exit(1)
		#print QUAL>41
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
#	Input: (filename, seq_error) string indicating the name of the FASTA file you want to simulate on , mean sequencing error
#	Output: --none-- Runs all methods and creates FASTQ file of modified sequence data
# 
#	TODO: Add optional arguments (sequencing machine or errors for example)
#		
def main(filename, seq_error):
	#mean_error = 0.02  #Assume Sequencing Machine has 2% error
	seq_error = float(seq_error)
	names, sequences = ff.get_fasta_sequences(filename)
	errors = []
	new_sequences = []
	quals = []
	outfile = open(filename[0:filename.lower().rfind('.fasta')] + ".fastq",'w')
	for i in range(len(sequences)):
		errors.append(assign_error(sequences[i], seq_error))
		new_sequences.append(induce_error(sequences[i],errors[i]))
		quals.append(create_quality_string(errors[i]))
		output_fastq_file(outfile, str(names[i]), str(sequences[i]), str(quals[i]))
	outfile.close()

if __name__ == '__main__':
	if len(sys.argv) < 3:
		print "Usage: fastq_sim file.fasta sequencer_error"
		exit(1)
	main(sys.argv[1], sys.argv[2])

