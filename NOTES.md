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




Parse journal textfile and populate local datastructure in memory.
Journal - a dict or hashmap of entries, and a dict of tag instance lists
||
|+Entries - a time ordered list of entries.
|  |
|  +Entry - class instance containing the entry time/id and the contained text. Contains a character index ordered list of tag instances
|  |
|  +Tag - class instance describing a tag and field within and entry
+TagLists - a dict containg all tag names in the journal. Each name has an assosiated list of instances
 |
 +TagList - a time ordered list of tag instaces. Refers directly to tag instances in the Entry class instances

Need to determine the structure of this data. Potential lookup operations:
Priority module:
Build a list of tasks with associated dependancy rules (required to generate the priority field over time). Start with list of task tags. Each task tag needs a list of entries it appears in. Need to build a local list for each task containing the constraints and modifiers that apply to it (and their time). In each associated entry, only start looking at tags after the given task tag instance, and stop when another task tag is reached or the entry ends.
Trying to make the data structure plugin agnostic, so do not want to have to store the relevant task tag in the record for each modifier tag, as this would require definitions from the priority plugin.
Could store list of tags in the entry, in character order, or just scan through the entry text. Tags in their instance list could then refer either to an entry and the character index, or directly to the tag instance in the entry.




