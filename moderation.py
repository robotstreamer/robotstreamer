import json

#This allows robot control to be moderated.

#Moderation is controlled by a file named with the --moderation-file flag
#on controller.py.
#The moderation file uses either a blacklist or whitelist format.
#The first line of the file should be 'blacklist' or 'whitelist' indicating
#which moderation  scheme to use

#if the whitelist scheme is used then each line after 'whitelist' should be
#a nick that is allowed to control the bot.

#If the whitelist scheme is used then each line should be an IP or the word
#anon. Any IP in the list will not be allowed to control the robot. Anon is a
#special case that blocks all users who are not logged in.


#reads lines from a file and strips off the whitespace at the end
def getFileLines(fileName):
  with open(fileName) as f:
    lineList=f.readlines()
  lineList=[x.strip() for x in lineList]
  return lineList


#controlEvent is parsed javascript and filename is the file with a whitelist or blacklist
def moderateControl(controlEvent, fileName):
  fileLines=getFileLines(fileName)

  if fileLines[0] == 'whitelist':
    whiteNicks=fileLines[1:]

    if 'user' in controlEvent and controlEvent['user'] in whiteNicks:
      if controlEvent['user'] == '':
        return False
      else:
        return True
    else:
      return False

  if fileLines[0] == 'blacklist':
    banList=fileLines[1:]
    if 'ip' in controlEvent and str(controlEvent['ip']) in banList:
      return False
    if 'anon' in banList and 'user' in controlEvent and controlEvent['user'] == '' :
      return False
    return True

  return False
