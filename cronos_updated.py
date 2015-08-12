#!/usr/bin/env python
#
import pwd
import sys
import os
import time
import subprocess

def run_command(command):
    p = subprocess.Popen(command,shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    return iter(p.stdout.readline, b'')  # b'' is byte repr of empty string

def get_username():
    return pwd.getpwuid( os.getuid() )[ 0 ]


def my_idle_jobs(queue):
    me = get_username()
    command = "squeue -p "+queue+" -u "+me+' | grep "'+ me+'  PD" | wc'
    x = run_command(command)
    for xi in x:
    	xii = xi.split()
    	print xii[0]
	break
    return int(xii[0])

def replace_stack(launchfile, runs):
    shortruns = runs[0]
    longruns = runs[1]
    home = os.path.expanduser('~')+'/'
    f = open(home+launchfile,'w')
    for si in shortruns:
        f.write(si)
    for li in longruns:
        f.write(li)
    f.close()

def my_waiting_jobs(launchfile):
    home = os.path.expanduser('~')+'/'
    f = open(home+launchfile,'rU')
    stack = f.readlines()
    f.close()
    shortruns =[]
    longruns =[]
    for sti in stack:
        s = sti.split()
        if s == []:
            continue
        #print s[-1]
        limittime = time.strptime(s[-1].strip(),"%I:%M:%S")
        year, month, day, hour, minute, second, weekday, yearday, daylight = limittime
        runtime = hour*60*60 + minute*60 + second
        #print runtime,
        if runtime <= 240*60:
            shortruns.append(sti)
        else:
            longruns.append(sti)
    return shortruns,longruns

def launch(runs,waiting):
    longruns = runs[1]
    shortruns = runs[0]
    
    while waiting[1]<10:
        if len(longruns)>=1:
            runnow = longruns.pop(0)
            #print runnow
            #os.system(runnow)
            waiting[1] += 1
        else:
            break
        
    while waiting[0]<150:
        if len(shortruns)>=1:
            runnow = shortruns.pop(0)
            os.system(runnow.strip()+" backfill")
            waiting[0] += 1
        else:
            break
    return shortruns,longruns

#
if __name__ == '__main__':
    # check the number of jobs in the queues 
    #    backfill
    #    backfill2
    #    beerli_q
    backfill= my_idle_jobs('backfill')
    beerli_q =  my_idle_jobs('beerli_q')
    waiting = [backfill, beerli_q]
    print waiting
    launchfile = 'launchfile'
    runs = my_waiting_jobs(launchfile)
    runs = launch(runs,waiting)
    replace_stack(launchfile,runs)
    print waiting
