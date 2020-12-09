
import pandas
import csv
import re
import os
import collections
from math import log10, floor
import json


#create an 1d array to store the total lines that was said by 6 ponys
#0 is Twilight Sparkle, 1 is Applejack, 2 is Rarity, 3 is Pinkie Pie, 4 is Rainbow Dash, 5 is Fluttershy
#6 would be the total value
verbosity = [0,0,0,0,0,0,0]

#mentions would be the same, but it would be a 2d Array
mentions=[[0]*7 for _ in range(6)]

#follow on comments would be also be a 2d array
follow_on=[[0]*8 for _ in range(6)]

#create 5 non dictionary word 2d arrays for 5 ponies

Twilight_ndw=[]
Apple_ndw=[]
Rarity_ndw=[]
pinkie_ndw=[]
rainbow_ndw=[]
fluttershy_ndw=[]

dictWord=[]

def parseDict(path):
    t=open(path, "r")
    for x in t:
        x=x.strip()
        dictWord.append(x)


def parseCSV(csvpath,dictPath):
    #TODO: change the path after move to the correct class
    f = open(csvpath,"r")
    reader = csv.reader(f)
    lis=list(reader)

    parseDict(dictPath)

    #TODO: change pos to 0
    pos=0
    total=len(lis)-1

    for i in range(len(lis)-1):
        if pos>=total : break 

        pony=lis[i][2]
        dialog=lis[i][3]

        #merge all the sentence

        if(i!=len(lis)-1 and pony!="Others"):
            while lis[i][0]==lis[i+1][0] and pony==lis[i+1][2]:
                dialog=dialog + " "+lis[i+1][3]
                del lis[i+1]
                total-=1

        #verbosity
        pony_num=find_verbosity(pony)

        if pony_num!=-1:
            verbosity[pony_num]+=1
            verbosity[6]+=1
        

            #mentions
            temp=find_mentions(dialog)
            for x in temp:
                mentions[pony_num][x]+=1
                mentions[pony_num][6]+=1

        
            #follow_by
            ponyAbove=find_verbosity(lis[i-1][2])
            if ponyAbove==-1:
                follow_on[pony_num][6]+=1
                follow_on[pony_num][7]+=1
            else:
                follow_on[pony_num][ponyAbove]+=1
                follow_on[pony_num][7]+=1

        #none-dict word
            if pony_num==0:
                Twilight_ndw.extend(none_dic_words(dialog))
            elif pony_num==1:
                Apple_ndw.extend(none_dic_words(dialog))
            elif pony_num==2:
                Rarity_ndw.extend(none_dic_words(dialog))
            elif pony_num==3:
                pinkie_ndw.extend(none_dic_words(dialog))
            elif pony_num==4:
                rainbow_ndw.extend(none_dic_words(dialog))
            elif pony_num==5:
                fluttershy_ndw.extend(none_dic_words(dialog)) 

        pos+=1

               


        


def find_verbosity(v):
    
    if v=="Twilight Sparkle" or v=="twilight sparkle" or v=="twilight Sparkle" or v=="Twilight sparkle":
        return 0
    elif v=="Applejack" or v=="applejack":
        return 1
    elif v=="Rarity" or v=="rarity":
        return 2
    elif v=="Pinkie Pie" or v=="pinkie pie" or v=="Pinkie pie" or v=="pinkie Pie":
        return 3
    elif v=="Rainbow Dash" or v=="rainbow dash" or v=="Rainbow dash" or v=="rainbow Dash":
        return 4
    elif v=="fluttershy" or v=="Fluttershy":
        return 5

    return -1
    




def find_mentions(w):
    ret = []
    if re.search(" Twilight ",w) or re.search(" Sprinkle ", w):
        ret.append(0)

    if re.search("Applejack",w):
        ret.append(1)

    if re.search("Rarity",w):
        ret.append(2)

    if re.search("Pinkie",w) or re.search(" Pie ", w):
        ret.append(3)

    if re.search("Rainbow ",w) or re.search(" Dash", w):
        ret.append(4)

    if re.search("Fluttershy",w):
        ret.append(5)

    return ret



def countWord(sentence, word):
    return sentence.split().count(word)


def none_dic_words(sentence):
    ret=[]
    sentence=sentence.lower()
    sentence=re.sub("[0-9]", "",sentence)
    sentence=re.sub("[+]", " ", sentence)
    sentence = re.sub("[^\w]", " ",  sentence).split()


    return list(set(sentence)-set(dictWord))


def output_to_set():
    data={}

    data["verbosity"]={
        'twilight': round_to_2(verbosity[0]/verbosity[6]),
        'applejack': round_to_2(verbosity[1]/verbosity[6]),
        'rarity': round_to_2(verbosity[2]/verbosity[6]),
        'pinkie': round_to_2(verbosity[3]/verbosity[6]),
        'rainbow': round_to_2(verbosity[4]/verbosity[6]),
        'fluttershy': round_to_2(verbosity[5]/verbosity[6])
    }

    data['mentions']=[]

    twi={
        'applejack': round_to_2(mentions[0][1]/(mentions[0][6]-mentions[0][0])),
        'rarity': round_to_2(mentions[0][2]/(mentions[0][6]-mentions[0][0])),
        'pinkie':round_to_2(mentions[0][3]/(mentions[0][6]-mentions[0][0])),
        'rainbow':round_to_2(mentions[0][4]/(mentions[0][6]-mentions[0][0])),
        'fluttershy': round_to_2(mentions[0][5]/(mentions[0][6]-mentions[0][0]))
    }
    data['mentions'].append({'twilight':twi})

    appl={
        'twilight': round_to_2(mentions[1][0]/(mentions[1][6]-mentions[1][1])),
        'rarity': round_to_2(mentions[1][2]/(mentions[1][6]-mentions[1][1])),
        'pinkie':round_to_2(mentions[1][3]/(mentions[1][6]-mentions[1][1])),
        'rainbow':round_to_2(mentions[1][4]/(mentions[1][6]-mentions[1][1])),
        'fluttershy': round_to_2(mentions[1][5]/(mentions[1][6]-mentions[1][1]))
    }
    data['mentions'].append({'applejack':appl})

    rari={
        'twilight': round_to_2(mentions[2][0]/(mentions[2][6]-mentions[2][2])),
        'applejack': round_to_2(mentions[2][1]/(mentions[2][6]-mentions[2][2])),
        'pinkie':round_to_2(mentions[2][3]/(mentions[2][6]-mentions[2][2])),
        'rainbow':round_to_2(mentions[2][4]/(mentions[2][6]-mentions[2][2])),
        'fluttershy': round_to_2(mentions[2][5]/(mentions[2][6]-mentions[2][2]))
    }
    data['mentions'].append({'rarity':rari})

    pink={
        'twilight': round_to_2(mentions[3][0]/(mentions[3][6]-mentions[3][3])),
        'applejack': round_to_2(mentions[3][1]/(mentions[3][6]-mentions[3][3])),
        'rarity':round_to_2(mentions[3][2]/(mentions[3][6]-mentions[3][3])),
        'rainbow':round_to_2(mentions[3][4]/(mentions[3][6]-mentions[3][3])),
        'fluttershy': round_to_2(mentions[3][5]/(mentions[3][6]-mentions[3][3]))
    }
    data['mentions'].append({'pinkie':pink})

    rainb={
        'twilight': round_to_2(mentions[4][0]/(mentions[4][6]-mentions[4][4])),
        'applejack': round_to_2(mentions[4][1]/(mentions[4][6]-mentions[4][4])),
        'rarity':round_to_2(mentions[4][2]/(mentions[4][6]-mentions[4][4])),
        'pinkie':round_to_2(mentions[4][3]/(mentions[4][6]-mentions[4][4])),
        'fluttershy': round_to_2(mentions[4][5]/(mentions[4][6]-mentions[4][4]))
    }
    data['mentions'].append({'rainbow':rainb})

    flut={
        'twilight': round_to_2(mentions[5][0]/(mentions[5][6]-mentions[5][5])),
        'applejack': round_to_2(mentions[5][1]/(mentions[5][6]-mentions[5][5])),
        'rarity':round_to_2(mentions[5][2]/(mentions[5][6]-mentions[5][5])),
        'pinkie':round_to_2(mentions[5][3]/(mentions[5][6]-mentions[5][5])),
        'rainbow': round_to_2(mentions[5][4]/(mentions[5][6]-mentions[5][5]))
    }
    data['mentions'].append({'flutershy':flut})



    data['follow_on_comments']=[]

    twi={
        'applejack': round_to_2(follow_on[0][1]/follow_on[0][7]),
        'rarity': round_to_2(follow_on[0][2]/follow_on[0][7]),
        'pinkie':round_to_2(follow_on[0][3]/follow_on[0][7]),
        'rainbow':round_to_2(follow_on[0][4]/follow_on[0][7]),
        'fluttershy': round_to_2(follow_on[0][5]/follow_on[0][7]),
        'others':round_to_2(follow_on[0][6]/follow_on[0][7])
    }
    data['follow_on_comments'].append({'twilight':twi})

    appl={
        'twilight': round_to_2(follow_on[1][0]/follow_on[1][7]),
        'rarity': round_to_2(follow_on[1][2]/follow_on[1][7]),
        'pinkie':round_to_2(follow_on[1][3]/follow_on[1][7]),
        'rainbow':round_to_2(follow_on[1][4]/follow_on[1][7]),
        'fluttershy': round_to_2(follow_on[1][5]/follow_on[1][7]),
        'others':round_to_2(follow_on[1][6]/follow_on[1][7])
    }
    data['follow_on_comments'].append({'applejack':appl})

    rari={
        'twilight': round_to_2(follow_on[2][0]/follow_on[2][7]),
        'applejack': round_to_2(follow_on[2][1]/follow_on[2][7]),
        'pinkie':round_to_2(follow_on[2][3]/follow_on[2][7]),
        'rainbow':round_to_2(follow_on[2][4]/follow_on[2][7]),
        'fluttershy': round_to_2(follow_on[2][5]/follow_on[2][7]),
        'others':round_to_2(follow_on[2][6]/follow_on[2][7])
    }
    data['follow_on_comments'].append({'rarity':rari})

    pink={
        'twilight': round_to_2(follow_on[3][0]/follow_on[3][7]),
        'applejack': round_to_2(follow_on[3][1]/follow_on[3][7]),
        'rarity':round_to_2(follow_on[3][2]/follow_on[3][7]),
        'rainbow':round_to_2(follow_on[3][4]/follow_on[3][7]),
        'fluttershy': round_to_2(follow_on[3][5]/follow_on[3][7]),
        'others':round_to_2(follow_on[3][6]/follow_on[3][7])
    }
    data['follow_on_comments'].append({'pinkie':pink})

    rainb={
        'twilight': round_to_2(follow_on[4][0]/follow_on[4][7]),
        'applejack': round_to_2(follow_on[4][1]/follow_on[4][7]),
        'rarity':round_to_2(follow_on[4][2]/follow_on[4][7]),
        'pinkie':round_to_2(follow_on[4][3]/follow_on[4][7]),
        'fluttershy': round_to_2(follow_on[4][5]/follow_on[4][7]),
        'others':round_to_2(follow_on[4][6]/follow_on[4][7])
    }
    data['follow_on_comments'].append({'rainbow':rainb})

    flut={
        'twilight': round_to_2(follow_on[5][0]/follow_on[5][7]),
        'applejack': round_to_2(follow_on[5][1]/follow_on[5][7]),
        'rarity':round_to_2(follow_on[5][2]/follow_on[5][7]),
        'pinkie':round_to_2(follow_on[5][3]/follow_on[5][7]),
        'rainbow': round_to_2(follow_on[5][4]/follow_on[5][7]),
        'others':round_to_2(follow_on[5][6]/follow_on[5][7])
    }
    data['follow_on_comments'].append({'fluttershy':flut})



    data['non_dictionary_words']=[]

    twi=collections.Counter(Twilight_ndw)
    appl=collections.Counter(Apple_ndw)
    rari=collections.Counter(Rarity_ndw)
    pink=collections.Counter(pinkie_ndw)
    rainb=collections.Counter(rainbow_ndw)
    flut=collections.Counter(fluttershy_ndw)

    data['non_dictionary_words'].append({
        'twilight': [word for word, wordcount in twi.most_common(5)],
        'applejack': [word for word, wordcount in appl.most_common(5)],
        'rarity': [word for word, wordcount in rari.most_common(5)],
        'pinkie': [word for word, wordcount in pink.most_common(5)],
        'rainbow': [word for word, wordcount in rainb.most_common(5)],
        'fluttershy': [word for word, wordcount in flut.most_common(5)]
    })

    return data

    

def round_to_2(num):
    if num==0: return 0

    return round(num,2-int(floor(log10(abs(num))))-1)
        

def write_to_file(data, path):
    f=open(path,'w+')
    json.dump(data, f)

if __name__ == "__main__":
    parseCSV('clean_dialog.csv', '../../data/words_alpha.txt')
    print(output_to_set())
    




    