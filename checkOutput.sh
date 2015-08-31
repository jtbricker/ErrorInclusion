for E in 0.01 0.05 0.10
do
	for L in 100 500 1000
	do
		for R in {1..100}
		do
			filename=$R\_E$E\_L$L
		
			for T in RAW FASTQ FASTQ\_FILTERED
			do
				[ ! -f $filename\_inseq\_$T.trees ] && echo $filename\_inseq\_$T.trees
			done
		done
	done
done
