from django.db import models
import nltk

class CommandProcessor(models.Model):
  
  @staticmethod
  def extractCommand(command):
    # Jarvis/Travis what is the weather
    if not CommandProcessor.isCommand(command):
      return False
    command = command.split(' ',1)[1] #removes jarvis from the command
    
    entities = CommandProcessor.entities(command)
    for entity in entities:
      if entity[0] == "weather":
        return "weather"

    return "unknown"
  
  @staticmethod
  def isCommand(command):
    if command.split(" ")[0].lower() == "travis" or command.split(" ")[0].lower() == "jarvis":
      return True
    else:
      return False

  @staticmethod
  def entities(command):
    tokens = nltk.word_tokenize(command)
    tagged = nltk.pos_tag(tokens)
    return nltk.chunk.ne_chunk(tagged)
    

