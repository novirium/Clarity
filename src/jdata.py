#!/usr/bin/python

# Defines the data structure used to hold journal tag data

class Journal:
    def __init__(self):
        self.entries = []#time ordered list of entries
        self.tagdict = {}#dict of tag instance lists, using tag name as keyword
        
    def isentrytimeunique(self,time):
        for entry in self.entries:
            if entry.time==time:
                return False
        return True

class Entry:
    def parse(self):
        tagindex=self.text.find('<')
        while (tagindex>-1):
            tagend=self.text.find('>',tagindex+1)
            tempname,_,tempfield=self.text[tagindex+1:tagend].partition(':')
            #print "Name:",tempname,"Field:",tempfield
            self.tags.append(Tag(tempname,tempfield,self))
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
    def __init__(self,name,field,parententry):
        self.name=name # name of tag
        self.field=field # field text
        self.parententry=parententry # entry that this tag instance is contained in