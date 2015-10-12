import fastq_filter as ff
from fastq_filter import char_to_qual
from fastq_sim import qual_to_error
import sys
import os

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
    dataID = a.split('.fastq')[0].split('.fasta')[0].split('/')[-1]
    stringInsert = stringInsert + '<data id="' + dataID + '" name=\"alignment"> \n'
    for i in range( len( names ) ):
        stringInsert = stringInsert + '<sequence id="seq_'         
        stringInsert = stringInsert + names[i]
        stringInsert = stringInsert + '" '
        stringInsert = stringInsert + 'taxon='
        stringInsert = stringInsert + '"'
        stringInsert = stringInsert + names[i]
        stringInsert = stringInsert + '" '
        stringInsert = stringInsert + 'sequenceData="'
        stringInsert = stringInsert + seqs[i] + '">\n'
        if quals:
            stringInsert = stringInsert + '\t<![CDATA[\n'
            stringInsert = stringInsert + '\t\t' + quals[i] + '\n'
            stringInsert = stringInsert + '\t]]>\n'
        stringInsert = stringInsert + '</sequence>\n'
    stringInsert = stringInsert + '</data>\n' 
    return stringInsert, dataID;

#---------Function: build_beauti_prbs_string
# 
#   Input: (filename) filename of fastx file, (names, seqs, quals) arrays of names, seqs, quals from sequences in fastx
#   Output: (stringInsert) string with the PROBABILITY sequence tag to be inserted into the beauti template file
# 
#   TODO: Handle fasta data/fastq
#       
def build_beauti_prbs_string(filename, names, seqs, quals):
    a = filename
    stringInsert = ""
    dataID = a.split('.fastq')[0].split('.fasta')[0].split('/')[-1]
    stringInsert = stringInsert + '<data id="' + dataID + '" name="alignment"> \n'
    for i in range( len( names ) ):
        stringInsert = stringInsert + '<sequence id="seq_'         
        stringInsert = stringInsert + names[i]
        stringInsert = stringInsert + '" '
        stringInsert = stringInsert + 'taxon='
        stringInsert = stringInsert + '"'
        stringInsert = stringInsert + names[i] + '">\n'
        stringInsert = stringInsert + '\t' + build_probs_string(seqs[i],quals[i]) + '\n'
        stringInsert = stringInsert + '</sequence>\n'
    stringInsert = stringInsert + '</data>\n' 
    return stringInsert, dataID;

#---------Function: build_probs_str
# 
#   Input: (sequence_str, quality_str) sequence string, quality string
#   Output: (probs_str) string of comma spaced likelihoods for each base ending with semicolon
# 
#       
def build_probs_string(sequence_str, quality_str):
    full_probs_str = ""
    for i in range(len(sequence_str)):
        full_probs_str = full_probs_str + uncertain_base_to_probs(sequence_str[i], quality_str[i])
    return full_probs_str


#---------Function: uncertain_base_to_probs
# 
#   Input: (base, quality_str) nucleotide base, quality character
#   Output: (probs_str) comma spaced likelihoods for each base ending with semicolon
# 
#       
def uncertain_base_to_probs(base, quality_char):
    bases = {'A':0, 'C':1,'G':2,'T':3}
    error = qual_to_error(char_to_qual(quality_char))
    probs = [error/3]*4
    probs[bases[base]] = 1 - error;
    probs_str = ','.join('{:f}'.format(x) for x in probs)+";"
    return probs_str
    


#---------Function: output_beauti_file
# 
#   Input: (stringInsert) string with sequence tag to be inserted, (outfilename) name of the beauti xml file to be created
#   Output: --none-- Generates beauti config file, inserting stringInsert into the SEQUENCE_TEMPLATE location
# 
#   TODO: Handle quality data when applicable
#       
def output_beauti_file(stringInsert, outfilename, dataID):
    b = open( 'data/beauti_template.xml', 'r')
    readInFile = b.readlines()
    b.close()

    for i in range( len(readInFile)):
        if( readInFile[i].strip() == "SEQUENCE_TEMPLATE"):
    	    readInFile[i] = stringInsert
    	    
    c = open( outfilename, 'w')
    for i in range( len(readInFile)):
        c.write( readInFile[i] )
    c.close();
    os.system("perl -p -i -e 's/SEQ_ID_NAME/"+dataID+"/g' "+outfilename)


#---------Function: main
# 
#   Input: (filename) string indicating the name of the FASTX that wil be used in BEAST
#   Output: --none-- Runs all methods and outputs BEAUTI XML file
# 
#   TODO: Handle FASTA/FASTQ
#       
def main(filename, probsFmt=False):
    quals = False #placeholder
    #get sequences from file
    if(filename.split('.')[-1].lower() == 'fastq'):
        names, seqs, quals = ff.get_sequences(filename)
    elif(filename.split('.')[-1].lower() == 'fasta'):
        names, seqs = ff.get_fasta_sequences(filename)
    else:
        print "Wrong filetype: Must provide with fasta/FASTA or fastq/FASTQ file"
        exit(1);
    #build beauti string
    if probsFmt:
        template_insert, dataID = build_beauti_prbs_string(filename,names,seqs,quals)
    else:
        template_insert, dataID = build_beauti_string(filename,names,seqs,quals)

    #create output file
    outfilename = filename.split('.fast')[0]+'_beauti.xml'
    output_beauti_file(template_insert, outfilename, dataID)

if __name__=='__main__':
    try:
        filename = sys.argv[1]
    except:
        print "Usage: fastxToBeauti.py infile.FASTX"
        exit(0);

    main(filename)    
