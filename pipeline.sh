#!/bin/sh
DATA_DIR=data
TREE_NAME=example.tree
SEQ_NAME=sequences 

SRC_DIR=src

#Generate Sequences from tree: seq-gen
seq-gen -mHKY $DATA_DIR/$TREE_NAME -op -q >> $DATA_DIR/$SEQ_NAME.phylip

#Convert generated sequences into FASTA format: phylipToFASTA.py
python $SRC_DIR/phylipToFASTA.py $DATA_DIR/$SEQ_NAME.phylip

#Simulate FASTQ data using generated FASTA file: fastq_sim.py
python $SRC_DIR/fastq_sim.py $DATA_DIR/$SEQ_NAME.FASTA

mv $DATA_DIR/$SEQ_NAME.FASTA.FASTQ $DATA_DIR/$SEQ_NAME.FASTQ 

