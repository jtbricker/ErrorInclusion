#!/usr/local/bin/python
from math import log
import sys



#---------Function: char_to_qual
# 
#	Input: (char) ASCII character representing quality score 
#	Output: (qual) Quality score integer value indicated by ASCII quality character
# 
#	TODO: Support various machines (only Ilumina 1.8+ now)
#		
def char_to_qual(char):
	seq_machine_mod = 33
	return ord(char)-seq_machine_mod

#---------Function: get_sequences
# 
#	Input: (filename) string indicating the name of the FASTQ file you want to filter on
#	Output: (names, seqs, quals) Arrays containing the names, sequences, and quality strings of all the indivduals from the inputted FASTQ file
# 
#	TODO: 
#		
def get_sequences(filename):
	file = open(filename,'r')
	names = []
	seqs = []
	quals = []
	line = file.readline()
	while(line):
		names.append(line[1:].strip())
		seqs.append(file.readline().strip())
		file.readline() # '+' line
		quals.append(file.readline().strip())
		line = file.readline()
	file.close()
	return names, seqs, quals

#---------Function: get_fasta_sequences
# 
#	Input: (filename) string indicating the name of the FASTA file you want to get name/seq data from
#	Output: (names, seqs) Arrays containing the names and sequences of all the indivduals from the inputted FASTA file
# 
#	TODO: 
#		
def get_fasta_sequences(filename):
	file = open(filename,'r')
	names = []
	seqs = []
	line = file.readline()
	while(line):
		names.append(line[1:].strip())
		seqs.append(file.readline().strip())
		line = file.readline()
	file.close()
	return names, seqs



#---------Function: filter_reads
#
#	This function takes in an array of alligned sequences (and their associated quality scores)
#	and outputs removes "columns" from this allignment where at least one of the quality score
#	falls below the threshold passed in. Returns filtered seqs and quals.
# 
#	Input: (seqs, quals, threshold) arrays sequences and quality strings, quality threshold value
#	Output: (newSeqs, newQuals) arrays containing the 
# 
#	TODO: 
#		
def filter_reads(seqs, quals, threshold):
	indicies = []
	newSeqs = []
	newQuals = []
	
	for i in range( len(quals) ):
		for j in range( len(quals[i])):
			if char_to_qual(quals[i][j]) > int( threshold):
				continue
			else:
				indicies.append(j)
			
	for i in range( len(seqs) ):
		temp = ""
		temp2 = ""
		for j in range( len(seqs[i]) ):
			if j in indicies:
				continue
			else:
				temp += seqs[i][j]
				temp2 += quals[i][j]
		newSeqs.append( temp )
		newQuals.append( temp2)

	return newSeqs,newQuals

#---------Function: output_fastq
# 
#	Input: (fastq_filename,names, seqs, quals) arrays sequences and quality strings, quality threshold value
#	Output: (none) creates new fastq file with name fastq_filtered_filename
# 
#	TODO: 
#		
def output_fastq(fastq_filtered_filename, names, newSeqs, newQuals):
	a = open( fastq_filtered_filename, 'w')
	
	for i in range( len(names)):
		a.write( "@" + names[i] + "\n")
		a.write( newSeqs[i] + "\n")
		a.write("+" + "\n")
		a.write( newQuals[i] + "\n")
	a.close()


#---------Function: output_fasta
# 
#	Input: (fastq_filename,names, seqs) arrays sequences and quality strings
#	Output: (none) creates new fasta file with name fasta_filtered_filename
# 
#	TODO: 
#		
def output_fasta(fasta_filtered_filename, names, newSeqs):
	a = open( fasta_filtered_filename, 'w')
	
	for i in range( len(names)):
		a.write( ">" + names[i] + "\n")
		a.write( newSeqs[i] + "\n")
	a.close()

#---------Function: main
# 
#	Input: (filename) string indicating the name of the FASTQ file you want to filter on, (threshold) minimum quality score to keep
#	Output: --none-- Runs all methods and creates both FASTQ/FASTA file of modified sequence data
# 
#	TODO: Add optional arguments (sequencing machine for example)
#		
def main(filename, threshold):
	file_ext = '.'+filename.split('.')[-1]
	names, seqs, quals = get_sequences(filename)
	newSeqs, newQuals = filter_reads(seqs,quals,threshold)
	fastq_filtered_filename = filename.split(file_ext)[0]+'_FILTERED.fastq'
	output_fastq(fastq_filtered_filename, names, newSeqs, newQuals)
	fasta_filtered_filename = filename.split(file_ext)[0]+'_FILTERED.fasta'
	output_fasta(fasta_filtered_filename, names, newSeqs)
	

if __name__ == '__main__':
	if len(sys.argv) <3 :
		print "Usage: python fastq_sim file.fastq threshold"
		exit(1)
	main(sys.argv[1], sys.argv[2])
	
