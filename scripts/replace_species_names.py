import re
import sys

def remove_names_from_tree(infile, outfile, species):
	file = open(infile,'r')
	line = file.readline()
	file.close()

	rx = re.compile("'*[A-Z][a-z]+\s*[a-z]*-*[a-z]*'*", re.UNICODE)
	names = rx.findall(line)


	file = open(species,'w')

	for i in range(len(names)):
		file.write('PL'+str(i+1) + '\t' + names[i].replace("'","") + '\n')
		line =line.replace(names[i], 'PL'+str(i+1))
	file.close()


	file = open(outfile,'w')
	file.write(line)
	file.write('\n')
	file.close()

def insert_names_into_tree(infile, outfile, species):
	file = open(infile,'r')
	tree = file.readline()
	file.close()

	file = open(species,'r')
	line = file.readline()
	while(line):
		line = line.strip().split('\t')
		tree = tree.replace(line[0]+':',"'"+line[1]+"':")
		line = file.readline()
	file.close()

	file = open(outfile,'w')
	file.write(tree+'\n')
	file.close()

def main():
	infilename = sys.argv[1]
	outtreefilename = sys.argv[2]
	speciesfilename = sys.argv[3]
	oper = sys.argv[4]

	if oper=='remove':
		remove_names_from_tree(infilename, outtreefilename, speciesfilename)

	elif oper=='insert':
		insert_names_into_tree(infilename, outtreefilename, speciesfilename)

	else:
		print "Usage: python replace_species_names.py orig_tree.tree new_tree.tree species_names.txt operation(remove/insert)"
		print "Error: Operation must be either 'remove' or 'insert'"

if __name__ == '__main__':
	if(len(sys.argv) < 5):
		print "Usage: python replace_species_names.py orig_tree.tree new_tree.tree species_names.txt operation(remove/insert)"
		exit(1)
	main()