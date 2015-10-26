#!/usr/bin/python

import sys
import journal
import time
import datetime
import textwrap

import argparse

jrnl = journal.Journal()


def getTerminalSize():
    import os
    env = os.environ 
    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios, struct, os
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,
            '1234'))
        except:
            return
        return cr
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        cr = (env.get('LINES', 25), env.get('COLUMNS', 80))

        ### Use get(key[, default]) instead of a try/catch
        #try:
        #    cr = (env['LINES'], env['COLUMNS'])
        #except:
        #    cr = (25, 80)
    return int(cr[1]), int(cr[0])


def main(argv):
    argparser=argparse.ArgumentParser(description='View, edit and add to Clarity journals')
    argparser.add_argument("journalfilename", dest="journalfilename",
            help="Journal file to parse")
    argparser.add_argument("-a", "--addentry", dest="addentry", default="",
            help="Add an entry and save it back to the journal file. Automatically adds <Entry> tag.")
    argparser.add_argument("-t", "--tagtables", help="Show the parsed tagtables", action="store_true", dest="tagtables", default=False)
    argparser.add_argument("-e", "--entries", help="Show entries", action="store_true", dest="showentries", default=True)

    args = argparser.parse_args()




    if args.addentry:
        entrytime=int(time.time())*1000
        timemod=0
        while(jrnl.isentrytimeunique(entrytime+timemod)==False) and (timemod<1000):
            timemod=timemod+1

        if (timemod>=1000) :
            print ("Could not find valid timestamp")
        else:
            entrytime=entrytime+timemod
            newentry=jrnl.Entry("\n<Entry:"+str(entrytime)+">"+args.addentry+"\n")
            jrnl.addentry(newentry)
            if newentry.validentry:
                print ("\nAdded:",newentry.text)
            jrnl.savetofile(args.journalfilename)
            print ("Updated journal")

    if args.tagtables:
        print ("\n".join(str(tag.name for tag in entry.tags) for entry in jrnl.entries))
        #print ("\n".join(map(lambda e: str(map(lambda t: t.name, e.tags)),jrnl.entries)))
        print ("\n")
        print ("\n".join(key+":"+ str(tag.field for tag in taglist) for key,taglist in jrnl.tagdict.items()))
        #print ("\n".join(map(lambda k,tl: k+":"+str(map(lambda tag:tag.field,tl)),jrnl.tagdict.items())))

    if args.showentries:
        currentdate=0
        wrapper=textwrap.TextWrapper(initial_indent="",subsequent_indent="                ",width=getTerminalSize()[0])
        for entry in jrnl.entries:
            entrytime=datetime.datetime.fromtimestamp(int(entry.time)/1000)
            entrydate=entrytime.date()
            if (currentdate!=entrydate):
                print ("----------"+entrydate.strftime("%A %d %b %Y")+"----------")
                currentdate=entrydate
            print (wrapper.fill(entrytime.strftime("%d/%m/%y %H:%M")+": "+entry.text))



if __name__ == "__main__":
    main(sys.argv[1:])
