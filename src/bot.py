from environment import token, channel
from phrases.help import roster as help_roster

import database
import discord
from discord.ext import commands

db = Database()

client = commands.Bot(command_prefix='!')
client.remove_command('help')

#Setup built-in events
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    alertChannel = client.get_channel(env.channel.alert)

    if message.channel.id == alertChannel.id:
        await alertChannel.send('<@&724642211337207909>')

    await client.process_commands(message)


@client.event
async def on_member_remove(user):
    systemChannel = client.get_channel(env.channel.system)

    db.clearUser(user.id)

    await systemChannel.send('User {0}<@{1}> with ID <{1}> left the discord server.'.format(user.display_name, user.id))


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('This is not a command.')

    if isinstance(error, commands.errors.MissingAnyRole):
        await ctx.send('You do not have access to this command.')


#Define custom checks
def if_roster(ctx):
    rosterChannel = client.get_channel(channel.roster)
    return ctx.message.channel.id == rosterChannel.id


#Setup custom commands
@client.command(pass_context=True)
@commands.check(if_roster)
@commands.has_any_role('Leader', 'Officer', 'Member', 'Provisional')
async def help(ctx):
    embed = discord.Embed(
        title='Roster Commands',
        description=help_roster,
        color=0xeeeeee
    )
    
    await ctx.send(content=None, embed=embed,)


@client.command(name='acronym')
@commands.check(if_roster)
@commands.has_any_role('Leader', 'Officer', 'Member', 'Provisional')
async def acronym(ctx):
    embed = discord.Embed(
        title='Class Acronyms',
        description="""*Hunter* - **HUN**
*Fighter* - **FIG**
*Ranger* - **RAN**
*Gunner* - **GUN**
*Force* - **FOR**
*Techter* - **TEC**
*Braver* - **BRA**
*Bouncer* - **BOU**
*Summoner* - **SUM**""",
        color=0xeeeeee
    )
    
    await ctx.send(content=None, embed=embed,)


@client.command(name='roster')
@commands.check(if_roster)
@commands.has_any_role('Leader', 'Officer', 'Member', 'Provisional')
async def roster(ctx):
    delimeter = "\n"
    desc = '\u200b ' * 155
    
    members = []
    data = db.allPlayers();
    
    i = 1
    for member in data:
        pid = member[0]
        name = str(i)+': '+str(member[1])
        
        chars = []
        subdata = allCharacterBoundPlayer(pid)
        
        if len(subdata):
            content = ""
            
            j = 0
            for char in subdata:
                row = str(char[2])
                chars.append(row)  
                j += 1
        
            content = delimeter.join(chars)
        else:
            content = "-"
        
        field = [name, content]
        members.append(field)
        
        i += 1
    
    embed = discord.Embed(title='Elementum Roster', description=desc, color=0xeeeeee)
    
    i = 0
    for field in members:
        if i == 18:
            try:
                await ctx.send(content=None, embed=embed,)
            except discord.HTTPException as e:
                print(e)
            
            embed = discord.Embed(title='', description=desc, color=0xeeeeee)
            i = 0 
        
        embed.add_field(name=str(field[0]), value=str(field[1]), inline=True)
        i += 1;
    
    if i%3 == 1:
        embed.add_field(name='\u200b', value='\u200b', inline=True)
        i += 1
    
    if i%3 == 2:
        embed.add_field(name='\u200b', value='\u200b', inline=True)
    
    try:
        await ctx.send(content=None, embed=embed,)
    except discord.HTTPException as e:
        print(e)
        

@client.command(name='verify')
@commands.check(if_roster)
@commands.has_any_role('Leader', 'Officer', 'Member', 'Provisional')
async def verify(ctx, *, pid):
    data = db.findUser(ctx.message.author.id)

    if not len(data):
        data = db.findPlayer(pid)
        
        if len(data):
            db.verifyUser(ctx.message.author.id, data[0][0])
            
            await ctx.send('You have succesfully been verified and linked.')
        else:
            await ctx.send('The Player ID Name could not be found.')
    else:
        await ctx.send('You have already been verified with the ID: {d[1]}'.format(d=data[0]))
    
    
@client.command(name='reg')
@commands.check(if_roster)
@commands.has_any_role('Leader', 'Officer', 'Member', 'Provisional')
async def reg(ctx, *, name):
    data = db.findUser(ctx.message.author.id)

    if len(data):
        pid = data[0][0]
        user = data[0][1]
        
        data = db.findCharacter(pid, name)

        if not len(data):
            db.bindCharacter(pid, name)
            
            await ctx.send("A character with the name {0} has now been bound to {1}.".format(name, user))
        else:
            await ctx.send("A character with the name {0} have already been bound to {1}.".format(name, user))
    else:
        await ctx.send('You need to link and verify your discord user with a Player ID Name before you can use this command!')    
    

@client.command(name='unreg')
@commands.check(if_roster)
@commands.has_any_role('Leader', 'Officer', 'Member', 'Provisional')
async def unreg(ctx, *, name):
    data = db.findUser(ctx.message.author.id)

    if len(data):
        pid = data[0][0]
        
        data = db.findCharacter(pid, name)
        
        if len(data):
            cid = data[0][0]
            
            db.unbindCharacter(cid)

            await ctx.send("{0} has been unbound and doesn't exist anymore.".format(name))
        else:
            await ctx.send("That character doesn't exist or doesn't belong to you!")   
    else:
        await ctx.send('You need to link and verify your discord user with a Player ID Name before you can use this command!')    
    
    
@client.command(name='level')
@commands.check(if_roster)
@commands.has_any_role('Leader', 'Officer', 'Member', 'Provisional')
async def level(ctx, name, acr, lv: int):
    data = db.findUser(ctx.message.author.id)

    if len(data):
        pid = data[0][0]
        
        data = db.findCharacter(pid, name)
        
        if len(data):
            cid = data[0][0]
            
            if acr == 'HUN':
                prepared = db.setCharacterHunter
            elif acr == 'FIG':
                prepared = db.setCharacterFighter
            elif acr == 'RAN':
                prepared = db.setCharacterRanger
            elif acr == 'GUN':
                prepared = db.setCharacterGunner
            elif acr == 'FOR':
                prepared = db.setCharacterForce
            elif acr == 'TEC':
                prepared = db.setCharacterTechter
            elif acr == 'BRA':
                prepared = db.setCharacterBraver
            elif acr == 'BOU':
                prepared = db.setCharacterBouncer
            elif acr == 'SUM':
                prepared = db.setCharacterSummoner
            else:
                prepared = False;
            
            if prepared:
                prepared(cid, lv)
                await ctx.send("The class level has been updated for {0}.".format(name))
            else:
                await ctx.send("The class acronym {0} is not valid or hasn't been implemented yet.".format(acr))
        else:
            await ctx.send("That character doesn't exist or doesn't belong to you!")   
    else:
        await ctx.send('You need to link and verify your discord user with a Player ID Name before you can use this command!')    


@client.command(name='levelall')
@commands.check(if_roster)
@commands.has_any_role('Leader', 'Officer', 'Member', 'Provisional')
async def levelall(ctx, name, hun: int, fig: int, ran: int, gun: int, forc: int, tec: int, bra: int, bou: int, summ: int):
    data = db.findUser(ctx.message.author.id)

    if len(data):
        pid = data[0][0]
        
        data = db.findCharacter(pid, name)
        
        if len(data):
            cid = data[0][0]
            
            db.setCharacterLevels(cid, [hun, fig, ran, gun, forc, tec, bra, bou, summ])
                
            await ctx.send("The class levels has been updated for {0}.".format(name))
        else:
            await ctx.send("That character doesn't exist or doesn't belong to you!")   
    else:
        await ctx.send('You need to link and verify your discord user with a Player ID Name before you can use this command!')


@client.command(name='member')
@commands.check(if_roster)
@commands.has_any_role('Leader', 'Officer')
async def member(ctx, date, *, pid):
    data = db.findPlayer(pid)

    if not len(data):
        db.addPlayer(pid, date)
        
        await ctx.send('Player ID Name {0} has succesfully been added.'.format(pid))
    else:
        await ctx.send('Player ID Name {0} already exist and can not be added again.'.format(pid))


@client.command(name='remove')
@commands.check(if_roster)
@commands.has_any_role('Leader', 'Officer')
async def remove(ctx, *, pid):
    data = db.findPlayer(pid)

    if len(data):
        db.deletePlayer(data[0][0], date)
        
        await ctx.send('Player ID Name {0} has succesfully been removed.'.format(pid))
    else:
        await ctx.send('Player ID Name {0} does not exist.'.format(pid))


client.run(env.token)