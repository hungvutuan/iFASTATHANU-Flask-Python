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

function postDevice(){
    const request = new XMLHttpRequest();
    // request.open("POST", "/device/new", true);
    request.open("POST", "/device/new?deviceName=Office sensor&type=Raspberry Pi&locId=2&smokeId=2&gasId=2&tempId=2", true);
    request.send(null);
    // request.onload = function() {
    //     alert(request.responseText);
    // }
    return(request.responseText);
}