Need to define file format, and if this will exist as a plain text file or in a database.

Probably start as a python server, processing journal files

Initial requirements:

- Parse journal files
- Journal entries need to be able to contain dynamic tags and attached metadata
 - Journal files contain separate Entries. Entries need to be individually distinguishable - use unix time? Rely on collision detection when adding a new entry - add a millisecond to separate (not as extensible as a hash, but a bit more elegant. May have problems when syncing changes if two independant devices try to create an entry at the same point. That said, existing systems somehow get around this with name collisions)
- Tags have a name and a field.
- Fields are just text, validation of field data type for a particular tag is up to the entry client.


Test case:

Several entries in a single journal file defining tasks. Each task has a set priority and dependency on other tasks.

? Can multiple tasks be defined in a single entry?


    <Entry:999999999> Blah blah stuff. Need to <Task:Do something> <Complete by:12/03/2015>. Should take <Duration: 4 hours>
    
    <Entry:33737373737> More stuff. Oh, and <Task:Something else> <Complete before:Do something>. <Task:Another thing> also needs doing for <Person>
    
    <Entry:2348972349> Words. More words. <Task:Boring thing> 
    
    <Entry:12312312313> Maybe a sentence? <Task:Less boring thing> <Complete after:Something else>
    
    
Journal parser needs to create lists for each tag, listing occurences and which entry they were in (also the character location). Specific tags (and identical field) may be present in multiple entries.

Priority module/plugin then uses this dataset. List of tasks is filled out, for each task occurence in an entry look for modifier tags (Complete by, Complete before, etc.) until another task or the entry finishes. Can build dependency links as this is happening, as a list of tasks already exists.




