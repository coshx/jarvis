var pop;
(function($) {
    $(document).ready(function() {
        try {
            var recognition = new webkitSpeechRecognition();
        } catch(e) {
            var recognition = Object;
        }
        recognition.continuous = true;
        recognition.interimResults = false;
        recognition.lang = "en";

        var interimResult = '';
        var textArea = $('#speech-page-content');
        var textAreaID = 'speech-page-content';

        recognition.start();

        recognition.onresult = function (event) {
            console.log(event);
            var currentIndex = event.results.length - 1;
            if(event.results[currentIndex].isFinal){
                var command = event.results[currentIndex][0].transcript;
                console.log(command);
                //$('#speech-input-content').text(command);
                document.getElementById('speech-input-content').innerHTML += command.trim() + "\n";
                console.log("confidence: " + event.results[currentIndex][0].confidence);
                $.ajax({
                    type: "GET",
                    url: "process_command/",
                    data: {q: command},
                    success:function(response) {
                    	$("#speech-page-content").val("");
                    	command = response.command;
                    	data = response.data;
                    	if(command == "speak") {
                    		if (data == "time") {
                    			processTimeCommand();
                    		} else {
                    	    	speakAndInsert(data);
                    	   	}
                    	} else if (command == "playerAction") {
                    		if (data instanceof Array) {
                    			if (data[0] == "play") {
                    				var ytubeurl = data[1];
                    				$('#youtube').html("");
                    				insertToTextarea("Now playing.");
                    				pop = Popcorn.youtube('#youtube','http://www.youtube.com/watch?v='+ytubeurl);
                    				pop.play();
                    				pop.pause(); //hackjobby way to prevent memory errors / video skipping
                    				pop.play();
                    				console.log(pop);
                    			} else if (data[0]=="volume") {
                    				console.log(data[1]);
                    				pop.options.youtubeObject = pop.options.youtubeObject.setVolume(data[1]);
                    			}
                    		} else if (data == "pause") {
                    			pop.pause();
                    			pop.play(); //hackjobby way to prevent memory errors / video skipping
                    			pop.pause();
                    		} else if (data == "resume") {
                    			pop.play();
                    			pop.pause(); //hackjobby way to prevent memory errors / video skipping
                    			pop.play();
                    		}
                    	}
                    },
                    error:function(data) {
                    	console.log("Error: " + data);
                    }
                });
            }
        };

        recognition.onend = function() {
            console.log("BAD- the recognition ended");
            recognition.start(); //lets just start it again...NEVER...STOP...LISTENING
        };
        
        function speakAndInsert(text) {
        	speak(text,{noWorker:true});
        	insertToTextarea(text);
        }
        
        function insertToTextarea(text) {
        	document.getElementById('speech-page-content').innerHTML += text.trim() + "\n";
        }
        
        function processTimeCommand() {
        	var today = new Date();
        	var h = today.getHours();
        	var m = today.getMinutes();
        	var pm = false;
        	var h_s,m_s;
        	if (h > 12) {
        		pm = true;
        		h = h%12;
        	}
        	h_s=h;
        	m_s=m;
        	if (h<10) h_s = "0"+h;
        	if (m<10) m_s = "0"+m;
        	var timeString = (pm)? h_s+":"+m_s+" pm" : h_s+":"+m_s+" am";
        	insertToTextarea("The current time is: " +timeString);
        	if (m<10) m_s = "oh "+m;
        	timeString = (pm)? h_s+" "+m_s+" p.m." : h_s+" "+m_s+" a.m.";
        	speak("The current time is: "+timeString);
        }
    });
})(jQuery);