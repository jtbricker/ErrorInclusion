data="data"
scripts="scripts"

filter_threshold=15

#3 Variants: Standard FASTA (A), Preprocessed FASTQ as FASTA (B), FASTQ with likelihood modification (C)

#Step 1:(ABC)  Generate the sequence files using a tree as input
#	-m (model)  HKY
#	-o (output type) Phylip
#	-q (quiet)
#	-l (length) 1000
seq-gen -mHKY $data/example.tree -op -q -l1000 >> $data/inseq.phy

#Step 2:(ABC) Convert seqeunces from phylip to FASTA format, remove unneeded phy file
#	Input: $data/sequences.phy
#	Output: $data/sequences.fasta
python $scripts/phylipToFASTA.py $data/inseq.phy $data/inseq.fasta
cp $data/inseq.fasta $data/inseq_RAW.fasta
rm $data/inseq.phy

#Step 3:(BC) Generate simulated FASTQ file from the FASTA file.
python $scripts/fastq_sim.py $data/inseq.fasta
cp $data/inseq.fastq  $data/inseq_FASTQ.fastq

#Step 4:(B) Run FASTQ file through some preprocessor
python $scripts/fastq_filter.py $data/inseq.fastq $filter_threshold
python $scripts/fastq_filter.py $data/inseq_FASTQ.fastq $filter_threshold  #Temporary

#Step 5:(ABC) Generate XML file for beast using FASTA/FASTQ files
python $scripts/fastxToBeauti.py $data/inseq_RAW.fasta   #RAW FASTA
python $scripts/fastxToBeauti.py $data/inseq_FILTERED.fasta  #FASTA FROM FILTERED FASTQ
python $scripts/fastxToBeauti.py $data/inseq_FASTQ_FILTERED.fastq #SIMULATED FASTQ


#Step 6:(ABC) Run beast
beast -overwrite -working $data/inseq_RAW_beauti.xml
beast -overwrite -working $data/inseq_FILTERED_beauti.xml
beast -overwrite -working $data/inseq_FASTQ_FILTERED_beauti.xml

#Step 7:(ABC) Annotate trees
treeannotator $data/inseq_RAW.trees $data/RAW_tree.nex
treeannotator $data/inseq_FILTERED.trees $data/FILTERED_tree.nex
treeannotator $data/inseq_FASTQ_FILTERED.trees $data/FASTQ_tree.nex

#Step 8:(ABC) Convert trees into newick format
cat $data/example.tree | sed 's/Taxon//g' > $data/example.tre
cat $data/RAW_tree.nex | grep ^tree | tr '[]' '\n' | grep -v ^\& | tr -d ' \n' | sed 's/^tree.*=//' > $data/RAW_tree.tre
cat $data/FILTERED_tree.nex | grep ^tree | tr '[]' '\n' | grep -v ^\& | tr -d ' \n' | sed 's/^tree.*=//' > $data/FILTERED_tree.tre
cat $data/FASTQ_tree.nex | grep ^tree | tr '[]' '\n' | grep -v ^\& | tr -d ' \n' | sed 's/^tree.*=//' > $data/FASTQ_tree.tre

#Step 8.5: Concat trees together
rm $data/intree
cat $data/example.tre >> $data/intree
cat $data/RAW_tree.tre >> $data/intree
cat $data/FILTERED_tree.tre >> $data/intree
cat $data/FASTQ_tree.tre >> $data/intree


#Step 9:(ABC) Measure tree distance
cd data; printf 'R\n2\nP\nF\nY\n' | treedist

#geodesic
#mary kuhner
#