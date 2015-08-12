rm inseq.*

seq-gen -mHKY ../data/example.tree -op -q -l$1 >> inseq.phy

python ../scripts/phylipToFASTA.py inseq.phy inseq.fasta

python ../scripts/fastq_sim.py inseq.fasta 0.02

# runipy QualityPlots.ipynb