import fastq_filter as ff
import sys

#---------Function: build_beauti_string
# 
#   Input: (filename) filename of fastx file, (names, seqs, quals) arrays of names, seqs, quals from sequences in fastx
#   Output: (stringInsert) string with the sequence tag to be inserted into the beauti template file
# 
#   TODO: Handle fasta data/fastq
#       
def build_beauti_string(filename, names, seqs, quals):
    a = filename
    stringInsert = ""
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
    return stringInsert;

#---------Function: output_beauti_file
# 
#   Input: (stringInsert) string with sequence tag to be inserted, (outfilename) name of the beauti xml file to be created
#   Output: --none-- Generates beauti config file, inserting stringInsert into the SEQUENCE_TEMPLATE location
# 
#   TODO: Handle quality data when applicable
#       
def output_beauti_file(stringInsert, outfilename):
    b = open( 'beauti2.xml', 'r')
    readInFile = b.readlines()
    b.close()

    for i in range( len(readInFile)):
        if( readInFile[i].strip() == "SEQUENCE_TEMPLATE"):
    	    readInFile[i] = stringInsert
    	    
    c = open( outfilename, 'w')
    for i in range( len(readInFile)):
        c.write( readInFile[i] )
    c.close();

#---------Function: main
# 
#   Input: (filename) string indicating the name of the FASTX that wil be used in BEAST
#   Output: --none-- Runs all methods and outputs BEAUTI XML file
# 
#   TODO: Handle FASTA/FASTQ
#       
def main(filename):
    #get sequences from file
    names, seqs, quals = ff.get_sequences(a)

    #build beauti string
    template_insert = build_beauti_string(filename,names,seqs,quals)

    #create output file
    outfilename = filename.split('.fast')[0]
    output_beauti_file(template_insert, outfilename)

if __name__=='__main__':
    try:
        filename = sys.argv[1]
    except:
        print "Usage: fastxToBeauti.py infile.FASTX"
        exit(0);

    main(filename)    
