d="data"

rm -f launchfile_temp
rm -f $d/*.names
rm -f $d/example.tree
for i in {1..100}; do rm -f $d/$i*; done;
rm -f $d/*.FASTA
rm -f $d/*.fasta
rm -f $d/*.phy
rm -f $d/*.FASTQ
rm -f $d/*.fastq
rm -f $d/*fastqc*
rm -f $d/*.trees
rm -f $d/*.tre
rm -f $d/*.nex
rm -f $d/*.log
rm -f $d/beauti_template.xml.state
rm -f $d/*sequences*
rm -f $d/*.log
find $d/*xml ! -name "beauti_template.xml" -exec rm {} \;
rm -f $d/*state*
rm -f $d/intree
rm -f $d/outfile
rm -f $d/*sub
rm -f *.sub
rm -f *_E*_L*
