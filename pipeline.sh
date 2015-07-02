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
	seq-gen -mHKY $data/example.tree -op -q -l1000 >> $data/$REP_inseq.phy

	#Step 2:(ABC) Convert seqeunces from phylip to FASTA format, remove unneeded phy file
	#	Input: $data/sequences.phy
	#	Output: $data/sequences.fasta
	python $scripts/phylipToFASTA.py $data/$REP_inseq.phy $data/$REP_inseq.fasta
	cp $data/$REP_inseq.fasta $data/$REP_inseq_RAW.fasta
	rm $data/$REP_inseq.phy

	#Step 3:(BC) Generate simulated FASTQ file from the FASTA file.
	python $scripts/fastq_sim.py $data/$REP_inseq.fasta
	cp $data/$REP_inseq.fastq  $data/$REP_inseq_FASTQ.fastq

	#Step 4:(B) Run FASTQ file through some preprocessor
	python $scripts/fastq_filter.py $data/$REP_inseq.fastq $filter_threshold
	python $scripts/fastq_filter.py $data/$REP_inseq_FASTQ.fastq $filter_threshold  #Temporary

	#Step 5:(ABC) Generate XML file for beast using FASTA/FASTQ files
	python $scripts/fastxToBeauti.py $data/$REP_inseq_RAW.fasta   #RAW FASTA
	python $scripts/fastxToBeauti.py $data/$REP_inseq_FILTERED.fasta  #FASTA FROM FILTERED FASTQ
	python $scripts/fastxToBeauti.py $data/$REP_inseq_FASTQ_FILTERED.fastq #SIMULATED FASTQ


	#Step 6:(ABC) Run beast
	echo beast_submit beast $data/$REP_inseq_RAW_beauti.xml 1 04:00:00 >> launchfile_temp
	echo beast_submit beast $data/$REP_inseq_FILTERED_beauti.xml 1 04:00:00 >> launchfile_temp
	echo beast_submit beast $data/$REP_inseq_FASTQ_FILTERED_beauti.xml 1 04:00:00 >> launchfile_temp

	#cp launchfile_temp ~/launchfile
	#################################################################
	#####  BREAK!!!! Need to RUN jobs before rest of pipeline  ######
	#################################################################

	# # #Step 7:(ABC) Annotate trees
	# treeannotator $data/$REP_inseq_RAW.trees $data/$REP_RAW_tree.nex
	# treeannotator $data/$REP_inseq_FILTERED.trees $data/$REP_FILTERED_tree.nex
	# treeannotator $data/$REP_inseq_FASTQ_FILTERED.trees $data/$REP_FASTQ_tree.nex

	# # #Step 8:(ABC) Convert trees into newick format
	# cat $data/example.tree | sed 's/Taxon//g' > $data/example.tre
	# cat $data/$REP_RAW_tree.nex | grep ^tree | tr '[]' '\n' | grep -v ^\& | tr -d ' \n' | sed 's/^tree.*=//' > $data/$REP_RAW_tree.tre
	# cat $data/$REP_FILTERED_tree.nex | grep ^tree | tr '[]' '\n' | grep -v ^\& | tr -d ' \n' | sed 's/^tree.*=//' > $data/$REP_FILTERED_tree.tre
	# cat $data/$REP_FASTQ_tree.nex | grep ^tree | tr '[]' '\n' | grep -v ^\& | tr -d ' \n' | sed 's/^tree.*=//' > $data/$REP_FASTQ_tree.tre

	# # #Step 8.5: Concat trees together
	# rm $data/$REP_intree
	# cat $data/example.tre >> $data/$REP_intree
	# cat $data/$REP_RAW_tree.tre >> $data/$REP_intree
	# cat $data/$REP_FILTERED_tree.tre >> $data/$REP_intree
	# cat $data/$REP_FASTQ_tree.tre >> $data/$REP_intree


	# #Step 9:(ABC) Measure tree distance
	# cd data; printf $data/$REP'_intree\nR\n2\nP\nF\nY\n' | treedist
done	