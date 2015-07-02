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


