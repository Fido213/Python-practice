import json
import uuid
from datetime import datetime
import inquirer

test_string_correct = "ac33cda7-e302-40ef-ba09-74363c1bd654 : random taskabcdferoinerhakfaslielddd ; date"
test_string_not_correct_order = "random task : uuid ; date"
test_string_not_correct_order_colonsincluded = "random task ; uuid : date"


def split_three(task):
    stripped_task = task.strip()
    indexsemi = stripped_task.find(";")
    indexcolon = stripped_task.find(":")
    if indexsemi > indexcolon:
        first_section = stripped_task[:indexcolon-1].strip()
        middle_section = stripped_task[indexcolon+1:indexsemi].strip()
        third_section = stripped_task[indexsemi+1:].strip()
        list_all_sections = [first_section, middle_section, third_section]
        print(list_all_sections)
        return list_all_sections
    elif indexcolon > indexsemi:
        first_section = stripped_task[:indexsemi-1].strip()
        middle_section = stripped_task[indexsemi+1:indexcolon].strip()
        third_section = stripped_task[indexcolon+1:].strip()
        list_all_sections = [first_section, middle_section, third_section]
        print(list_all_sections)
        return list_all_sections


split_three(test_string_correct)
split_three(test_string_not_correct_order)
split_three(test_string_not_correct_order_colonsincluded)
def uuid_check():
    list_all_sections = split_three(test_string_correct)
    for task in list_all_sections:
        print(task)
        if len(task) == 36:
            try:
                uuid.UUID(task)
                print("is uuid")
            except ValueError:
                print("its not uuid")
        else:
            print("not uuid")
uuid_check()
#print(len(test_string_correct))
#stripped_test_string_correct = test_string_correct.strip()
#print(stripped_test_string_correct)
#indexsemi = stripped_test_string_correct.find(";")
#indexcolon = stripped_test_string_correct.find(":")
#print(indexcolon, indexsemi)
#print(f"the length between the : and ; is equal to ({indexsemi} - ({indexcolon}) - 1")
#indexed_middle_test_string_correct = stripped_test_string_correct[indexcolon+1:indexsemi].strip()
#print(indexed_middle_test_string_correct)
#indexed_first_test_string_correct = stripped_test_string_correct[:indexcolon-1].strip()
#indexed_third_test_string_correct = stripped_test_string_correct[indexsemi+1:].strip()
#print(indexed_first_test_string_correct)
#print(indexed_third_test_string_correct)
#list_format_test_string_correct = [indexed_first_test_string_correct, indexed_middle_test_string_correct, indexed_third_test_string_correct]
#print(list_format_test_string_correct)





#length_uuid = len(str("ac33cda7-e302-40ef-ba09-74363c1bd654"))
#print(len(indexed_middle_test_string_correct))


#if len(indexed_middle_test_string_correct) == length_uuid:
#    try:
#        uuid.UUID(indexed_middle_test_string_correct)
#        print("is uuid")
#    except ValueError:
#        print("its not uuid")
#else:
#    print("not uuid")

# first index ":" is at 6, second is at 9
# full length is 30
# in index terms that 29 "cursor"
# u can calculate the first string before the ":" is 5+1 in length
# and in between the length is 2+1 in length
# and after is the rest so 6 (first length) + 3 (second length) = 9, so the 
# rest is 30-9 = 21,
# so first we calculate all the lengths and save them
# ie first part, second, third,  this means that A:
# i can split them via first_part[index, index] and etc
# then i can save them in a list
# after saving them in a list im able to use the actual index for lists
# (way easier) to pick and choose which one i want to check
# now after making them into a list, ill run a for loop to check all 3 for:
# if they match a uuid length, if they do then we check via uuid.UUID(string)
# else we continue and skip this iteration (first loop), if they dont pass the uuid.UUID
# then we also skip them, in both cases if they fail, they get into another function (made already)
# to check if they are date formatted, if they arent then they are foricbiiy a task
# then in each check, if a part is found true, then we take it from the list
# via pop and insert to resort them (0 for date, 1 for uuid and 2 for task)
# finally after sorting them we rejoin them in a .join function and stringify them
# now if they happen to not have either a : or ;, then in the earlier calculations if it
# returns -1, they stop that calculation and instead calculate half, so like it will continue
# to the exisitng delimetter (5 10 and 15, if 10 doesnt exist it gon count from 5 to 15)
# and if both dont exist, we go to checking
# it will then verify as usual the uuid and date (both or singular)
# if its singular and it happens to be a uuid or datetime then we delete it since no task in memory
# if its singular and a task, then we add a uuid and datetime in the correct spot
# else if its 2 parts it will check as said before if its which is uuid and which is date
# we can run an if statement:
# if both are true, we delete
# if date is true and uuid isnt, we sort, create uuid in correct spot, and then join and continue with normal flow
# same thing if the other way around
# every check is its seperate function and will all be used via return functions to ease flow
# this function will run everytime we start up the program, it will use the read memory function
# and each time it updates or corrects something it will use the update memory function
# also the data its gonna sanitise will be the status dictionary
# my idea was instead of going over list by list i could just do 2 seperate function, one containing the actual sanitsation code, the other activiting it for each list:
#for i in status[done]
#    sanitsation_function(i)
# and repeat for pending and unfinished
# ill aim to split first by ; and then :


