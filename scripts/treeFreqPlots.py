#!/usr/bin/python
import re, os, numpy, math
from matplotlib import pyplot
import combine_plots as cp

doms = "324"

def getDistances(filename):
	file = open(filename)
	tree_dist_str = file.readlines()[9].split('|')[1].strip()
	file.close()
	tree_dists = re.split('\s+', tree_dist_str)
	# if(len(tree_dists[1:]) != 3):
		# print filename
	return tree_dists[1:4]


def updateArray(oldArray, newData):
	if(len(oldArray) != len(newData)):
		print "ERROR!"
		exit(0);

	for i in range(len(newData)):
		oldArray[i].append(float(newData[i]))

	return oldArray

def makeHistogram(arr, means=[], title="Plot Title"):
	lb = min(min(arr))
	ub = max(max(arr))
	n_values = len(arr[0])
	bins = numpy.linspace(lb, 1.6, 30)
	# pyplot.hist(arr[0], histtype='stepfilled', bins=bins, color='black', alpha=1, label='RAW')
	# pyplot.hist(arr[1], histtype='stepfilled', bins=bins, color='white', alpha=0.25, label='FASTQ')
	# pyplot.hist(arr[2], histtype='stepfilled', bins=bins, color='orange', alpha=0.25, label='FILTERED')
	pyplot.hist(arr, bins=bins, normed=1,color=['red','green','blue'], label=['RAW ( ' + means[0] + ' )','FASTQ ( ' + means[1] + ' )','FILTERED ( ' + means[2] + ' )'])
	pyplot.legend(loc='upper right')
	save_tit = title.replace(' ','').replace('=','').replace('.','_')
	pyplot.title(title)
	pyplot.xlabel('Geodesic Distance to Origin Tree')
	pyplot.ylabel('Frequency')
	pyplot.savefig(save_tit)
	# pyplot.show()
	pyplot.close()


def run(typ='ALL DATA', quant='', num_reps=100):
	reps = range(1,num_reps+1)
	if(typ=='E'):
		lengths = ['100']
		errors = [quant]
	elif(typ=='L'):
		errors = ['0.01','0.05','0.10']
		lengths = [quant];
	else:
		lengths = ['100','500', '1000']
		errors = ['0.01','0.05','0.10']
	distances = [[],[],[]]
	for e in errors:
		for l in lengths:
			for r in reps:
				newData = getDistances(str(r)+"_E"+e+'_L'+l+'.outfile')
				distances = updateArray(distances, newData)
	means = [str(numpy.mean(distances[0])),str(numpy.mean(distances[1])),str(numpy.mean(distances[2]))]  #Using means
	# means = [str(numpy.median(distances[0])),str(numpy.median(distances[1])),str(numpy.median(distances[2]))]  #Using medians
	# print "RAW mean: " + means[0]
	# print "FASTQ mean: " + means[1]
	# print "FILTERED mean: " + means[2]
	title = typ + ' = ' + quant if typ != 'All DATA' else typ
	makeHistogram(distances, means, title)

def main():
	errors = ['0.01','0.05','0.10']
	lengths = ['100','500', '1000']
	num_reps = 100
	for e in errors:
		run('E',e,num_reps)
	for l in lengths:
		run('L',l, num_reps)
	run()
	cp.main()

if __name__=='__main__':
	main()