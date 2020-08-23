function search(){
    console.log('banana')
    var query = document.getElementById('query').value;
    var pages = document.getElementById('pages').value;
    var results = document.getElementById('results').value;
    window.location.href = 'http://localhost:8080/'+query;
}