# %% [markdown]
# # Developing an Information Retrieval System with Spelling Correction and Wildcard Queries
# 
# ## AmirAli Amini - 610399102
# 
# #### HW2
# 
# 

# %% [markdown]
# # توضیحات مسئله و چالش ها و بهبود ها
# 
# بزرگ ترین چالش این مسئله ساخت درخت ترای بود که با ساختن دو کلاس یکی برای هر نود و یکی برای کل درخت انجام شد
# 
# در این سوال تمام جایگشت های دوری یک رشته را با $ در انتهای آن به درست اضافه میکنم که بتوان طبق الگوریتم گفته شده در کتاب وایدکارت ها را بدست اورد؛
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
# # Code 
# در این سوال فقط به توضیح توابع اضافه شده نسبت به تمرین سری اول میپردازم
# 
# ### node:
# این کلاس به صورت مشخص ایمپلیمنت کننده هر برگ درخت ترای است
# 
# 

# %%
class node : #class node for nodes of try tree
    def __init__(self,isWord=False, myChar=None , myWord=None):
        self.myChar = myChar
        self.myWord = myWord
        self.nodes = {} # children
        self.seenChars = []  # chars in children
        self.isAWrod = isWord # boolean to check if this node indicate a valid word or not
    
    def addNode(self ,char , isWord = False):  # add a child to self and return new node
        if (char not in self.seenChars):
            newNode = node(myChar=char , myWord=self.myWord+char if self.myWord else char , isWord=isWord)
            self.nodes[char] = newNode
            self.seenChars.append(char)
            return newNode
        if isWord:
            self.nodes[char].makeWord()
        return self.nodes[char]
        
    def makeWord(self): # set self node to a valid word
        self.isAWrod=True

    def getWord (self):
        return self.myWord
    
    def getIsWord (self):
        return self.isAWrod

    def getChar (self):
        return self.myChar
    
    def includesChar(self, char):
        return char in self.seenChars
    
    def getSeenNodes (self):
        return [self.nodes[char] for char in self.seenChars]




# %% [markdown]
# ### tryTree
# این کلاس هم درخت تری را ایمپلیمنت میکند و توضیح توابع در کامنت ها نوشته شده است
# 
# تنها نکته مهم استفاده از 
# BFS 
# برای پیمایش زیر درخت هر نود است که یک نود را میگیرد و زیر درختش را پیمایش میکند و همه نود ها را برمیگرداند
# 
# 
# 
# #### getBFSWords:
# 
# این تابع کلمات ولید در نود های برگردانده شده از bfs را برمیگرداند
# 
# #### BFSPrefix: 
# تابع بی اف اس پریفیکس هم یک پیشوند برای تمام کلماتی که در درخت میخواهیم پیدا کنیم ورودی میگیرد سپس به نود ان پیشوند رفته و بی اف اس را از آن نود شروع میکند
# 
# 
# #### find:
# تابع فاند عملیات پیدا کردن وایلد کارت را رو درخت طبق الگوریتم گفته شده انجام میدهذ به این صورت که پریفیکس کلمه (مقدار قبل از ستاره) را در درخت جست و جو میکند سپس کلمات بازگشت داده شده را میچرخاند با علامت دلار در اخر آنها قرار گیرد.
# 
# برای دو ستاره نیز برای یک ستاره این کار را انجام میدهد و برای ستاره دوم بین تمام کلمات بازگشتی آنهایی که دارای مقدار بین دو ستاره هستند را برمیگرداند 
# 
# توجه شود که علارت به صورتی میچرخد که یک ستاره در انتها و بین ستاره ها کمترین حروف قرار گیرد و اینکار برای افزایش سرعت سرچ میباشد
# 
# همچنین در ابتدا تابع سرچ وایلد کارت به انتها ورودی کی علامت دلار اضافه میشود که نشان از انتها کلمه است.
# 
# 

# %%



class tryTree :
    def __init__ (self):
        self.root = node()

    def insertWord(self, word): # insert a word to tree by adding all its chars respectively
        currentNode  = self.root
        for char in range(len(word)): 
            currentNode = currentNode.addNode(word[char] , isWord = char == len(word)-1)


    def insertWordPermutation (self,inputWord): # insert all permutation of a word to the tree by adding $ to end of it
        word = inputWord+"$"
        for index in range(len(word)):
            self.insertWord(word[index:]+word[:index])

    def BFS(self , node): # BFS traversal of a subtree
        result = [node]
        for child in node.getSeenNodes():
            result+= self.BFS(child)
        return result
    
    def getBFSWords (self , node): # get valid word from result of BFS
        ls = self.BFS(node)
        return [node.getWord() for node in ls if node.getIsWord()]
    
    def prefixBFS (self, prefix= ''): # find prefix node and start BFS from it
        currentNode = self.root
        for char in range(len(prefix)): 
            currentNode = currentNode.addNode(prefix[char])
        ls = self.getBFSWords(currentNode)
        return ls

    
    def find(self, inputWord): # find wild cards in try tree
        word = inputWord
        if ('*' not in word):
            return []
        # if inputWord[-1] != "*":
        word +='$'
        startCount = word.count('*')
        if (startCount ==1):
            index = word.find('*')
            prefix = word[index+1:]+word[:index]
            ls = self.prefixBFS(prefix=prefix)
            st = set()
            for w in ls :
                index = w.find('$')
                st.add(w[index+1:]+w[:index])
            return list(st)
        elif(startCount==2):
            while (word[-1]!='*'):
                word = word[-1:]+word[:-1]
            splitWord = word[:-1].split('*')
            if len(splitWord[0])< len(splitWord[1]):
                splitWord[0], splitWord[1] = splitWord[1],splitWord[0]
            
            ls = [i for i in self.prefixBFS(prefix=splitWord[0]) if splitWord[1] in i[len(splitWord[0]):]]

            st = set()
            for word in ls :
                index = word.find('$')
                st.add(word[index+1:]+word[:index])
            return list(st)




    def prnt (self,node=None):
        root = self.root
        if (node):
            root = node
        print (self.getBFSWords(root) )
    


# %% [markdown]
# # ADDED FUNCTIONS:
# 
# 
# #### findDistance:
# پیدا کردن فاصله دو کلمه با استفاده از الگوریتم گفته شده در اسلاید ها
# 
# 
# #### spellCheckingSingleWord:
# مقایسه کلمه ورودی با همه کلمات پستینگ لیست و بازگرداندن کمترین فاصله
# 
# در ایتدا چک میشود اگر کلمه در در پستینگ لیست وجود داشت آنرا برمیگردانیم
# 
# 
# #### spellCheckingExpressions:
# برای تک تک ورد های عبارت ورودی اسپل چکینگ را انجام میدهد و ترکیب آنها را برمیگرداند
# 
# #### findQueryWord:
# با استقاده از تابع فایند درخت سرچ وایلد کارد را برای یک کلمه انجام میدهد
# 
# 
# #### findQuery:
# عبارت را همانند تمرین قبل تجزیه کرده و برای کلمات ستاره دار وایلد کارد و برای کلمات بدون ستاره اسپل چکینگ را انجام میدهد سپس تمام کویری ها ممکن را میسازد و با اجتماع گرفتن از همه نتیجه ها، نتیجه نهایی را برمیگرداند
# 
# 

# %%

class searchEngine:
    def __init__(self , debug = False) -> None: # constructor of class
        self.debug = debug
        self.postingList =[]
        self.files=[] 
        self.stop = set(stopwords.words('english') + list(string.punctuation)) # all extra expression which should ignore
        self.tryTree = tryTree()

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

            self.tryTree.insertWordPermutation(word)


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
            






# HW2 : codes of homework 2

    def findDistance (self,inputWord, baseWord ,printOff=True ): # this function is used to find distance of each word if posting list with input word
        inWord = " "+inputWord
        bWord = " "+baseWord
        distanceMatrix = [[0]* len(bWord) for _ in range(len(inWord))] # quantified the matrix
        for i in range(len(bWord)):
            distanceMatrix[0][i]=i
        for i in range(len(inWord)):
            distanceMatrix[i][0]=i

        for row in range(1,len(inWord)): # fill the matrix using dynamic programming algorithm
            for column in range(1,len(bWord)):
                deleteScore = distanceMatrix[row-1][column] +1
                insertScore = distanceMatrix[row][column-1] +1
                copyOrReplaceScore = distanceMatrix[row-1][column-1] 
                if bWord[column] != inWord[row]:
                    copyOrReplaceScore+=1
                distanceMatrix[row][column] = min(deleteScore , insertScore , copyOrReplaceScore)
                self.debugPrint (f'min is {distanceMatrix[row][column]} for {(deleteScore , insertScore , copyOrReplaceScore)} {row}, {column}' ,printOff=printOff)
 
        self.debugPrint(np.array(distanceMatrix),printOff=printOff)
        return distanceMatrix[-1][-1] # return the result



    def spellCheckingSingleWord (self,inputWord,printOff=True): # call "def findDistance ()" for all words in posting list with input word
        index = self.searchPostingList(inputWord) # check if spell is correct (word exists in posting list)
        if (index< len(self.postingList)):
            if (self.postingList[index]["word"] == inputWord):
                return [inputWord]
            
        allWords = [item['word'] for item in self.postingList]
        distances = [[] for _ in range(100) ]
        for baseWord in allWords:
            currentDistance = self.findDistance(inputWord, baseWord ,printOff=True) # call "def findDistance ()" for all words in posting list with input 
            distances[currentDistance].append(baseWord) # add new distance to distances list
        self.debugPrint (distances,isMatrix=True, printOff=printOff)
        for item in distances:
            if(len(item)):
                return item
        return []
            

    def spellCheckingExpression(self, expression, printOff = True): # split the expression and check spell for all parts the concat them together
        # tokenize input and remove stop words and ponctuations
        tokenizedExpression= [word for word in word_tokenize(expression.lower(),preserve_line=False) if word not in self.stop] 
        answersLists = [] # list of all near words for each token
        for word in tokenizedExpression:
            answersLists.append(self.spellCheckingSingleWord(word))
        self.debugPrint(answersLists, printOff=printOff)

        results = []

        for ls in answersLists: # multiply lists founded before
            temp =[]
            if (len(results)):
                for wordResult in results:
                    for word in ls:
                        temp.append(f'{wordResult} {word}')
                results = temp
            else :results = copy.copy(ls)

        self.debugPrint(results, printOff=printOff)
        return results
    

    def findQueryWord (self, word ) : # I do my wild search in my tree class
        wildcardFind = self.tryTree.find(word)
        return wildcardFind


    def findQuery (self, query ,printQueries=True) :
        splitQuery = query.lower().split()
        if ('*' not in query): # check if query is a wild card
            # query does not contains any wildcard
            if (len(splitQuery) == 3): # complicated query
                # spell checking for both of sides
                spellCheckFind1 = self.spellCheckingExpression(splitQuery[0]) 
                spellCheckFind2 = self.spellCheckingExpression(splitQuery[2])
                results = set()
                for spellItem1 in spellCheckFind1:
                    for spellItem2 in spellCheckFind2: # make results
                        if printQueries: print (f'query : {spellItem2} {splitQuery[1]} {spellItem1}')
                        results = results.union(set(self.find(f'{spellItem2} {splitQuery[1]} {spellItem1}')))
                    return list(results)
                return self.find(query)
            else: # simple query - just spellchecking 
                spellCheckFind = self.spellCheckingExpression(splitQuery[0])
                results = set()
                for item in spellCheckFind:
                    results=results.union(set(self.find(item)))
                return list(results)

        # query contains some wildcards 

        if (len(splitQuery) == 3): # complicated query
            if '*' not in splitQuery[0]: 
                splitQuery[0],splitQuery[2] = splitQuery[2],splitQuery[0] # move wildcard to left side

            wildcardFind = self.tryTree.find(splitQuery[0]) # search wildcard
            spellCheckFind = self.spellCheckingExpression(splitQuery[2]) # checking spell
            self.debugPrint(wildcardFind)
            results = set()
            for spellItem in spellCheckFind: # make results
                # search 
                for wildItem in wildcardFind:
                    if printQueries: print (f'query : {wildItem} {splitQuery[1]} {spellItem}')
                    results = results.union(set(self.find(f'{wildItem} {splitQuery[1]} {spellItem}')))
                # print(f'{item} {splitQuery[1]} {splitQuery[2]}' ,set(self.find(f'{item} {splitQuery[1]} {splitQuery[2]}')) ,results)
            self.debugPrint(wildcardFind,isMatrix=False)
            self.debugPrint(splitQuery,isMatrix=True)
            return list(results)
        
        else: # simple query with one wildcard
            wildcardFind = self.tryTree.find(splitQuery[0]) 
            results = set()
            for item in wildcardFind:
                results = results.union(set(self.find(item))) # find all documents contain result of wild card searching
            return list(results)
        

        







        




                        
            

            
    def debugPrint(self, value ,isMatrix = False, printOff=False):
        if (self.debug and not printOff):
            if (isMatrix):
                for row in value:
                    print(row)
            else:
                print(value)
        


    def prnt(self):
        for i in self.postingList:
            print(i)




# %% [markdown]
# # Test cases:

# %%
test = searchEngine()

test.input(['document1.txt','document2.txt','document3.txt'])


# %% [markdown]
# 

# %%
test.spellCheckingExpression('amrali ani astam man',printOff=True)

# %%
print(test.findQuery( "amir or ex*m*le"))

# %%
print(test.findQuery('c*s and several'))

# %%
print(test.findQuery('c*s or several'))

# %%
print(test.findQuery('c*s* near/3 several'))

# %%
print(test.findQuery('s*l* near/3 several'))

# %% [markdown]
# # Docs WildCards

# %%
import os
directory_input = ['docs/'+path for path in os.listdir('docs') if path[-3:] == 'txt']
print(directory_input)

# %%
test_directory = searchEngine()
test_directory.input(directory_input)

# %%
result=test_directory.findQuery("People")
print(result)
for file in [directory_input[index-1] for index in result]:
    print(file)

# %%
result=test_directory.findQuery("los")
print(result)
for file in [directory_input[index-1] for index in result]:
    print(file)

# %%
result = test_directory.findQuery("People and Los")
print(result)
for file in [directory_input[index-1] for index in result]:
    print(file)

# %%
result = test_directory.findQuery("People OR Los")
print(result)
for file in [directory_input[index-1] for index in result]:
    print(file)

# %%
result = test_directory.findQuery("piano near/4 said")
print(result)
for file in [directory_input[index-1] for index in result]:
    print(file)

# %%
result = test_directory.findQuery("pia*o near/4 said")
print(result)
for file in [directory_input[index-1] for index in result]:
    print(file)

# %%
result = test_directory.findQuery("p*a*o near/4 said")
print(result)
for file in [directory_input[index-1] for index in result]:
    print(file)

# %%
result = test_directory.findQuery("p*a near/4 said")
print(result)
for file in [directory_input[index-1] for index in result]:
    print(file)


# %%
result = test_directory.findQuery("*p*a near/4 said")
print(result)
for file in [directory_input[index-1] for index in result]:
    print(file)


# %% [markdown]
# # DOCS

# %% [markdown]
# ## Docs Spell Checking
# ### Input – Spell Checking

# %%
result = test_directory.spellCheckingExpression("festivsl funders")
for item in result:
    print (item)

# %%
result = test_directory.spellCheckingExpression("contrnt")
for item in result:
    print (item)

# %% [markdown]
# ## Docs findWildCardWord
# ### Input – Information Retrieval System

# %%
print( test_directory.findQueryWord("n*b*y"))


# %% [markdown]
# ## Docs WildCardQuery
# ### Input – Wildcard Queries

# %%
result = test_directory.findQuery("exa*le AND content")
print(result)
for file in [directory_input[index-1] for index in result]:
    print(file)

# %%
result = test_directory.findQuery("l*e* AND popila")
print(result)
for file in [directory_input[index-1] for index in result]:
    print(file)

# %% [markdown]
# # TESTS

# %% [markdown]
# # Input – Information Retrieval System

# %%
test = searchEngine()

test.input(['document1.txt','document2.txt','document3.txt'])

# %%
result = test.findQuery("exa*le AND contrnt")
print(result)
for file in [directory_input[index-1] for index in result]:
    print(file)

# %%


# %%



