import sys
import re
import requests
from bs4 import BeautifulSoup as bs
import nltk
from PyDictionary import PyDictionary
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
import pandas as pd
from ftfy import fix_text
from googleLInk import lookup
from imgGet import imgGetter
import multiprocessing
from multiprocessing import Manager, Value
from ctypes import c_char_p
import time


#set up nltk



#define global variable

command = None
class brevis():
    def __init__(self, query, lookAmt = 15, resultAmt = 5, shortResult = False, paragraph = [], totalWord = 0, links = [], j ='', ):
        self.paragraph = paragraph
        self.query = query
        self.lookAmt = lookAmt
        self.resultAmt = resultAmt
        self.shortResult = shortResult
        self.totalWord = totalWord
        self.links = []
        self.j = j

        self.setup()


    def setup(self):
        nltk.download('stopwords')
        self.lemmatizer = WordNetLemmatizer()
        dictionary = PyDictionary()

    def firstImage(self):
        getter = imgGetter(self.query)
        img = getter.getImg()
        return img

    def soupHTML(self):
        html_content = requests.get(self.j).text
        soup = bs(html_content, "html.parser")
        for tag in ['script', 'button', 'nav', 'a', "style", 'list', 'ul', 'form', 'input']:
            for t in soup.select(tag):
                t.extract()
        texts = soup.find('body')
        if len(texts.get_text()) >= 1600:
            print(texts.get_text())
            self.string.value = texts.get_text()
            self.currentLength.value = len(texts.get_text())
            print("Extracted the html and souped, proceeding")


    def look(self):

        self.totalWord = 0
        # use google api to search for link with query and return a certain result
        searchEngine = lookup(self.query, results=self.lookAmt)
        results = searchEngine.search()
        self.links = []
        for j in results.values():
            print(j)
            if re.findall('favicon.io', j):
                continue
            else:
                self.links.append(j)

        i = 0
        for j in self.links:

            try:
                print(i)
                self.j = j
                manager = Manager()
                self.string = manager.Value(c_char_p, '')
                self.currentLength = Value('d', 0.0)
                p = multiprocessing.Process(target=self.soupHTML)
                p.start()
                p.join(60)
                if p.is_alive():
                    print('Souping is taking too long, terminating for', j)
                    p.terminate()
                    p.join
                self.paragraph.append(self.string.value)
                i += 1
                self.totalWord += self.currentLength.value


            except:
                continue
    def citation(self):
        if self.links == None:
            return None
        else:
            return self.links



    def summary(self):
        returnObj = {} #this is the object will be return in a json like type
        wordRank = {}  # the rank of all the word
        sentRank = {}  # the rank of all the sentence base on the word within
        # get the text, find the highest occurence of words
        # find their own gramatical counter part
        for text in self.paragraph:
            for sign in [',', '.', '"', '...', ':', "?", "'", '_', '`', '(', ')', '!', "*", '%', '~', '[', ']', '|',
                         "@", '!', '<', '>', '{', ')', '&',';', 'â€™', 'ref=harv', 'cs1', "''", '``','p', 'â€', 'â€™', '}', 'u']:
                text = text.replace(sign, "")

            instanceText = word_tokenize(text.lower())  # Instance of the real text
            instanceText = [word for word in instanceText if not word in stopwords.words('English')]

            for word in instanceText:
                # lemantized word
                try:
                    try:
                        lm_word = self.lemmatizer.lemmatize(word, pos=wn.synsets(word)[0].pos())
                        if lm_word in wordRank:  # check if the word is already in the rank table
                            wordRank[lm_word.lower()] += 1  # update the frequency
                        else:
                            wordRank[
                                lm_word.lower()] = 1  # reset the frequency, giving a default frequency to add on later
                    except:
                        reword = re.sub("^\W", "", word)
                        lm_word = self.lemmatizer.lemmatize(reword, pos=wn.synsets(reword)[0].pos())
                        if lm_word in wordRank:  # check if the word is already in the rank table
                            wordRank[lm_word.lower()] += 1  # update the frequency
                        else:
                            wordRank[
                                lm_word.lower()] = 1  # reset the frequency, giving a default frequency to add on later
                except:
                    if word in wordRank:  # check if the word is already in the rank table
                        wordRank[word.lower()] += 1  # update the frequency
                    else:
                        wordRank[
                            word.lower()] = 1  # reset the frequency, giving a default frequency to add on later

        # show table
        print("------------------------------------------------------------------------")
        df = pd.DataFrame(sorted(wordRank, reverse=True, key=wordRank.get), columns=['word'])
        print(df)
        df = pd.DataFrame.from_dict(wordRank, columns=['frequency'], orient="index")
        print(df)

        # split and get the sentence with the most point

        for text in self.paragraph:

            sentenceList = sent_tokenize(text)
            for sentence in sentenceList:
                score = 0
                for word in word_tokenize(sentence):
                    try:
                        lm_word = self.lemmatizer.lemmatize(word, pos=wn.synsets(word)[0].pos())  # lemantized the word
                        score += wordRank[lm_word]  # assigned point for the sentence base on frequency of the word

                    except:
                        continue
                if len(word_tokenize(sentence)) >= 100 and self.shortResult:
                    score -= len(word_tokenize(sentence)) * 65
                sentRank[sentence] = score
        # return the highest score sentences
        sortedSent = sorted(sentRank, key=sentRank.get, reverse=True)
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
                sentences.append(fix_text(sentence))

        print("------------------------------------------------------------------------")
        for result in sentences[0:self.resultAmt]:
            resultWord += len(result)
        if self.totalWord != 0:
            print("Short", resultWord / self.totalWord * 100, "%")
        else:
            print('total word none, scan failed')
            print('')
        print("------------------------------------------------------------------------")
        returnObj['summary'] = sentences[0:self.resultAmt]
        returnObj['wordRank'] = wordRank
        returnObj['sentenceRank'] = sentRank
        print(self.totalWord)
        try:
            if self.totalWord == 0:
                print('failed')
            else:
                returnObj['percentage'] = resultWord / self.totalWord * 100
        except ZeroDivisionError:
            return returnObj
        return returnObj
    def main(self):
        self.paragraph = []
        self.look()
        results =  self.summary()
        results['img'] = self.firstImage()
        return results

#main loop





