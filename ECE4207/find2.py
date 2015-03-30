#!/usr/bin/env python

# Author     : Myeong-Uk (mwsong@imtl.skku.ac.kr)
# Date       : 2015. 03. 30
# Desc       : Python program to dictionary attack SHA256
# Dependency : dictionary.out (Password dictionary), hashedPasswords.txt(input)
# Command    : <python find2.py>
# OUTPUT     : Passwords.txt

import timeit

start_time = timeit.default_timer() #when program start

pass_dump = {}
hash_dump = {}
count = 0

def init():
    global pass_dump, hash_dump
    with open("dictionary.out","r") as dic:
       for a in dic:
        key = a.split("|")[1].replace("\r\n","").replace("\n","") #hash
        value = a.split("|")[0] #original text
        pass_dump[key] = value

    with open("hashedPasswords.out","r") as dic:
       for a in dic:
        key = str(a.split(":")[2].replace("\r\n","").replace("\n","")) #hash
        value = a.split(":")[1] #user
        hash_dump[key] = value

    print "Init finished.."

def do_work():
    global hash_dump,pass_dump,count

    for a in hash_dump:
        try:
            if pass_dump[a]:
                count += 1
                fp = open("Passwords.txt","a")
                fp.write(str(count)+":"+hash_dump[a]+":"+pass_dump[a]+"\r\n")
                fp.close()
        except KeyError:
            pass
  
def search_word(word):
    match = re.search(r'.*'+word,pass_dump)
    if match:
        print match.group(0)
     
if __name__ == '__main__':

    init()
    do_work()

    stop_time = timeit.default_timer() #when program end

    print "Done!!"
    print str(count) + " Password(s) found. Recorded at Passwords.txt"
    print "Program Run Time : " + str(stop_time - start_time) 