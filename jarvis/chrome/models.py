from django.db import models
import urllib
# import nltk

class CommandProcessor(models.Model):
  
  @staticmethod
  def extractCommand(command):
    # Jarvis/Travis what is the weather
    if not CommandProcessor.isCommand(command):
      return False
    command = command.split(' ',1)[1] #removes jarvis from the command
    
    # entities = CommandProcessor.entities(command)
    entities = command.split(' ')
    
    #check for music
    if entities[0] == "play" and len(entities) > 1:
      entities.pop(0) #remove play
      return {'command': 'play', 'data': urllib.quote(' '.join(entities))}

    if entities[0] in ["pause", "paws", "popeyes", "Paz", "pies", "pa"]:
      return {'command': 'pause'}

    if entities[0] in ["resume", "play"]:
      return {'command': 'resume'}

    #check for weather
    for entity in entities:
      print entity
      if entity == "weather":
        return {"command": "weather"}

    return {"command": "unknown"}
  
  @staticmethod
  def isCommand(command):
    if command.split(" ")[0].lower() in ["travis", "jarvis", "jaris", "javis"]:
      return True
    else:
      return False

  # @staticmethod
  # def entities(command):
  #   tokens = nltk.word_tokenize(command)
  #   tagged = nltk.pos_tag(tokens)
  #   return nltk.chunk.ne_chunk(tagged)