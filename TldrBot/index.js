var reqObject = null


function search(){
	var pages = document.getElementById('pages').value;
	var short = document.getElementById('short').checked;
	var rs = document.getElementById('results').value;
    var query = document.getElementById('queryBox').value;

    console.log(query)
    
    if(query[0] == '$'){
    	if (query.toLowerCase() == '$statistic' && reqObject != null){
    		i = 0
    		document.getElementById('output').innerHTML = '<table><tr><th>word</th><th>frequency</th></tr>'
    		console.log(reqObject.wordRank)
    		for (var word in reqObject.wordRank){
    			console.log(word)
    			if (i < 25){
    				i++
    				document.getElementById('output').innerHTML += '<tr><td>'+ word +'</td><td>'+ reqObject.wordRank[word] +'</td></tr>'
    			}

    		}
    		document.getElementById('output').innerHTML += '</table>' 
    	}else{
    		document.getElementById('output').innerHTML += "You either didn't query anything OR command is not available"
    	}
    }else{
    	document.getElementById('header').innerHTML = 'Query: ' + query + ', proccessing '+ pages + ' pages...'
    	console.log('Requesting query ' + query)
    	url = 'http://127.0.0.1:5000/main?q=' + query + '&pgs=' + pages + '&r' + results
    	if (short){
    		url += '&short'
    	}
    	fetch(url)
	    .then(response=>response.json()).then(data=>{
	    	
	    	reqObject = data
	    	console.log(reqObject)
	    	var summary = ''
	    	for (var summa in data.summary){
	    		summary += '&nbsp;&nbsp;&nbsp;&nbsp;[' + summa + ']' + data.summary[summa] + '<br>'
	    	}

	    	
	    	document.getElementById('header').innerHTML = 'Query: ' + query + ', minimize to ' + data.percentage + '%'
	    	document.getElementById('output').innerHTML = summary
	    	document.getElementById('firstIMG').src = data.img
	    	if(data.abstract){
	    		console.log(data.abstract)
	    		document.getElementById('abstractOutput').innerHTML = data.abstract
	    	}
	    	document.getElementById('navigation').style.display = "block"
	    	document.getElementById('input').style.display = 'none'

	    })
	    .catch(error=>{
	    	console.log(error)
	    })
    }

}

function statistic(){
	console.log('reqOBJ', reqObject)
	document.getElementById('output').style.display = 'none'
	document.getElementById('outputStatistic').style.display = 'block'
	for (var word in reqObject.sortedWordRank.slice(0,25)){
		document.getElementById('outputTable').innerHTML += '<tr><td>' + reqObject.sortedWordRank[word] + '</td><td>' + reqObject.wordRank[reqObject.sortedWordRank[word]]+'</td>'+'</tr>'
	}
	for (var link in reqObject.links){
		document.getElementById('citation').innerHTML += '<a href=' + link + '>' + reqObject[link] + '</a><br>'
	}
}

function summaryShow(){
   	document.getElementById('output').style.display = 'block'
   	document.getElementById('outputStatistic').style.display = 'none'
}

function inputShow(){
	document.getElementById('input').style.display = 'block'
}