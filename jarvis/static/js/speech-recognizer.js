(function($) {
	var pop;
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
                console.log("confidence: " + event.results[currentIndex][0].confidence);
                $.ajax({
                    type: "GET",
                    url: "process_command/",
                    data: {q: command},
                    success:function(response) {
                    	$("#speech-page-content").val("");
                    	command = response.command;
                    	data = response.data;
                    	if(command == "speak"){
                    	    speakAndInsert(response.data);
                    	} else if (command == "playerAction") {
                    		if (data instanceof Array) {
                    			if (data[0] == "play") {
                    				var ytubeurl = data[1];
                    				$('#youtube').html("");
                    				pop = Popcorn.youtube('#youtube','http://www.youtube.com/watch?v='+ytubeurl);
                    				pop.play();
                    				pop.pause(); //hackjobby way to prevent memory errors / video skipping
                    				pop.play();
                    			} else if (data[0]=="volume") {
                    				pop.setVolume(data[1])
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
        	$('#speech-page-content').val(text);
        }
    });
})(jQuery);