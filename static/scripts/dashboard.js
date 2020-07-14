a = "";

function getMetrics(){
    const request = new XMLHttpRequest();
    request.open("GET", "/metrics", true);
    request.send(null);
    a = request.responseText;
    return(request.responseText);
}

