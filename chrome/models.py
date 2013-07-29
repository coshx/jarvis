from django.db import models
import urllib, wolframalpha
# import nltk

class CommandProcessor(models.Model):
  @staticmethod
  def humanify(result):
      result = result.split("\/")
      if len(result) == 1:
          return result[0]
      else:
          newResult = ""
          for i,r in enumerate(result):
              if i % 2 == 0:
                  newResult += r + " "
              elif r.isdigit():
                  newResult += "over " + r + " "
              else:
                  newResult += "per " + r + " "
      return newResult
  
  @staticmethod
  def processWolframAlphaResult(result):
    query_string = ""
    for idx,rs in enumerate(result.results):
        if idx == 2:
            break
        
        query_string += CommandProcessor.humanify(rs.result)
        if idx == 0:
            query_string += " is "
    return query_string
  
  @staticmethod
  def extractCommand(command):
    if not CommandProcessor.isCommand(command):
      return False
    command = command.split(' ',1)[1] #removes jarvis from the command
    
    # entities = CommandProcessor.entities(command)
    entities = command.split(' ')
    
    #check for weather
    for entity in entities:
      if entity == "weather":
        return {"command": "weather"}
      if entity == "temp" or entity == "temperature":
          return {"command":"temperature"}
      if entity == "wind":
          return {"command":"wind"}
      if entity == "time":
          return {'command':'time'}
      if entity == "volume":
          return {'command':'volume','data':' '.join(entities)}
    
    #check for music
    if entities[0] == "play" and len(entities) > 1:
      entities.pop(0) #remove play
      return {'command': 'play', 'data': urllib.quote(' '.join(entities))}
  
    #check for pause command
    if entities[0] in ["pause", "paws", "popeyes", "Paz", "pies", "pa"]:
      return {'command': 'pause'}

    #check for resume command
    if entities[0] in ["resume", "play", "repeat"]:
      return {'command': 'resume'}
  
    #check for wolfram alpha question
    if entities[0] in ["what", "ask", "what's"]:
        entities.pop(0)
        question = " ".join(entities)
        query = wolframalpha.WolframAlpha(question)
        query_string = CommandProcessor.processWolframAlphaResult(query)
        return {'command':'ask', 'data': query_string }

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