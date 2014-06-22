setupWebsocket = function() {
	console.log("Setting up websocket");			
	var ws;
    if ("WebSocket" in window) {
        ws = new WebSocket("ws://localhost:5000/websocket");
    } else {
        ws = new MozWebSocket("ws://localhost:5000/websocket");
    }


	var rightHandY = 
	var headY = 

    ws.onmessage = function( event ) {
        var data = JSON.parse(event.data);
		
		if (data.address) {
		console.log("Address: " + data.address);
		}
		
        // var addr = data.addr;
        // var value = data.value;
        var skelid = data.skelid;
        var jointname = data.jointname;
        var handstate = data.handstate;
        var coords = data.coords;
        
		
		if (jointname == "head") {
			headY = data.coords.y;
		}
		
		if (jointname == "handright") {
			rightHandY = data.coords.y;
		}
		
		if (rightHandY > headY) {
			// Trigger something
			console.log("triggering");
			trigger('0,2');
		}

        //console.log(skelid, jointname, coords, data);
        

    }

    ws.onopen = function( event ) {
        console.log("Websocket Connection opened");		
    }
}

setupWebsocket();
