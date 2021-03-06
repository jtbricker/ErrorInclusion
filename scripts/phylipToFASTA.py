import sys

def main(filename, outfile_name):
	try:
		file = open(filename,'r')
	except:
		print "Error: Cannot open filename: %s"%filename
		exit(1)

	header = file.readline().strip().split()
	num_seqs = int(header[0])
	seq_length = int(header[1])

	outfile = open(outfile_name,'w')
	for i in range(num_seqs):
		seq  =file.readline().strip().split()
		outfile.write('>%s\n'%seq[0])
		outfile.write('%s\n'%seq[1])

	outfile.close()
	file.close()
if __name__=='__main__':
	try:
		filename = sys.argv[1]
		outfile_name = sys.argv[2]
	except:
		print "Usage: phylipToFASTA infile.phylip outfile.FASTA"
		exit(0);

	main(filename, outfile_name)

	