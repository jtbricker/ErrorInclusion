data="data"
scripts="scripts"

rm launchfile_temp

filter_threshold=15


for REP in {1..100}
do
	#3 Variants: Standard FASTA (A), Preprocessed FASTQ as FASTA (B), FASTQ with likelihood modification (C)

	#Step 1:(ABC)  Generate the sequence files using a tree as input
	#	-m (model)  HKY
	#	-o (output type) Phylip
	#	-q (quiet)
	#	-l (length) 1000
	seq-gen -mHKY $data/example.tree -op -q -l1000 >> $data/inseq_$REP.phy

	#Step 2:(ABC) Convert seqeunces from phylip to FASTA format, remove unneeded phy file
	#	Input: $data/sequences.phy
	#	Output: $data/sequences.fasta
	python $scripts/phylipToFASTA.py $data/inseq_$REP.phy $data/inseq_$REP.fasta
	cp $data/inseq_$REP.fasta $data/inseq_RAW_$REP.fasta
	rm $data/inseq_$REP.phy

	#Step 3:(BC) Generate simulated FASTQ file from the FASTA file.
	python $scripts/fastq_sim.py $data/inseq_$REP.fasta
	cp $data/inseq_$REP.fastq  $data/inseq_FASTQ_$REP.fastq

	#Step 4:(B) Run FASTQ file through some preprocessor
	python $scripts/fastq_filter.py $data/inseq_$REP.fastq $filter_threshold
	python $scripts/fastq_filter.py $data/inseq_FASTQ_$REP.fastq $filter_threshold  #Temporary

	#Step 5:(ABC) Generate XML file for beast using FASTA/FASTQ files
	python $scripts/fastxToBeauti.py $data/inseq_RAW_$REP.fasta   #RAW FASTA
	python $scripts/fastxToBeauti.py $data/inseq_$REP_FILTERED.fasta  #FASTA FROM FILTERED FASTQ
	python $scripts/fastxToBeauti.py $data/inseq_FASTQ_$REP_FILTERED.fastq #SIMULATED FASTQ


	#Step 6:(ABC) Run beast
	echo beast_submit beast $data/inseq_RAW_$REP_beauti.xml 1 04:00:00 >> launchfile_temp
	echo beast_submit beast $data/inseq__$REPFILTERED_beauti.xml 1 04:00:00 >> launchfile_temp
	echo beast_submit beast $data/inseq_FASTQ_$REP_FILTERED_beauti.xml 1 04:00:00 >> launchfile_temp

	#cp launchfile_temp ~/launchfile
	#################################################################
	#####  BREAK!!!! Need to RUN jobs before rest of pipeline  ######
	#################################################################

	# # #Step 7:(ABC) Annotate trees
	# treeannotator $data/inseq_RAW_$REP.trees $data/RAW_tree_$REP.nex
	# treeannotator $data/inseq_$REP_FILTERED.trees $data/FILTERED_tree_$REP.nex
	# treeannotator $data/inseq_$REP_FASTQ_FILTERED.trees $data/FASTQ_tree_$REP.nex

	# # #Step 8:(ABC) Convert trees into newick format
	# cat $data/example.tree | sed 's/Taxon//g' > $data/example.tre
	# cat $data/RAW_tree_$REP.nex | grep ^tree | tr '[]' '\n' | grep -v ^\& | tr -d ' \n' | sed 's/^tree.*=//' > $data/RAW_tree_$REP.tre
	# cat $data/FILTERED_tree_$REP.nex | grep ^tree | tr '[]' '\n' | grep -v ^\& | tr -d ' \n' | sed 's/^tree.*=//' > $data/FILTERED_tree_$REP.tre
	# cat $data/FASTQ_tree_$REP.nex | grep ^tree | tr '[]' '\n' | grep -v ^\& | tr -d ' \n' | sed 's/^tree.*=//' > $data/FASTQ_tree_$REP.tre

	# # #Step 8.5: Concat trees together
	# rm $data/intree
	# cat $data/example.tre >> $data/intree_$REP
	# cat $data/RAW_tree_$REP.tre >> $data/intree_$REP
	# cat $data/FILTERED_tree_$REP.tre >> $data/intree_$REP
	# cat $data/FASTQ_tree_$REP.tre >> $data/intree_$REP


	# #Step 9:(ABC) Measure tree distance
	# cd data; printf '$data/intree_$REP\nR\n2\nP\nF\nY\n' | treedist
done	