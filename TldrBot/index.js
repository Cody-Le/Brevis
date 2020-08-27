function search(){
    var query = document.getElementById('queryBox').value;
    console.log(query)
    fetch('http://127.0.0.1:5000/main?q=' + query)
    .then(response=>response.json()).then(data=>{
    	console.log(data.summary)
    	var summary = ''
    	for (var summa in data.summary){
    		summary += '[' + summa + ']' + data.summary[summa]
    	}

    	document.getElementById('output').innerHTML = summary

    })
    .catch(error=>{
    	console.log(error)
    })
    
}