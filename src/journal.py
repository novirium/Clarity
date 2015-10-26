#!/usr/bin/python

# Defines the data structure used to hold journal tag data

import time

class Journal:
    def __init__(self):
        self.entries = []#time ordered list of entries
        self.tagdict = {}#dict of tag instance lists, using tag name as keyword

    def addnewentry(self,entrytext):
        entrytime=int(time.time())*1000
        timemod=0
        while(self.isentrytimeunique(entrytime+timemod)==False) and (timemod<1000):
            timemod=timemod+1

        if (timemod>=1000) :
            print ("Could not find valid timestamp")
        else:
            entrytime=entrytime+timemod
            newentry=Entry("\n<Entry:"+str(entrytime)+">"+entrytext+"\n")
            self.addentry(newentry)

    def addentry(self,newentry):
        if newentry.validentry:
            self.entries.append(newentry)

            for newtag in newentry.tags:
                if newtag.name in self.tagdict:
                    self.tagdict[newtag.name].append(newtag)
                else:
                    self.tagdict[newtag.name]=[newtag]


    def loadfromfile(self,filename):
        try:
            with open(filename) as jfile:
                entryindex=-1
                tempstring=" "
                for jline in jfile:
                    tempstring+=jline
                    entryindex=tempstring.find("<Entry:",1)
                    while (entryindex>-1):
                        self.addentry(Entry(tempstring[:entryindex]))


                        tempstring=tempstring[entryindex:]
                        entryindex=tempstring.find("<Entry:",1)

                self.addentry(Entry(tempstring))
        except IOError:
            print ("Could not open journal file")

    def savetofile(self,filename):
        with open(filename, "w+") as jfile:
            for entry in self.entries:
                jfile.write(entry.text)


    def isentrytimeunique(self,entrytime):
        for entry in self.entries:
            if entry.time==entrytime:
                return False
        return True

class Entry:
    def parse(self):
        tagindex=self.text.find('<')
        while (tagindex>-1):
            tagend=self.text.find('>',tagindex+1)
            tempname,_,tempfield=self.text[tagindex+1:tagend].partition(':')
            #print "Name:",tempname,"Field:",tempfield
            self.tags.append(Tag(tempname,tempfield,self,tagend))
            tagindex=self.text.find('<',tagindex+1)

    def __init__(self,text):
        self.time=0 # Unix time identifier
        self.text=text # text of entry
        self.tags=[] # character index order list of tags in entry
        self.parse()
        self.validentry=False

        if len(self.tags)>0:
            if (self.tags[0].name=="Entry"):
                if self.tags[0].field.isdigit():
                    self.validentry=True
                    self.time=int(self.tags[0].field)


class Tag:
    def __init__(self,name,field,parententry,endcharindex):
        self.name=name # name of tagsentenceaftertag
        self.field=field # field text
        self.parententry=parententry # entry that this tag instance is contained in
        self.endcharindex=endcharindex # character index of the end of the tag in the parsed entry text

    def getnextsentence(self):
        sentenceend=len(self.parententry.text)-1
        tempindex=self.parententry.text.find('<',self.endcharindex+1)
        if (tempindex<sentenceend) and (tempindex>self.endcharindex):
            sentenceend=tempindex
        tempindex=self.parententry.text.find('.',self.endcharindex+1)
        if (tempindex<sentenceend) and (tempindex>self.endcharindex):
            sentenceend=tempindex

        return (self.parententry.text[self.endcharindex+1:sentenceend]).rstrip()
