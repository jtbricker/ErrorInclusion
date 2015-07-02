data="data"
scripts="scripts"

rm launchfile_temp

filter_threshold=15


for REP in {1..100}  #REPLICATES
do
	for F in 5 10 15 20  #FILTER THRESHOLDS (CHANGE FOR FASTQ MUTATION RATE)
	do
	ID=$REP\_F$F
	#3 Variants: Standard FASTA (A), Preprocessed FASTQ as FASTA (B), FASTQ with likelihood modification (C)

	#Step 1:(ABC)  Generate the sequence files using a tree as input
	#	-m (model)  HKY
	#	-o (output type) Phylip
	#	-q (quiet)
	#	-l (length) 1000
	seq-gen -mHKY $data/example.tree -op -q -l1000 >> $data/$ID\_inseq.phy

	#Step 2:(ABC) Convert seqeunces from phylip to FASTA format, remove unneeded phy file
	#	Input: $data/sequences.phy
	#	Output: $data/sequences.fasta
	python $scripts/phylipToFASTA.py $data/$ID_inseq.phy $data/$ID\_inseq.fasta
	cp $data/$ID\_inseq.fasta $data/$ID\_inseq\_RAW.fasta
	rm $data/$ID\_inseq.phy

	#Step 3:(BC) Generate simulated FASTQ file from the FASTA file.
	python $scripts/fastq_sim.py $data/$ID\_inseq.fasta
	cp $data/$ID\_inseq.fastq  $data/$ID\_inseq\_FASTQ.fastq

	#Step 4:(B) Run FASTQ file through some preprocessor
	python $scripts/fastq_filter.py $data/$ID\_inseq\_RAW.fasta 0
	python $scripts/fastq_filter.py $data/$ID\_inseq.fastq $filter_threshold
	python $scripts/fastq_filter.py $data/$ID\_inseq\_FASTQ.fastq $filter_threshold  #Temporary

	#Step 5:(ABC) Generate XML file for beast using FASTA/FASTQ files
	python $scripts/fastxToBeauti.py $data/$ID\_inseq\_RAW.fasta   #RAW FASTA
	python $scripts/fastxToBeauti.py $data/$ID\_inseq\_FILTERED.fasta  #FASTA FROM FILTERED FASTQ
	python $scripts/fastxToBeauti.py $data/$ID\_inseq\_FASTQ\_FILTERED.fastq #SIMULATED FASTQ


	#Step 6:(ABC) Run beast
	echo beast_submit beast $data/$ID\_inseq\_RAW\_beauti.xml 1 04:00:00 >> launchfile_temp
	echo beast_submit beast $data/$ID\_inseq\_FILTERED\_beauti.xml 1 04:00:00 >> launchfile_temp
	echo beast_submit beast $data/$ID\_inseq\_FASTQ\_FILTERED\_beauti.xml 1 04:00:00 >> launchfile_temp

	#cp launchfile_temp ~/launchfile
	#################################################################
	#####  BREAK!!!! Need to RUN jobs before rest of pipeline  ######
	#################################################################

	# # #Step 7:(ABC) Annotate trees
	# treeannotator $data/$ID_inseq_RAW.trees $data/$ID_RAW_tree.nex
	# treeannotator $data/$ID_inseq_FILTERED.trees $data/$ID_FILTERED_tree.nex
	# treeannotator $data/$ID_inseq_FASTQ_FILTERED.trees $data/$ID_FASTQ_tree.nex

	# # #Step 8:(ABC) Convert trees into newick format
	# cat $data/example.tree | sed 's/Taxon//g' > $data/example.tre
	# cat $data/$ID_RAW_tree.nex | grep ^tree | tr '[]' '\n' | grep -v ^\& | tr -d ' \n' | sed 's/^tree.*=//' > $data/$ID_RAW_tree.tre
	# cat $data/$ID_FILTERED_tree.nex | grep ^tree | tr '[]' '\n' | grep -v ^\& | tr -d ' \n' | sed 's/^tree.*=//' > $data/$ID_FILTERED_tree.tre
	# cat $data/$ID_FASTQ_tree.nex | grep ^tree | tr '[]' '\n' | grep -v ^\& | tr -d ' \n' | sed 's/^tree.*=//' > $data/$ID_FASTQ_tree.tre

	# # #Step 8.5: Concat trees together
	# rm $data/$ID_intree
	# cat $data/example.tre >> $data/$ID_intree
	# cat $data/$ID_RAW_tree.tre >> $data/$ID_intree
	# cat $data/$ID_FILTERED_tree.tre >> $data/$ID_intree
	# cat $data/$ID_FASTQ_tree.tre >> $data/$ID_intree


	# #Step 9:(ABC) Measure tree distance
	# cd data; printf $data/$ID'_intree\nR\n2\nP\nF\nY\n' | treedist
	done
done	