import re

#Define custom methods
def splitDiscordURL(url):
    reg = re.compile('https[:]//discordapp.com/channels/[0-9]+/[0-9]+/[0-9]+')
    match = reg.fullmatch(url)
    
    if match:
        url = url.lstrip('https[:]//discordapp.com/channels/')
        return url.split('/')
    else:
        return False

def createDiscordURL(guildID, channelID, messageID):
    return 'https://discordapp.com/channels/'+guildID+'/'+channelID+'/'+messageID