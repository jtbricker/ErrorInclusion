import fastq_filter as ff
import sys

a = sys.argv[1]


stringInsert = ""

names, seqs, quals = ff.get_sequences(a)


dataID = a.split('.py')


stringInsert = stringInsert + '<data id=' + dataID[0] + ' name=\"alignment"> \n'


for i in range( 1, len( names ) ):
    stringInsert = stringInsert + '<sequence id="seq_'         
    stringInsert = stringInsert + names[i]
    stringInsert = stringInsert + '" '
    stringInsert = stringInsert + 'taxon='
    stringInsert = stringInsert + '"'
    stringInsert = stringInsert + names[i]
    stringInsert = stringInsert + '" '
    stringInsert = stringInsert + 'totalcount="4" value= "'
    stringInsert = stringInsert + seqs[i]
    stringInsert = stringInsert + '" > \n'
   



stringInsert = stringInsert + '</data> \n' 


#print(stringInsert)

b = open( 'beauti2.xml', 'r')

readInFile = b.readlines()

b.close()

for i in range( len(readInFile)):
    if( readInFile[i].strip() == "123template123"):
	    readInFile[i] = stringInsert
	    
c = open( 'product.xml', 'w')

for i in range( len(readInFile)):
    c.write( readInFile[i] )
