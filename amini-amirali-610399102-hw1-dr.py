# %% [markdown]
# # Developing an Information Retrieval System with Advanced Boolean Search
# 
# ## AmirAli Amini - 610399102
# 
# #### HW1
# 

# %% [markdown]
# # توضیحات مسئله و چالش ها و بهبود ها
# 
# بزرگ ترین چالش مسئله ساختار پستینگ لیست که برای سیو کردن مقادیر استفاده میشود بود چرا که باید به صورتی ذخیره شوند که برای هر داکیومنت علاوه بر شامل بود کلمه ، ایندکس های آن کلمه هم ذخیره شود.
# 
# در این مسئله از ساختاری سریع تر از لینک لیست برای دسترسی به دیتا استفاده کردم
# 
# همچنین از باینری سرچ برای بهبود سرعت پیدا کردن دیتا استفاده میکنم
# 
# میتوان تمام دیکشنری های استفاده شده را با ارایه دو بعدی جایگذین کرد که تاثیری در سرعت کد زده شده ندارد و تنها خوانایی کد پایین اورده میشود
# 
# 

# %% [markdown]
# ## کتابخانه ها 
# 
# ###  from nltk import word_tokenize :
# از این کتابخانه برای تکنایز کردن داده ها به این دلیل که توکنایز کردن دیتا سریع تر میشه استفاده کردم
# 
# ###  from nltk.corpus import stopwords :
# از این کتابخانه برای دریافت استاپینگ ورد های زبان انگلیسی استفاده کردم
# 
# ###  import string:
# از این کتابخانه برای دریافت پانچویشن های زبان انگلیسی استفاده کردم
# 
# ###  import numpy as np:
# از این کتابخانه برای جمع یک عدد با تمام اعضای یک آرایه استفاده کردم
# 
# ###  import copy:
# از این کتابخانه برای دیپ کپی کردن ارایه استفاده کردم

# %%
from nltk.tokenize import word_tokenize


from nltk.corpus import stopwords # a library to tokenize input texts

import nltk


nltk.download('punkt')
nltk.download('stopwords') # stopping word in English language

import string # using to remove punctuation

import numpy as np

import copy

# %% [markdown]
# ## Code 
# برای رسیدن به هدف سوال، یک 
# "posring list"
# با ساختار
# list of {word : nameOfWord , docs :[list of {doc:nameOfDocument , indexes: indexes of the word if this document}]}
# میسازم که هر خانه متناظر با یک کلمه است و ساختاری به صورت گفته شده دارد
# 
# در این ساختار داکیومنت هایی که دارای این کلمه هستند در این قسمت ذخیره میشووند به این صورت که ایندکس هایی که برابر آن کلمه در آن داکیومنت هستند نگهداری میشود
# 
# دلیل نگه داری اندکس کلمات در داکیومنت ها این است که در آینده بتوان با متد 
# 
# near
# 
# اختلاف مکانی دو کلمه را پیدا کرد
# 
# 
# کلیت ساخت پستینگ لیست به این صورت است که کلمات هر داکیومنت را نگاه میکند در پستینگ لیست پس از پیدا کردن کلمه مورد نظر، مقدار ایندکس آن در داکیومنت حاضر و شماره داکیومنت ثبت میشود
# 
# توضیحات جزئی تر در کد به صورت کامنت نوشته شده است
# 
# 
# ### input:
# تابع اینپوت ادرس داکیومنت ها را ورودی میگیرد و برای هر داکیومنت عملیات اضافه کردن به پستینگ لیست را انجام میدهد
# 
# ### findWord:
# این تابع ایندکس متناظر با کلمه سرج شده را خروجی میدهد
# 
# ### find:
# این در مرحله اول کویری داده شده را تجزیه میکند به ۳ کتگوری اصلی تقسیم بندی میشود
# 
# - تک کلمه
# - بولین
# - همسایگی
# 
# #### single word:
# برای تک کلمه به صورت مستثیم از تابع فایند ورد استفاده میکنم و ایندکس داکیومنت های آن را برمیگردانم
# 
# #### boolean:
# برای بولین ها داکیومنت های هر کلمه را به همانند تک کلمه پیدا میکنم  
# 
# ##### AND:
# اشتراک لیست های بدست آمده را برمیگردانم
# 
# ##### OR:
# اجتماع لیست های بدست آمده را برمیگردانم
# 
# 
# ### NEAR:
# برای کلمه اول و دوم برای هرکدام یک دیکشنری از داکیومنت های دارای آن کلمه میسازم که کلید آن اندکس داکیومنت و مقدار آن ایندکس کلمه در آن داکیومنت است
# 
# برای هر دوداکیومنت مشترک در در دو کلمه ماتریس قدرمطلق فاصله متناظر با عضو های هردو را میسازم و مینیمم فاصله را بدست می آورم
# 
# اگر کوچک تر از عدد خواسته شده بود آن داکیومنت را به جواب اضافه میکنم

# %% [markdown]
# # input 1 , text2.txt : 
# aa aa  aa bb bb bb zz zz ll mm mm  aa aa ll 
# 
# 
# amir ali amini amir hossein hasani
# 
# 
# # input 2 , test.tst:
# amirali , amini, hastam salam. amirali , amirali aa bb

# %%

class searchEngine:
    def __init__(self) -> None: # constructor of class
        self.postingList =[]
        self.files=[] 
        self.stop = set(stopwords.words('english') + list(string.punctuation)) # all extra expression which should ignore

        # structure of postingList : list of {word : nameOfWord , docs :[list of {doc:nameOfDocument , indexes: indexes of the word if this document}]}


    # binary search to find a word in posting list
    def searchPostingList(self, word):
        s= 0 
        e = len(self.postingList)
        if e <=0 :
            return 0
        e-=1
        while (1):
            if (e-s < 2):
                if (self.postingList[e]["word"] < word):
                    return e+1
                if (self.postingList[e]["word"] == word):
                    return e
                if (self.postingList[s]["word"] >= word):
                    return s

                return e
            mid = (s+e)/2
            mid = int(mid)
            if (word<self.postingList[mid]["word"]):
                e=mid
            elif (word> self.postingList[mid]["word"]):
                s = mid
            else :
                return mid
            
        # {word:str, indexes:list(int)}
    # binary search to find a word in each dictionary
    def searchDictionary(self, word,ls):
        s= 0 
        e = len(ls)
        if e <=0 :
            return 0
        e-=1
        while (1):
            if (e-s < 2):
                if (ls[e]["doc"] < word):
                    return e+1
                if (ls[e]["doc"] == word):
                    return e
                if (ls[s]["doc"] >= word):
                    return s

                return e
            mid = (s+e)/2
            mid = int(mid)
            if (word<ls[mid]["doc"]):
                e=mid
            elif (word> ls[mid]["doc"]):
                s = mid
            else :
                return mid


            
        # {doc:number, indexes:list(int)}



    def addToPostingList(self, tokenizedText: list[str],docIndex:int): # add tokenized word in posting list 
        for i in range(len(tokenizedText)):
            word = tokenizedText[i]
            index = self.searchPostingList(word) # find index of word in posting list
            if (len(self.postingList)>index): # check if index is not larger than posting list (if word is bigger that all words, search function returns len(postingList)+1)
                if (self.postingList[index]["word"] == word): # check if index is the index of the word
                    if (self.postingList[index]["docs"][-1]["doc"] == docIndex): # if we have already added the document index 
                        self.postingList[index]["docs"][-1]["indexes"].append(i) # as we read tokens in order of their index, we need to add token in end of the list

                    else:
                        self.postingList[index]["docs"].append({"doc":docIndex,"indexes":[i] }) # if we have not already added the document and dou to the fact that they are read in order of their index, we can easily add append new one in end of the list 

                else :
                    self.postingList[index:index]= [({"word":word , "docs":[{"doc":docIndex , "indexes":[i]}]})] # word is bigger that all other words => we can append it to end of the list

            else :
                self.postingList.append({"word":word , "docs":[{"doc":docIndex , "indexes":[i]}]}) # we have not already added the word and dou to the fact that they are read in order of their index, we can easily add append new one in end of the list


    def input (self, filePath: list[str]): # input paths of inputs
        for i in range(len(filePath)): # for files in input
            file = open(filePath[i],'r',encoding='cp1252') # open the file
            text = file.read() # read the file
            file.close()  # close the file
            # tokenize text and ignore stopping words using nltk library 
            tokenizedText = [word for word in word_tokenize(text.lower(),preserve_line=False) if word not in self.stop] 
            print (f'document {i+1} : {filePath[i]}')
            # print(tokenizedText)
            self.addToPostingList(tokenizedText , i+1) # i indicates to index of document we are reading


    def findWord(self, word): # this function use our binary search function to find word in posting list and if the word is not included in the list, returns -1
        index = self.searchPostingList(word)
        if (index< len(self.postingList)):
            if (self.postingList[index]["word"] == word):
                return index # real index of the word
        return -1 # word is not in the posting list


    def find(self , query:str): # split the query and find the result 
        splitQuery = query.lower().split()
        if (len(splitQuery)==1): # query is only one word
            index = self.findWord(splitQuery[0])
            if (index>-1):
                return [ i["doc"] for i in self.postingList[index]["docs"]]
            return []

        else: 
            index1 = self.findWord(splitQuery[0])
            index2 = self.findWord(splitQuery[2])
            if splitQuery[1] in ["and" ,"or", "AND", "OR"]: # boolean condition
                
                if (splitQuery[1] in ["and","AND"]): # and condition
                    if(index1!=-1 and index2!=-1): # check if there are result for both of words
                        docs1 =  set([ i["doc"] for i in self.postingList[index1]["docs"]]) # find document of word one 
                        docs2 =  set([ i["doc"] for i in self.postingList[index2]["docs"]]) # find document of word two 
                        # print(self.postingList[index1]["docs"] , self.postingList[index2]["docs"])
                        return list(docs1.intersection(docs2)) # make intersection of two results
                    return []
                    
                if (splitQuery[1] in ["or","OR"]): # or condition
                    if(index1!=-1 and index2!=-1): # check if there are result for both of words
                        docs1 =  set([ i["doc"] for i in self.postingList[index1]["docs"]])
                        docs2 =  set([ i["doc"] for i in self.postingList[index2]["docs"]])
                        # print(self.postingList[index1]["docs"] , self.postingList[index2]["docs"])
                        return list(docs1.union(docs2))
                    if(index1!=-1): return [ i["doc"] for i in self.postingList[index1]["docs"]] # check if there is result for first word
                    return [ i["doc"] for i in self.postingList[index2]["docs"]] # check if there is result for second word

            else : # near condition
                nearNumber = int(splitQuery[1].split('/')[1]) # find near 
                if(index1!=-1 and index2!=-1): # check if there are result for both of words
                    docs1 =   {i["doc"]:i["indexes"] for i in self.postingList[index1]["docs"]} # find document of word one and make dictionary for result
                    docs2 =   {i["doc"]:i["indexes"] for i in self.postingList[index2]["docs"]} # find document of word two and make dictionary for result

                    result = [] 
                    keysOfDocs2 = docs2.keys()
                    for key, value in docs1.items():
                        if (key in keysOfDocs2):
                            d1 = np.array(value) # indexes of word in first document
                            d2 = np.array(copy.deepcopy(docs2[key])) # indexes of word in second document
                            distanceMatrix = np.array([[abs(i - j )for i in d1] for j in d2]) # distance matrix
                            if (distanceMatrix.min() <= nearNumber): # check validation
                                result.append(key)


                            # example of distanceMatrix
                            # 
                            # [[ 0  1  2 10 11]
                            # [ 1  0  1  9 10]
                            # [ 2  1  0  8  9]
                            # [10  9  8  0  1]
                            # [11 10  9  1  0]]


                    return result
                return []



                        
            

            
        



    def prnt(self):
        for i in self.postingList:
            print(i)




# %% [markdown]
# # My Tests:

# %%
test = searchEngine()

test.input(['text1.txt' , "test.txt"])

# %%
print(test.find("amirali and aa"))

# %%
print(test.find("amirali or aa"))

# %%
print(test.find("amirali or ii"))

# %%
print(test.find("amirali n/3 amini"))

# %%
print(test.find("hasani n/3 amini"))

# %%
print(test.find("aa n/3 aa"))

# %%
test.prnt()

# %% [markdown]
# # Test Cases: 

# %%
testCase  = searchEngine()
testCase.input(['document1.txt','document2.txt','document3.txt'])

# %% [markdown]
# ## Boolean Test
# ### Input Boolean Query
# 
# expected results = [2, 3]

# %%
testCase.find('example AND content')

# %% [markdown]
# ## Near
# ### Input proximity Query
# 
# expected results proximity = [2]

# %%
testCase.find('example NEAR/3 content')


# %%
import os

# %%
directory_input = ['docs/'+path for path in os.listdir('docs') if path[-3:] == 'txt']
print(directory_input)

# %% [markdown]
# # docs
# 

# %%
test_directory = searchEngine()
test_directory.input(directory_input)
test_directory.prnt()

# %%
result=test_directory.find("People")
print(result)
for file in [directory_input[index-1] for index in result]:
    print(file)

# %%
result=test_directory.find("Los")
print(result)
for file in [directory_input[index-1] for index in result]:
    print(file)

# %%
result = test_directory.find("People and Los")
print(result)
for file in [directory_input[index-1] for index in result]:
    print(file)

# %%

result = test_directory.find("People OR Los")
print(result)
for file in [directory_input[index-1] for index in result]:
    print(file)

# %%
result = test_directory.find("piano near/4 said")
print(result)
for file in [directory_input[index-1] for index in result]:
    print(file)



# %%



