data="/Users/justinbricker/Playground/error/data"
scripts="/Users/justinbricker/Playground/error/scripts"

#Step 1:  Generate the sequence files using a tree as input
#	-m (model)  HKY
#	-o (output type) Phylip
#	-q (quiet)
#	-l (length) 1000
seq-gen -mHKY $data/example.tree -op -q -l1000 >> $data/sequences.phy

#Step 2: Convert seqeunces from phylip to FASTA format
#	Input: $data/sequences.phy
#	Output: $data/sequences.fasta
python $scripts/phylipToFASTA.py $data/sequences.phy $data/sequences.fasta

