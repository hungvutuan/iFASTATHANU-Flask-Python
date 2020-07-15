function getMetrics(){
    const request = new XMLHttpRequest();
    request.open("GET", "/metrics", true);
    request.send(null);
    // request.onload = function() {
    //     alert(request.responseText);
    // }
    return(request.responseText);
}

function getHistory(){
    const request = new XMLHttpRequest();
    request.open("GET", "/history", true);
    request.send(null);
    // request.onload = function() {
    //     alert(request.responseText);
    // }
    return(request.responseText);
}
