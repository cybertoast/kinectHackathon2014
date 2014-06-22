setupWebsocket = function() {
	var ws;
    if ("WebSocket" in window) {
        ws = new WebSocket("ws://localhost:5000/websocket");
    } else {
        ws = new MozWebSocket("ws://localhost:5000/websocket");
    }

    ws.onmessage = function( event ) {
        var data = JSON.parse(event.data);
        // var addr = data.addr;
        // var value = data.value;
        var skelid = data.skelid;
        var jointname = data.jointname;
        var handstate = data.handstate;
        var coords = data.coords;
        
        console.log(skelid, jointname, coords, data);
        
        var s = "";
        var olds = document.getElementById("msg").innerHTML.split("\n");
        for(var i=olds.length-20; i<olds.length; i++) {
           	if(i>=0) s += olds[i] + "\n";  
        }
        
        s += "<p>" + skelid + " : " + jointname + " : ";
        for(var i=0; i<coords.length; i++) {
        	s += "[" + i + ": " + coords[i] + "] ";
        }
        s += "</p>\n";
        document.getElementById("msg").innerHTML = s;
    }

    ws.onopen = function( event ) {
    }
}

setupWebsocket();
