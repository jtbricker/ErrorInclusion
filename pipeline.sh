#!/bin/bash
data="data"
scripts="scripts"

rm -f launchfile_temp

INDEX=0
TOTAL=900

for L in 50 # 100 500 #1000 #SEQUENCE LENGTH
do
	#for F in 10 15 20  #FILTER THRESHOLDS (CHANGE FOR FASTQ MUTATION RATE)
	F=1
	for E in 0.01 #0.05 0.10
	do		
		for REP in 1 # {1..100}  #REPLICATES
		do
		ID=$REP\_E$E\_L$L
		#  3 Variants: Standard FASTA (A), Preprocessed FASTQ as FASTA (B), FASTQ with likelihood modification (C)


		#Step 0:(ABC)  Replace species names in tree file with short replacement names (original names stored)
		#	Inputs
		#	original.tree -   The original tree that you are replacing names in
		#	example.tree -  New tree you are creating with replaced names
		#	plant.names - Name of file where short-to-long name list is/will be stored
		# 	1 for replace(2 for insert)- Operation you are performing
		python $scripts/replace_species_names.py $data/original.tree $data/example.tree $data/plant.names 1

		#Step 1:(ABC)  Generate the sequence files using a tree as input
		#	-m (model)  HKY
		#	-o (output type) Phylip
		#	-q (quiet)
		#	-l (length) 1000
		seq-gen -mHKY $data/example.tree -op -q -l$L >> $data/$ID\_inseq.phy

		#Step 2:(ABC) Convert seqeunces from phylip to FASTA format, remove unneeded phy file
		#	Input: $data/sequences.phy
		#	Output: $data/sequences.fasta
		python $scripts/phylipToFASTA.py $data/$ID\_inseq.phy $data/$ID\_inseq.fasta
		cp $data/$ID\_inseq.fasta $data/$ID\_inseq\_RAW.fasta   #USE THIS #1-RAW
	
		# rm $data/$ID\_inseq.phy

		#Step 3:(BC) Generate simulated FASTQ file from the FASTA file with given error.
		python $scripts/fastq_sim.py $data/$ID\_inseq.fasta $E    
		cp $data/$ID\_inseq.fasta  $data/$ID\_inseq\_FASTA_ERROR.fasta  #USE THIS #2-ErrorFASTA
		cp $data/$ID\_inseq.fastq  $data/$ID\_inseq\_FASTQ_CALCULATED.fastq  #USE THIS #4-FASTQ_CALCULATED

		#Step 4:(B) Run FASTQ file through some preprocessor
		python $scripts/fastq_filter.py $data/$ID\_inseq.fastq $F #-->  data/$ID_inseq_FASTQ_FILTERED.fasta  #USE THIS #3 FASTQ_FILTERED


		#Step 5:(ABC) Generate XML file for beast using FASTA/FASTQ files
		python $scripts/fastxToBeauti.py $data/$ID\_inseq\_RAW.fasta   #1 RAW FASTA
		python $scripts/fastxToBeauti.py $data/$ID\_inseq\_FASTA_ERROR.fasta  #2 SIMULATED ERROR FASTA
		python $scripts/fastxToBeauti.py $data/$ID\_inseq\_FILTERED.fasta #3 FILTERED SIMULATED FASTQ as FASTA
		python $scripts/fastxToBeauti.py $data/$ID\_inseq\_FASTQ_CALCULATED.fastq  #4 SIMULATED ERROR FASTQ!

		#Step 6:(ABC) Run beast
		echo cd 'ErrorInclusion; beast_submit beast '$data'/'$ID'_inseq_RAW_beauti.xml '$ID'_RAW 1 4:00:00' >> launchfile_temp
		echo cd 'ErrorInclusion; beast_submit beast '$data'/'$ID'_inseq_FASTA_ERROR_beauti.xml '$ID'_FASTA_ERROR 1 4:00:00' >> launchfile_temp
		echo cd 'ErrorInclusion; beast_submit beast '$data'/'$ID'_inseq_FILTERED_beauti.xml '$ID'_FILTERED 1 4:00:00' >> launchfile_temp
		echo cd 'ErrorInclusion; beast_submit beast '$data'/'$ID'_inseq_FASTQ_CALCULATED_beauti.xml '$ID'_FASTQ_CALCULATED 1 4:00:00' >> launchfile_temp

		#beast -overwrite -working $data/$ID\_inseq_RAW_beauti.xml
		#beast -overwrite -working $data/$ID\_inseq_FILTERED_beauti.xml 
		#beast -overwrite -working $data/$ID\_inseq_FASTQ_FILTERED_beauti.xml


		INDEX=$(($INDEX+1))
		PERC=$(($INDEX*100/$TOTAL))
		LOAD=''
		for num in $(seq 1 $PERC); do
		    LOAD=$LOAD#;
		done
		printf "\r[$PERC%%][%-100s]" $LOAD
		

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
done	
echo 
