#!/usr/bin/python

import sys,jdata,time
from optparse import OptionParser

        
journal=jdata.Journal()


        
def process_new_entry(newentry):
    if newentry.validentry:
        journal.entries.append(newentry)
    
        for newtag in newentry.tags:
            if journal.tagdict.has_key(newtag.name):
                journal.tagdict[newtag.name].append(newtag)
            else:
                journal.tagdict[newtag.name]=[newtag]
                

def write_journal(filename):
    with open(filename, "w+") as jfile:
        for entry in journal.entries:
            jfile.write(entry.text)
                
            
def main(argv):
    
    optparser = OptionParser()
    optparser.add_option("-j", "--journalfile", dest="journalfilename",
            help="Journal file to parse")
    optparser.add_option("-a", "--addentry", dest="addentry", default="",
            help="Add an entry and save it back to the journal file. Automatically adds <Entry> tag.")
    optparser.add_option("-t", "--tagtables", help="Show the parsed tagtables", action="store_true", dest="tagtables", default=False)
            
    (options, args) = optparser.parse_args();
    

    
    try:
        with open(options.journalfilename) as jfile:
            entryindex=-1
            tempstring=" "
            for jline in jfile:
                tempstring+=jline
                entryindex=tempstring.find("<Entry:",1)
                while (entryindex>-1):
                    newentry=jdata.Entry(tempstring[:entryindex])
                    process_new_entry(newentry)
                    
                                
                    tempstring=tempstring[entryindex:]
                    entryindex=tempstring.find("<Entry:",1)
    
            newentry=jdata.Entry(tempstring)
            process_new_entry(newentry)
    except IOError:
         print "Could not open journal file"
     
    if options.addentry:
        entrytime=int(time.time())*1000
        timemod=0
        while(journal.isentrytimeunique(entrytime+timemod)==False) and (timemod<1000):
            timemod=timemod+1
            
        if (timemod>=1000) :
            print "Could not find valid timestamp"
        else:
            entrytime=entrytime+timemod
            newentry=jdata.Entry("\n<Entry:"+str(entrytime)+">"+options.addentry+"\n")
            process_new_entry(newentry)
            if newentry.validentry:
                print "\nAdded:",newentry.text
            write_journal(options.journalfilename)
            print "Updated journal"
            
    if options.tagtables:
        print "\n".join(map(lambda e: str(map(lambda t: t.name, e.tags)),journal.entries))
        print "\n"
        print "\n".join(map(lambda (k,tl): k+":"+str(map(lambda tag:tag.field,tl)),journal.tagdict.items()))

    
    
if __name__ == "__main__":
    main(sys.argv[1:])