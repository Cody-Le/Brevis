import sys
import re
import requests
from bs4 import BeautifulSoup as bs
from bs4.element import Comment
import nltk
from PyDictionary import PyDictionary
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
import pandas as pd
try:
    from googlesearch import search
except:
    print('search module not found')



#set up nltk
nltk.download('stopwords')
lemmatizer = WordNetLemmatizer()
dictionary = PyDictionary()

#define global variable
paragraph = []
command = None




def look(query,num_results):
    global totalWord
    totalWord = 0
    # use google api to search for link with query and return a certain result
    results =  search(query, tld="com", num=2, stop=num_results, pause=2)
    links = []
    for j in results:
        print(j)
        links.append(j)
    for j in links:
        try:
            print(j)
            html_content = requests.get(j).text
            soup = bs(html_content, "html.parser")
            print("Extracted the html and souped, proceeding")
            for tag in ['script', 'button','nav', 'a', "style"]:
                for t in soup.select(tag):
                    t.extract()
            texts = soup.find('body')
            if len(texts.get_text()) >= 1600:
                paragraph.append(texts.get_text())
                totalWord += len(texts.get_text())
        except:
            continue
 
def summary(texts, sentResults):

    wordRank = {}#the rank of all the word
    sentRank = {}#the rank of all the sentence base on the word within
    #get the text, find the highest occurence of words
    #find their own gramatical counter part
    for text in texts:
        for sign in [',','.','"','...',':', "?","'", '_', '`', '(', ')', '!', "*", '%', '~', '[', ']', '|', "@", '!', '<', '>']:
            text = text.replace(sign, "")
    
        
        instanceText =  word_tokenize(text.lower())#Instance of the real text
        instanceText = [word for word in instanceText if not word in stopwords.words('English')]
        
        for word in instanceText:
            #lemantized word
            try:
                try:
                    lm_word = lemmatizer.lemmatize(word, pos = wn.synsets(word)[0].pos())
                    if lm_word in wordRank: #check if the word is already in the rank table
                        wordRank[lm_word.lower()] += 1 #update the frequency
                    else:
                        wordRank[lm_word.lower()] = 1 #reset the frequency, giving a default frequency to add on later
                except:
                    reword = re.sub("^\W","", word)
                    lm_word = lemmatizer.lemmatize(reword, pos = wn.synsets(reword)[0].pos())
                    if lm_word in wordRank: #check if the word is already in the rank table
                        wordRank[lm_word.lower()] += 1 #update the frequency
                    else:
                        wordRank[lm_word.lower()] = 1 #reset the frequency, giving a default frequency to add on later
            except:
                if word in wordRank: #check if the word is already in the rank table
                    wordRank[word.lower()] += 1 #update the frequency
                else:
                    wordRank[word.lower()] = 1 #reset the frequency, giving a default frequency to add on later     
            
            
    #show table
    print("------------------------------------------------------------------------")
    df = pd.DataFrame(sorted(wordRank, reverse = True, key = wordRank.get), columns =['word'])
    print(df)
    df = pd.DataFrame.from_dict(wordRank,columns =['frequency'], orient ="index")
    print(df)
    
    #split and get the sentence with the most point

    for text in texts:

        sentenceList = sent_tokenize(text)
        for sentence in sentenceList:
            score = 0

            for word in sentence:
                try:
                    lm_word = lemmatizer.lemmatize(word, pos = wn.synsets(word)[0].pos())# lemantized the word
                    score += wordRank.get(lm_word, default = 0) #check the number of frequency of each word in its lemantized form
                except:
                    continue
            sentRank[sentence] = score
    #return the highest socre sentences
    sortedSent = sorted(sentRank, key = sentRank.get, reverse = True)
    print(sortedSent)
    sys.stdout.flush()
    sentences = []
    global resultWord
    resultWord = 0
    for sent in sortedSent:
        sentence = ""
        words = word_tokenize(sent)
        for word in words:
            if word != " ":
                if word in ['.', ',', '?', ':']:
                    sentence += word
                elif word in ['"', ")"]:
                    sentence += word + ' ' 
                else:
                    sentence += ' ' + word
        if len(sentence) >= 30:
            sentences.append(sentence)
            resultWord += len(sentence)
    print("Short", resultWord/totalWord * 100, "%")
    print("------------------------------------------------------------------------")
    return sentences[0:sentResults]

lookAmt = 30
resultAmt = 5
  
x = input("Search for summary: ")
    
look(x, lookAmt)
i = 1
for suma in summary(paragraph, resultAmt):
    print('[' + str(i) + ']', suma)
    i += 1
    


    
