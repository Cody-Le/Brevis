<h1 align = "center">Brevis</h1>
<h2 align= "center">"Short" in Latin</h2>


# Introduction to Brevis
A bot look up google search results then give the sentence that would give the best summarize a query. 

Use google api query an amount of wesbite, article
Pass on to an SMMRY like algorithm, to rank the word appears in the website then rank the sentence with the words


# Installation
1. All file are ignorable except the 3 python files within **/TldrBot/TldrBot** folder

2. Run server website
  ```sh
  py httpReq.py
  ```

3. Optional parameter include variable by adding 'r=result receive', 'pgs=page search', 'short = applying an equation to get the shortest answer'

  ```sh
  r = result received
  pgs = pages that will searched from
  short = bool if the result need to also be as short as possible
  ```

4. search **'http://localhost:8080/?q=' + your query** on your chosen browser

