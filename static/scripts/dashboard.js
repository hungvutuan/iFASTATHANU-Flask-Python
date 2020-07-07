function getMetrics(){
    const request = new XMLHttpRequest();
    request.open("GET", "/live", true);
    request.send(null);
    return request.responseText;
}