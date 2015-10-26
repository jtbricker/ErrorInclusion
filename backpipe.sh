#!/bin/bash
data="data"
scripts="scripts"

rm -f launchfile_temp

INDEX=0
TOTAL=900

for L in 50 100 500 #SEQUENCE LENGTH
do
	#for F in 10 15 20  #FILTER THRESHOLDS (CHANGE FOR FASTQ MUTATION RATE)
	F=28
	for E in 0.01 0.05 0.10
	do		
		for REP in {1..100}  #REPLICATES
		do
		ID=$REP\_E$E\_L$L
		
		#################################################################
		#####  BREAK!!!! Need to RUN jobs before this step         ######
		#################################################################

		# 4 TYPES OF RUNS
		# 1)  RAW
		# 2)  FASTA_ERROR
		# 3)  FILTERED
		# 4)  FASTQ_CALCULATED


		# # #Step 7:(ABC) Annotate trees
		# treeannotator $data/$ID\_inseq\_RAW.trees $data/$ID\_RAW\_tree.nex
		# treeannotator $data/$ID\_inseq\_FASTA\_ERROR.trees $data/$ID\_FASTA\_ERROR\_tree.nex
		# treeannotator $data/$ID\_inseq\_FILTERED.trees $data/$ID\_FILTERED\_tree.nex
		# treeannotator $data/$ID\_inseq\_FASTQ\_CALCULATED.trees $data/$ID\_FASTQ\_CALCULATED\_tree.nex

		# # #Step 8:(ABC) Convert trees into newick format
		cat $data/example.tree | sed 's/Taxon//g' > $data/example.tre
		cat $data/$ID\_inseq\_RAW.tree | grep ^tree | tr '[]' '\n' | grep -v ^\& | tr -d ' \n' | sed 's/^tree.*=//' > $data/$ID\_RAW\_tree.tre
		cat $data/$ID\_inseq\_FASTA\_ERROR.tree | grep ^tree | tr '[]' '\n' | grep -v ^\& | tr -d ' \n' | sed 's/^tree.*=//' > $data/$ID\_FASTA\_ERROR\_tree.tre
		cat $data/$ID\_inseq\_FILTERED.tree | grep ^tree | tr '[]' '\n' | grep -v ^\& | tr -d ' \n' | sed 's/^tree.*=//' > $data/$ID\_FILTERED\_tree.tre
		cat $data/$ID\_inseq\_FASTQ\_CALCULATED.tree | grep ^tree | tr '[]' '\n' | grep -v ^\& | tr -d ' \n' | sed 's/^tree.*=//' > $data/$ID\_FASTQ\_CALCULATED\_tree.tre

		# # #Step 8.5: Concat trees together
		# rm $data/$ID_intree
		cat $data/example.tre >> $data/$ID\_intree
		cat $data/$ID\_RAW\_tree.tre >> $data/$ID\_intree
		cat $data/$ID\_FASTA\_ERROR\_tree.tre >> $data/$ID\_intree
		cat $data/$ID\_FILTERED\_tree.tre >> $data/$ID\_intree
		cat $data/$ID\_FASTQ\_CALCULATED\_tree.tre >> $data/$ID\_intree


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
