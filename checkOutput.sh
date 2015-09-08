#RUN THIS IS THE Error_Inclusion/data directory

for E in 0.01 0.05 0.10
do
	for L in 100 500 1000
	do
		for R in {1..100}
		do
			filename=$R\_E$E\_L$L

			for T in RAW FASTQ FASTQ\_FILTERED
			do
			[ ! -f $filename\_inseq\_$T.trees ] && echo "cd ErrorInclusion; beast_submit beast data/$R""_E$E""_L$L""_inseq_""$T""_beauti.xml $R""_E$E""_L$L""_$T 1 4:00:00" >> ../launchfile_redo
			done
		done
	done
done
