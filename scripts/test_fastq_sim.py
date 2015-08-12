import unittest, fastq_sim as fs, os
from math import log
from scipy import stats
from random import random
import numpy as np
import fastq_filter as ff


bases = ['A','T','C','G']
quals = "!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHI"


# Test to Make Sure that the assign_error function is opererating correctly
class AssignErrorTest(unittest.TestCase):
	def setUp(self):
		self.error_mean = 0.15;
		self.seq = 'AAA'*1000000
		self.errors = fs.assign_error(self.seq, self.error_mean)
		print("Mean of Errors: ", np.mean(self.errors))
		print("Max of Errors: ",np.max(self.errors))
		

	#test if length of error array is same as original sequence
	def test_error_assign_length(self):
		self.assertEqual(len(self.errors), len(self.seq))

	# test if mean of errors is within a close range of true error mean.
	def test_error_assign_mean(self):  
		mean_of_errors = np.mean(self.errors)
		print mean_of_errors
		self.assertLess(abs(mean_of_errors-self.error_mean), 0.01) 

#Test if error induction method results in a mutated string with teh appropriate error rate
class ErrorInductionTest(unittest.TestCase):
	def setUp(self):
		self.sequence = 'A'*10000
		self.error_rate = 0.05
		self.errors = fs.assign_error(self.sequence, self.error_rate)
		self.error_seq = fs.induce_error(self.sequence, self.errors)

	#test if percent of errors in new sequence agrees with the error rate
	def test_error_induced_percent(self):
		num_error = 0
		for base in self.error_seq:
			if base != 'A':
				num_error +=1
		self.assertLess(stats.binom_test(num_error, len(self.error_seq), self.error_rate*3/4.0), 0.05) #Binomial test with 5% significance
		 # 3/4 factor to account for errors with no change (A -> A)

	#test if length of error sequence is same as original sequence
	def test_error_induced_length(self):
		self.assertEqual(len(self.error_seq), len(self.sequence))		


# Test to make sure quality string method is outputting the correct result
class QualityAssignTest(unittest.TestCase):
	def setUp(self):
		self.errors = []
		self.expected = "!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHI"
		for Q in range(41):
			self.errors.append(10.0**(-Q/10.0))
		self.fastq_string = fs.create_quality_string(self.errors)

	#test if correct ascii characters are generated for Illumina 1.8+ with errors in full range
	def test_illumina_ascii(self):
		self.assertEqual(self.fastq_string,self.expected)

	#test if the quality string is the correct length
	def test_quality_string_length(self):
		self.assertEqual(len(self.fastq_string),len(self.expected))

# Test to make sure output as FASTQ function works properly
class FastqOutputTest(unittest.TestCase):
	def setUp(self):
		self.filename = 'testfile.fasta'
		self.seq_name = 'TestSequence'
		self.error_seq = 'ATCCGATCCG'
		self.qualityString = ''
		for base in self.error_seq:  #Random QUALS
			self.qualityString += quals[int(random()*len(self.error_seq))]
		
		self.outfile = open(self.filename.split('.')[0]+".FASTQ",'w')
		fs.output_fastq_file(self.outfile, self.seq_name, self.error_seq, self.qualityString) #outputs to testfile.fasta.FASTQ
		self.outfile.close()

		self.file = open('testfile.FASTQ','r')
		self.name_line = self.file.readline().strip()
		self.seq_line = self.file.readline().strip()
		self.plus_line = self.file.readline().strip()
		self.qual_line = self.file.readline().strip()
		self.file.close()

	#test if the name line in FASTQ file is correct
	def test_fastq_out_name(self):
		self.assertEqual(self.name_line, "@"+self.seq_name)

	#test if the sequence line in FASTQ file is correct
	def test_fastq_out_seq(self):
		self.assertEqual(self.seq_line, self.error_seq)

	#test if the plus line in FASTQ file is correct
	def test_fastq_out_plus(self):	
		self.assertEqual(self.plus_line, '+')

	#test if the quality string line in FASTQ file is correct
	def test_fastq_out_quals(self):
		self.assertEqual(self.qual_line, self.qualityString)

	def tearDown(self):
		os.remove('testfile.FASTQ')

#Test to make sure output as FASTQ function works properly when multiple sequences present
class MainTest(unittest.TestCase):
	def setUp(self):
		#Generate a fasta file with multiple sequences
		self.filename = 'testfile.fasta'
		self.num_seq = 10
		self.infile = open('testfile.fasta','w')
		for i in range(self.num_seq):
			self.infile.write(">TestSeq%s\n"%(i+1))
			seq = bases[(i%4)]*50
			self.infile.write("%s\n"%seq)
		self.infile.close()

		#Pass fasta through the main method with arbitrary 5% error
		fs.main(self.filename, 0.05)

		#Observe the output file and check
		self.outfile = open('testfile.FASTQ','r')
		self.seqs = self.outfile.readlines()
		self.outfile.close()

	#test if the correct number of lines appear in the output file
	def test_num_output_lines(self):
		self.assertEqual(len(self.seqs),4*self.num_seq)

	#test if the 5th line in the output file is the correct name of the 2nd sequence
	def test_second_name(self):
		self.assertEqual(self.seqs[4].strip(),"@TestSeq2")

	#test if the 11th line in the output file contains only '+'
	def test_third_plus(self):
		self.assertEqual(self.seqs[10].strip(),'+')

	def tearDown(self):
		os.remove('testfile.fasta')
		os.remove('testfile.FASTQ')

if __name__ == '__main__':
	unittest.main()