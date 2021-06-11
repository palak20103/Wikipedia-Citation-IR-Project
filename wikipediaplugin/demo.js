function gotback(result){
  console.log(result);
  result = JSON.parse(result);
  console.log(result['res']);
  document.getElementById("resultfromFlask").setAttribute("style", "visibility: visible;");
  if (result['demo'] === "not done"){
    document.getElementById('relevance').innerHTML = "Error";

  }
  else
    document.getElementById('relevance').innerHTML = result['res'];


}



function sendData(url, query) {

  var Titlesplit = url.split('en.wikipedia.org/wiki/')[1];
  if (Titlesplit.split('#').length > 1)
    Titlesplit = Titlesplit.split('#')[0];

  document.getElementById("Title").innerHTML = '<h3>Wikipedia Current Page Title :</h3> ' + Titlesplit;
  document.getElementById("Query").innerHTML = '<h4>Selected Query: </h4> '+ query;


  var myHeaders = new Headers();
  myHeaders.append("Content-Type", "application/json");

  var sending = JSON.stringify({
    "page": Titlesplit,
    "query": query
  });

  var requestOptions = {
    method: 'POST',
    headers: myHeaders,
    body: sending,
    redirect: 'follow'
  };

  fetch("http://127.0.0.1:5000/test", requestOptions)
    .then(response => response.text())
    .then(result => gotback(result))
    .catch(error => console.log('error', error));

}


result.onclick = function (element){

  chrome.tabs.query({
    active: true,
    lastFocusedWindow: true
  }, function (tabs) {
    chrome.tabs.executeScript({
      code: "window.getSelection().toString();"
    },
      function (selection) {
        var query = selection[0];
        chrome.tabs.executeScript(tabs[0].id, {
          code: sendData(tabs[0].url, query)
        });
      }
    );
  });
};