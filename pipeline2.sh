#!/bin/bash
data="data"
scripts="scripts"

rm -f launchfile_temp

filter_threshold=15

INDEX=0
TOTAL=18

for L in 100 500 1000 #SEQUENCE LENGTH
do
	#for F in 10 15 20  #FILTER THRESHOLDS (CHANGE FOR FASTQ MUTATION RATE)
	F=15
	for E in 0.01 0.05 0.10
	do		
		for REP in {1..1}  #REPLICATES
		do
		ID=$REP\_E$E\_L$L
		#3 Variants: Standard FASTA (A), Preprocessed FASTQ as FASTA (B), FASTQ with likelihood modification (C)

		#Step 1:(ABC)  Generate the sequence files using a tree as input
		#	-m (model)  HKY
		#	-o (output type) Phylip
		# #	-q (quiet)
		# #	-l (length) 1000
		# seq-gen -mHKY $data/example.tree -op -q -l$L >> $data/$ID\_inseq.phy

		# #Step 2:(ABC) Convert seqeunces from phylip to FASTA format, remove unneeded phy file
		# #	Input: $data/sequences.phy
		# #	Output: $data/sequences.fasta
		# python $scripts/phylipToFASTA.py $data/$ID\_inseq.phy $data/$ID\_inseq.fasta

		# cp $data/$ID\_inseq.fasta $data/$ID\_inseq\_RAW.fasta   #USE THIS #1
	
		# rm $data/$ID\_inseq.phy

		# #Step 3:(BC) Generate simulated FASTQ file from the FASTA file.
		# python $scripts/fastq_sim.py $data/$ID\_inseq.fasta $E
		# # cp $data/$ID\_inseq.fastq  $data/$ID\_inseq\_RAW.fastq  
		# cp $data/$ID\_inseq.fastq  $data/$ID\_inseq\_FASTQ.fastq  #USE THIS #2

		# #Step 4:(B) Run FASTQ file through some preprocessor
		# # python $scripts/fastq_filter.py $data/$ID\_inseq\_RAW.fastq 0
		# # cp $data/$ID\_inseq\_RAW_FILTERED.fasta $data/$ID\_inseq\_RAW.fasta
		# # python $scripts/fastq_filter.py $data/$ID\_inseq.fastq $F
		# python $scripts/fastq_filter.py $data/$ID\_inseq\_FASTQ.fastq $F  #Temporary

		# #Step 5:(ABC) Generate XML file for beast using FASTA/FASTQ files
		# python $scripts/fastxToBeauti.py $data/$ID\_inseq\_RAW.fasta   #RAW FASTA
		# python $scripts/fastxToBeauti.py $data/$ID\_inseq\_FASTQ.fastq  #SIMULATED FASTQ
		# python $scripts/fastxToBeauti.py $data/$ID\_inseq\_FASTQ\_FILTERED.fastq #FILTERED SIMULATED FASTQ


		# #Step 6:(ABC) Run beast
		# # echo cd 'ErrorInclusion; beast_submit beast '$data'/'$ID'_inseq_RAW_beauti.xml '$ID'_RAW 1 4:00:00' >> launchfile_temp
		# # echo cd 'ErrorInclusion; beast_submit beast '$data'/'$ID'_inseq_FILTERED_beauti.xml '$ID'_FILTERED 1 4:00:00' >> launchfile_temp
		# # echo cd 'ErrorInclusion; beast_submit beast '$data'/'$ID'_inseq_FASTQ_FILTERED_beauti.xml '$ID'_FASTQ_FILTERED 1 4:00:00' >> launchfile_temp

		# beast -overwrite -working $data/$ID\_inseq_RAW_beauti.xml
		# beast -overwrite -working $data/$ID\_inseq_FASTQ_beauti.xml 
		# beast -overwrite -working $data/$ID\_inseq_FASTQ_FILTERED_beauti.xml


		
		#cp launchfile_temp ~/launchfile
		#################################################################
		#####  BREAK!!!! Need to RUN jobs before rest of pipeline  ######
		#################################################################

		# # #Step 7:(ABC) Annotate trees
		treeannotator $data/$ID\_inseq\_RAW.trees $data/$ID\_RAW\_tree.nex
		treeannotator $data/$ID\_inseq\_FASTQ.trees $data/$ID\_FASTQ\_tree.nex
		treeannotator $data/$ID\_inseq\_FASTQ\_FILTERED.trees $data/$ID\_FASTQ\_FILTERED\_tree.nex

		# # #Step 8:(ABC) Convert trees into newick format
		cat $data/example.tree | sed 's/Taxon//g' > $data/example.tre
		cat $data/$ID\_RAW\_tree.nex | grep ^tree | tr '[]' '\n' | grep -v ^\& | tr -d ' \n' | sed 's/^tree.*=//' > $data/$ID\_RAW\_tree.tre
		cat $data/$ID\_FASTQ\_tree.nex | grep ^tree | tr '[]' '\n' | grep -v ^\& | tr -d ' \n' | sed 's/^tree.*=//' > $data/$ID\_FASTQ\_tree.tre
		cat $data/$ID\_FASTQ\_FILTERED\_tree.nex | grep ^tree | tr '[]' '\n' | grep -v ^\& | tr -d ' \n' | sed 's/^tree.*=//' > $data/$ID\_FASTQ\_FILTERED_tree.tre

		# # #Step 8.5: Concat trees together
		# rm $data/$ID_intree
		cat $data/example.tre >> $data/$ID\_intree
		cat $data/$ID\_RAW\_tree.tre >> $data/$ID\_intree
		cat $data/$ID\_FASTQ\_tree.tre >> $data/$ID\_intree
		cat $data/$ID\_FASTQ\_FILTERED_tree.tre >> $data/$ID\_intree


		# #Step 9:(ABC) Measure tree distance
		printf $data/$ID'_intree\nR\n2\nP\nF\nY\n' | treedist
		mv outfile $data/$ID'.outfile'

		INDEX=$(($INDEX+1))
		PERC=$(($INDEX*100/$TOTAL))
		LOAD=''
		for num in $(seq 1 $PERC); do
		    LOAD=$LOAD#;
		done
		printf "\r[$PERC%%][%-100s]" $LOAD
		done
	done
done	
echo 
