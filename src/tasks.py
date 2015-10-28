#!/usr/bin/python

import journal
import argparse
import datetime
import string


#Want to be able to refer to tasks by a short reference. Reference is based on week and defined order during that week.
#entry format:
#<entry:123123> <task:1A>Finish x for Y.
#<entry:123124> <todonext:1A>Make file for Z.
#
#ctask
#39E: Task to do something
#     --Make file fo Z
#39G: Other task
#39H: Something else
#
#ctask -a "task description"
#Added 39N: task description
#
#ctask 39A -n "something that needs to be done next"
#
#
#

class Task:
    def __init__(self,name,todonext):
        self.name=name
        self.todonext=todonext

jrnl = journal.Journal()
tasklist= {}
completetasks=[]

def gentasklist():
    if 'task' in jrnl.tagdict:
        tasktags=jrnl.tagdict['task']
    else:
        tasktags=[]

    if 'completetask' in jrnl.tagdict:
        completetasktags=jrnl.tagdict['completetask']
    else:
        completetasktags=[]

    completetasks[:]=[]
    for completetasktag in completetasktags:
        completetasks.append(completetasktag.field)

    for tasktag in tasktags:
        if not (tasktag.field in completetasks):
            if tasktag.field in tasklist:
                tasklist[tasktag.field].name=tasktag.getnextsentence()
            else:
                tasklist[tasktag.field]=Task(tasktag.getnextsentence(),"")

    if 'todonext' in jrnl.tagdict:
        tdntags=jrnl.tagdict['todonext']
    else:
        tdntags=[]

    for tdntag in tdntags:
        if not (tdntag.field in completetasks):
            if tdntag.field in tasklist:
                tasklist[tdntag.field].todonext=tdntag.getnextsentence()
            else:
                print ("Couldn't find task "+tdntag.field)

def getfreetaskref(weeknumber):
    letterindex=0
    newtaskref=str(weeknumber)+"A"
    while ((newtaskref in tasklist) or (newtaskref in completetasks)) and (letterindex<701):
        letterindex+=1
        newtaskref=str(weeknumber)
        if (letterindex>=26):
            newtaskref=newtaskref+(string.ascii_uppercase)[(letterindex//26)-1]
        newtaskref=newtaskref+(string.ascii_uppercase)[letterindex%26]
    return newtaskref


def main():
    argparser=argparse.ArgumentParser(description='View, edit and add to Clarity tasks')
    argparser.add_argument("journalfilename",
            help="Journal file to use")
    argparser.add_argument("taskref", default="", nargs="?",
            help="Task for operation to be applied to. Example: 39C")
    argparser.add_argument("-a", "--addtask", help="Add a new task. Follow option with task description text.", dest="addtask", default="") #need to change to actual values rather than boolean
    argparser.add_argument("-n", "--todonext", help="Adds a new ToDoNext to the task referenced.", dest="todonext", default="")
    argparser.add_argument("-c", "--complete", help="Marks a task as complete", action="store_true", dest="markcomplete", default=False)

    args = argparser.parse_args()

    if not(args.journalfilename):
        print("Journal filename is required")
        return 0

    jrnl.loadfromfile(args.journalfilename)

    gentasklist()

    if args.addtask:
        nowweeknumber=datetime.datetime.today().isocalendar()[1]
        newtaskref=getfreetaskref(nowweeknumber)
        newentrytext="<task:"+newtaskref+">"+args.addtask
        jrnl.addnewentry(newentrytext)
        jrnl.savetofile(args.journalfilename)
        print ("Added task "+newtaskref+"\n")
        print (newentrytext)
        gentasklist()
        #add task

    if args.taskref:
        if args.taskref in tasklist:
            if args.todonext:
                newentrytext="<todonext:"+args.taskref+">"+args.todonext
                jrnl.addnewentry(newentrytext)
                jrnl.savetofile(args.journalfilename)
                print ("Updated ToDoNext\n")
                gentasklist()


            if args.markcomplete:
                newentrytext="<completetask:"+args.taskref+">"
                jrnl.addnewentry(newentrytext)
                jrnl.savetofile(args.journalfilename)
                print ("Completed "+args.taskref+"\n")
                gentasklist()

            print(args.taskref+": "+tasklist[args.taskref].name)
            if (tasklist[args.taskref].todonext):
                print("    -- "+tasklist[args.taskref].todonext)
        else:
            print ("Couldn't find task "+args.taskref)
    else:
        for taskname,task in sorted(tasklist.items()):
            print(taskname+": "+task.name)
            if (task.todonext):
                print("   -- "+task.todonext)

if __name__ == "__main__":
    #main(sys.argv[1:])
    main()
