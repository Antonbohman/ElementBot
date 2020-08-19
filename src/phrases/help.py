#Help text for roster channel
roster = """**!roster**
- Prints a minimal roster list with current members
A more comprehensive roster can be found on [webpage](http://elementum.voidcorner.com/roster.php)

**!verify <Player ID Name>**
- Links your discord user with game ID

**!active**
- Updates your last active status to current time

**!reg <Race and gender acronym> <Character Name>**
- Create and binds character name to your game ID

**!unreg <Character Name>**
- Unbinds and removes character name from your game ID

**!setgr <Race and Gender Acronym> <Character Name>**
- Updates bound character with new race and gender acronym

**!level <Class Acronym> <Level> <Character Name>**
- Updates selected class level for selected character

**!levelall <Hunter Level> <Fighter Level> <Ranger Level>
<Gunner Level> <Force Level> <Techter Level> <Braver Level> 
<Bouncer Level> <Summoner Level> <Character Name>** 
- Updates all levels for selected character

**!acronym <Player ID Name>**
- Show a list with acronyms for classes, race and genders

__**Admin Commands**__
**!member <Date Joined> <Player ID Name>**
- Adds a new Player ID Name to the roster 
Date should be formated as *YYYY-MM-DD*
  
**!remove <Player ID Name>**
- Removes Player ID Name from the roster

**!activate <Player ID Name>**
- Updates last active status for player to current time"""



#Help text for guide channel
guide = """Helptext for indexing the guide.

Target ID should always be the whole URL string, in this format:
https://discordapp.com/channels/guildID/channelID/messageID


__**Index Controls**__
**!createIndexTarget**
- Create a new blank target message for indexing     

**!setIndexTitle <Title>**
- Sets a new title to be used for the Index print.

**!setIndexTarget <Message Target ID>**
- Binds existing message as target for indexing, must be a message created by the bot

**!updateIndex**
- Updates current target index message with current values from database
Creates and prints the index with normal settings

**!updateIndexDebug**
- Updates current target index message with current values from database
Creates and prints the index with debug settings, showing extra info

**!clearIndex**
- Removes index target and all categories and subjects saved in database


__**Category Controls**__
**!createCategory <Title>**
- Create a new category for the index

**!updateCatTitle <Category ID> <Title>**
- Renames title for selected category

**!updateCatOrder <Category ID> <Weight>**
- Updates category weight, which defines order of categories in index *(low to high)*

**!removeCategory <Category ID>**
- Removes selected category and it's sub titles


__**Subject Controls**__
**!createSubject <Title>**
- Create a new subject for the index, placed uncategorised at creation

**!updateSubCat <Subject ID> <Category ID>**
- Moves the subject under selected Category

**!updateSubCat <Subject ID> <Title>**
- Renames title for selected subject

**!updateSubTarget <Subject ID> <Message Target ID>**
- Updates target message subject should link to

**!updateSubOrder <Subject ID> <Weight>**
- Updates subject weight, which defines order of subjects in index *(low to high)*

**!removeCategory <Category ID>**
- Removes selected subject"""