#!/usr/bin/python

import sys,jdata
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
                
            
def main(argv):
    
    optparser = OptionParser()
    optparser.add_option("-j", "--journalfile", dest="journalfilename",
            help="Journal file to parse")
    optparser.add_option("-o", "--outputfile", dest="outputfilename",
            help="Output file to write tag dictionary into")
            
    (options, args) = optparser.parse_args();
    

    
    
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
                
    print "\n".join(map(lambda e: str(map(lambda t: t.name, e.tags)),journal.entries))
    print "\n"
    print "\n".join(map(lambda (k,tl): k+":"+str(map(lambda tag:tag.field,tl)),journal.tagdict.items()))

    
    
if __name__ == "__main__":
    main(sys.argv[1:])