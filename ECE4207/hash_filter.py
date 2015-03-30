import hashlib,re,string

i = 1
with open("rock2.txt") as f:
 for line in f:
     raw_pw = line.split(":")[0].replace('\r\n','').replace('\n','')
     if len(raw_pw) < 20 and len(raw_pw) >= 8:
          if re.search("[\!\-\~]",raw_pw) > -1:
               if re.search("[0-9]",raw_pw) > -1: 
                  if re.search("[A-Z]",raw_pw) > -1: 
         	        hash_text = hashlib.sha256(raw_pw).hexdigest()
         	        fp = open("aa.out","a")
                 	fp.write(str(i)+":"+raw_pw+":"+hash_text+"\r\n")
                 	fp.close()
                 	i+=1
         