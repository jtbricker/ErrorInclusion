data="data"
scripts="scripts"

#3 Variants: Standard FASTA (A), Preprocessed FASTQ as FASTA (B), FASTQ with likelihood modification (C)

#Step 1:(ABC)  Generate the sequence files using a tree as input
#	-m (model)  HKY
#	-o (output type) Phylip
#	-q (quiet)
#	-l (length) 1000
seq-gen -mHKY $data/example.tree -op -q -l1000 >> $data/sequences.phy

#Step 2:(ABC) Convert seqeunces from phylip to FASTA format
#	Input: $data/sequences.phy
#	Output: $data/sequences.fasta
python $scripts/phylipToFASTA.py $data/sequences.phy $data/sequences.fasta

#Step 3:(BC) Generate simulated FASTQ file from the FASTA file.
python $scripts/fastq_sim.py $data/sequences.fasta

#Step 4:(B) Run FASTQ file through some preprocessor

#Step 4b:(B) Convert FASTQ to FASTA

#Step 5:(ABC) Generate XML file for beast using FASTA/FASTQ files

#Step 6:(ABC) Run beast
beast -overwrite -working $data/beauti_template.xml

#Step 7:(ABC) Annotate trees
treeannotator $data/sequences.trees $data/treeA.nex

#Step 8:(ABC) Convert trees into newick format
phyutility -vert -in $data/treeA.nex -out $data/treeA.tre

#Step 8.5: Concat trees together
cat $data/example.tree >> $data/treeABC.tre
cat $data/treeA.tre >> $data/treeABC.tre
# cat treeB.tre >> treeABC.tre
# cat treeC.tre >> treeABC.tre

#Step 9:(ABC) Measure tree distance