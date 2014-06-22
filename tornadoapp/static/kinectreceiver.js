setupWebsocket = function() {
	console.log("Setting up websocket");			
	var ws;
    if ("WebSocket" in window) {
        ws = new WebSocket("ws://localhost:5000/websocket");
    } else {
        ws = new MozWebSocket("ws://localhost:5000/websocket");
    }

	var triggerable = true;
	
	var handtipleft = 0;
	var headY = 1000000;

    ws.onmessage = function( event ) {
        var data = JSON.parse(event.data);
        // var addr = data.addr;
        // var value = data.value;
        var skelid = data.skelid;
        var jointname = data.jointname;
        var handstate = data.handstate;
        var coords = data.coords;
        
		
		if (jointname == "head") {
			headY = data.coords[1];
		}
		
		
		if (jointname == "handtipleft") {
			handtipleft = data.coords[1];	
		}
		
		
		if ((jointname == "head") || (jointname == "handtipleft")) {
			console.log("handtipleft\t" + handtipleft + "\theadY\t" + headY);
		}
		
		
		
		if ((triggerable) && (handtipleft > headY)) {
			triggerable = false;
			// Trigger something
			console.log("triggering");
			trigger('0,2');
			setTimeout(function (){
				triggerable = true;
			}, 1000);
		}

        //console.log(skelid, jointname, coords, data);
        

    }

    ws.onopen = function( event ) {
        console.log("Websocket Connection opened");		
    }
}

setupWebsocket();
