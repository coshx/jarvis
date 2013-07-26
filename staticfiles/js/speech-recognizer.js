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
                console.log("confidence: " + event.results[currentIndex][0].confidence);
                
                $.ajax({
                    type: "GET",
                    url: "process_command/",
                    data: {q: command}
                }).done(function(response) {
                    $("#speech-page-content").val("")
                    if(typeof(response["speak"]) === null && response["speak"].length > 0){
                        speak(response["speak"],{noWorker:true});
                        insertAtCaret(textAreaID, response["speak"]);
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