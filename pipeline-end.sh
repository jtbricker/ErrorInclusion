#Step 6:(ABC) Run beast
beast -overwrite -working $data/inseq_RAW_beauti.xml
beast -overwrite -working $data/inseq_FILTERED_beauti.xml
beast -overwrite -working $data/inseq_FASTQ_FILTERED_beauti.xml

# #Step 7:(ABC) Annotate trees
treeannotator $data/inseq_RAW.trees $data/RAW_tree.nex
treeannotator $data/inseq_FILTERED.trees $data/FILTERED_tree.nex
treeannotator $data/inseq_FASTQ_FILTERED.trees $data/FASTQ_tree.nex

# #Step 8:(ABC) Convert trees into newick format
cat $data/example.tree | sed 's/Taxon//g' > $data/example.tre
cat $data/RAW_tree.nex | grep ^tree | tr '[]' '\n' | grep -v ^\& | tr -d ' \n' | sed 's/^tree.*=//' > $data/RAW_tree.tre
cat $data/FILTERED_tree.nex | grep ^tree | tr '[]' '\n' | grep -v ^\& | tr -d ' \n' | sed 's/^tree.*=//' > $data/FILTERED_tree.tre
cat $data/FASTQ_tree.nex | grep ^tree | tr '[]' '\n' | grep -v ^\& | tr -d ' \n' | sed 's/^tree.*=//' > $data/FASTQ_tree.tre

# #Step 8.5: Concat trees together
rm $data/intree
cat $data/example.tre >> $data/intree
cat $data/RAW_tree.tre >> $data/intree
cat $data/FILTERED_tree.tre >> $data/intree
cat $data/FASTQ_tree.tre >> $data/intree


#Step 9:(ABC) Measure tree distance
cd data; printf 'R\n2\nP\nF\nY\n' | treedist