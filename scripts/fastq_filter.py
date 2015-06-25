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
#	Output: --none-- Runs all methods and creates FASTQ/FASTA file of modified sequence data
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

#---------Function: main
# 
#	Input: (filename) string indicating the name of the FASTQ file you want to filter on, (threshold) minimum quality score to keep
#	Output: --none-- Runs all methods and creates FASTQ/FASTA file of modified sequence data
# 
#	TODO: Add optional arguments (sequencing machine for example)
#		
def main(filename, threshold):
	names, seqs, quals = get_sequences(filename)


	indicies = []
	newSeqs = []
	newQuals = []
	#print( quals)
	
	for i in range( len(quals) ):
		for j in range( len(quals[i])):
			#print( type( char_to_qual( quals[i][j] ) ) )
			#print( type( threshold ))
			#print(  char_to_qual(quals[i][j])  >  threshold )
			if char_to_qual(quals[i][j]) > int( threshold):
				continue
			else:
				#print("hello")
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
		
	#print newSeqs
	#print newQuals
	
	a = open( 'FastqFilter.FASTQ', 'w')
	
	for i in range( len(names)):
		a.write( "@" + names[i] + "\n")
		a.write( newSeqs[i] + "\n")
		a.write("+" + "\n")
		a.write( newQuals[i] + "\n")
	a.close()
	



if __name__ == '__main__':
	if len(sys.argv) <3 :
		print "Usage: python fastq_sim file.fasta threshold"
		exit(1)
	main(sys.argv[1], sys.argv[2])
	
