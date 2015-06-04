#!/usr/bin/python

import sys
from optparse import OptionParser

class Journal:
    def __init__(self):
        self.entries = []#time ordered list of entries
        self.tagdict = {}#dict of tag instance lists, using tag name as keyword

class Entry:
    def parse(self):
        tagindex=self.text.find('<')
        while (tagindex>-1):
            tagend=self.text.find('>',tagindex+1)
            tempname,_,tempfield=self.text[tagindex+1:tagend].partition(':')
            #print "Name:",tempname,"Field:",tempfield
            self.tags.append(Tag(tempname,tempfield))
            tagindex=self.text.find('<',tagindex+1)
            
    def __init__(self,text):
        self.time=0 # Unix time identifier
        self.text=text # text of entry
        self.tags=[] # character index order list of tags in entry
        self.parse()
        self.validentry=False
        
        if len(self.tags)>0:
            if (self.tags[0].name=="Entry"):
                if len(self.tags[0].field)>1:
                    self.validentry=True
        
class Tag:
    def __init__(self,name,field):
        self.name=name # name of tag
        self.field=field # field text
        
        
        
        
journal=Journal()


        
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
                newentry=Entry(tempstring[:entryindex])
                process_new_entry(newentry)
                
                            
                tempstring=tempstring[entryindex:]
                entryindex=tempstring.find("<Entry:",1)

        newentry=Entry(tempstring)
        process_new_entry(newentry)
                
    print "\n".join(map(lambda e: str(map(lambda t: t.name, e.tags)),journal.entries))
    print "\n"
    print "\n".join(map(lambda (k,tl): k+":"+str(map(lambda tag:tag.field,tl)),journal.tagdict.items()))

    
    
if __name__ == "__main__":
    main(sys.argv[1:])