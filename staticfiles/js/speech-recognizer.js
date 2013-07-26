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
                    	if(typeof(response.speak) !== 'undefined'){
                    	    speak(response.speak,{noWorker:true});
                    	    insertAtCaret(textAreaID, response["speak"]);
                    	} else if (typeof(response.action) !== 'undefined') {
                    		if (response.action == "youtube" && response.data !== "") {
                    			var ytubeurl = response.data;
                    			pop = Popcorn.youtube('#youtube','http://www.youtube.com/watch?v='+ytubeurl);
                    			pop.play();
                    		} else if (response.action == "pause") {
                    			pop.pause();
                    		} else if (response.action == "resume") {
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
    });
})(jQuery);