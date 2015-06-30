d="data"
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
find ./*xml ! -name "beauti_template.xml" -exec rm {} \;