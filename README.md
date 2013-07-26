JARVIS
===
Stands for Just A Really Very Intelligent System.
Uses webkit speech interpretation and natural language processing to execute voice commands.

Jarvis only responds to commands prefaced with "jarvis".
Currently implemenented commands:
---
-weather
gives the temperature and weather state.
-temperature
gives the current temperature, with a high and low for today.
-wind
gives the current wind speed, with a direction heading
-play (parameters)
searches youtube using the parameters you've given it and plays the first video returned from the search
-pause
if there's a video playing, this command pauses it.
-resume
if there's a video that's been paused, this command resumes it.
-ask (question)
returns what Wolfram|Alpha returns for your question.

All of these commands have aliases and natural language processing is built in, so you can say "jarvis, what is the weather like?" or "jarvis, how's the weather", and on and on.

Runs on Django and requires the wolframalpha module.
