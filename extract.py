# -*- coding: <UTF-8> -*-
from collections import defaultdict
import json
import os,sys
import html
import io
path = "/home/gulab/Desktop/bhagvate/sb/"
dirs = os.listdir( path )

words=defaultdict(lambda : defaultdict(list))	    #global database

def find_all(a_string, sub):
    result = []
    k = 0
    while k < len(a_string):
        k = a_string.find(sub, k)
        if k == -1:
            return result
        else:
            result.append(k)
            k += 1 #change to k += len(sub) to not search overlapping results
    return result

def check_int(c):
	if c=='0' or c=='1' or c=='2' or c=='3' or c=='4' or c=='5' or c=='6' or c=='7' or c=='8' or c=='9':
		return 1
	return 0

def main():
	dash = "—"
	#outer loops to traverse the directories
	for subdir in dirs:
		if os.path.isdir(path + subdir) :
			subdirs = os.listdir( path  + subdir + "/")
			#print(subdir + " :")
			for subsubdir in subdirs :
				if os.path.isdir(path + subdir + "/" + subsubdir) :
					subsubdirs = os.listdir( path  + subdir + "/" + subsubdir + "/")
					for files in subsubdirs :
						if files.find(".htm")!=-1 :
							filename=files[0:len(files)-4]
							if check_int(filename[0])==1 :
								filepath=path  + subdir + "/" + subsubdir + "/" + files
								#reached the innermost directory and file
								fo =  open(filepath,"r")
								check = fo.read()
								fo.close()

								#extracting the word-meaning section from the entire html file
								check=check[check.find("SYNONYMS"):check.find("TRANSLATION")+20]

								#removing the html tags from the data
								while check.find("<")!=-1 :
									l=check.find("<")
									r=check.find(">")
									if l==0 :
										check=check[r+1:]
									elif r==len(check)-1 :
										check=check[0:l]
									else :
										check=check[0:l]+check[r+1:]

								# Converting into unicode
								check = html.unescape(check)

								#finding all occurences of "—" and storing the indexes in a list
								list = find_all(check,dash)

								#removing redundant "—"  (which do not separate word-meaning)
								n=len(list)
								i=1
								while i<n:
									if i<n :
										current = check[list[i-1]+2:list[i]]
										if current.find(";") == -1:
											del list[i]
											i-=1
											n-=1
									i=i+1

								x = check.find("SYNONYMS")      
								word=check[x+8:list[0]-1]             #first word (just after SYNONYMS)
								#loop to get word and meaning pairs between dashes stored in list  
								for i in range(1,len(list),1):
									current = check[list[i-1]+1:list[i]]
									if current.find(";") == -1 and i<len(list)-1:
										del list[i]
										current = check[list[i-1]+1:list[i]]
									index = current.rfind("; ")
									meaning = current[1:index]      
									words[word][meaning].append("sb/" + subdir + "/" + subsubdir + "/" + files)   #adding the collected data from file into the global database
									# if subdir + "/" + subsubdir + "/" + files == "10/2/27.htm" :
									# 	print(word)
									# 	print(meaning)
									# 	print("\n")
									word=current[index+2:len(current)-1]

								x = check.find("TRANSLATION")
								meaning=check[list[len(list)-1]+8:x-1]    #last meaning (just before TRANSLATION)
								words[word][meaning].append("sb/" + subdir + "/" + subsubdir + "/" + files)   

	with io.open("data.txt", "w", encoding="utf8") as f:									# writing data as json string in unicode
		json.dump(words,f,indent=4,ensure_ascii=False,sort_keys=True)

main()
