from environment import token, channel
from phrases.help import roster as help_roster, guide as help_guide
import functions as method
import database

import discord
from discord.ext import commands

db = database.connection()

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

    alertChannel = client.get_channel(channel.alert)

    if message.channel.id == alertChannel.id:
        await alertChannel.send('<@&724642211337207909>')

    await client.process_commands(message)


@client.event
async def on_member_remove(user):
    systemChannel = client.get_channel(channel.system)

    db.user.clear(user.id)

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

def if_guide(ctx):
    guideChannel = client.get_channel(channel.guide)
    return ctx.message.channel.id == guideChannel.id

def if_debug(ctx):
    debugChannel = client.get_channel(channel.debug)
    return ctx.message.channel.id == debugChannel.id


#Setup custom commands
@client.command(pass_context=True)
@commands.has_any_role('Leader', 'Officer', 'Member', 'Provisional')
async def help(ctx):
    if if_roster(ctx):
        embed = discord.Embed(
            title='Roster Commands',
            description=help_roster,
            color=0xeeeeee
        )
    elif if_guide(ctx): 
        embed = discord.Embed(
            title='Index Commands',
            description=help_guide,
            color=0xeeeeee
        )
        
    await ctx.send(content=None, embed=embed,)


@client.command(name='acronym')
@commands.check(if_roster)
@commands.has_any_role('Leader', 'Officer', 'Member', 'Provisional')
async def acronym(ctx):
    embed = discord.Embed(
        title='Acronyms',
        description="",
        color=0xeeeeee
    )
    
    embed.add_field(name='Class', value='''*Hunter* - **HUN**
*Fighter* - **FIG**
*Ranger* - **RAN**
*Gunner* - **GUN**
*Force* - **FOR**
*Techter* - **TEC**
*Braver* - **BRA**
*Bouncer* - **BOU**
*Summoner* - **SUM**''', inline=False)
    
    embed.add_field(name='Gender and Race', value='''*Male Human* - **MH**
*Female Human* - **FH**
*Male Newman* - **MN**
*Female Newman* - **FN**
*Male CAST* - **MC**
*Female CASR* - **FC**
*Male Deuman* - **MD**
*Female Deuman* - **FD**''', inline=False)
     
    await ctx.send(content=None, embed=embed,)


@client.command(name='roster')
@commands.check(if_roster)
@commands.has_any_role('Leader', 'Officer', 'Member', 'Provisional')
async def roster(ctx):
    delimeter = "\n"
    desc = '\u200b ' * 155
    
    members = []
    data = db.player.catalogue();
    
    i = 1
    for member in data:
        pid = member[0]
        name = str(i)+': '+str(member[1])
        
        chars = []
        subdata = db.character.catalogue(pid)
        
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
    data = db.user.find(ctx.message.author.id)

    if not len(data):
        data = db.player.find(pid)
        
        if len(data):
            db.user.verify(ctx.message.author.id, data[0][0])
            
            await ctx.send('You have succesfully been verified and linked.')
        else:
            await ctx.send('The Player ID Name could not be found.')
    else:
        await ctx.send('You have already been verified with the ID: {d[1]}'.format(d=data[0]))


@client.command(name='reg')
@commands.check(if_roster)
@commands.has_any_role('Leader', 'Officer', 'Member', 'Provisional')
async def reg(ctx, acr, *, name):
    data = db.user.find(ctx.message.author.id)

    if len(data):
        pid = data[0][0]
        user = data[0][1]
        
        if acr == 'MH':
            group = 2
        elif acr == 'FH':
            group = 3
        elif acr == 'MN':
            group = 4
        elif acr == 'FN':
            group = 5
        elif acr == 'MC':
            group = 6
        elif acr == 'FC':
            group = 7
        elif acr == 'MD':
            group = 8
        elif acr == 'FD':
            group = 9
        else:
            group = 0
        
        if group:
            data = db.character.find(pid, name)

            if not len(data):
                db.character.bind(pid, name, group)
                
                await ctx.send("A character with the name {0} has now been bound to {1}.".format(name, user))
            else:
                await ctx.send("A character with the name {0} have already been bound to {1}.".format(name, user))
        else:
            await ctx.send("The race and gender acronym {0} is not valid.".format(acr))
    else:
        await ctx.send('You need to link and verify your discord user with a Player ID Name before you can use this command!')


@client.command(name='unreg')
@commands.check(if_roster)
@commands.has_any_role('Leader', 'Officer', 'Member', 'Provisional')
async def unreg(ctx, *, name):
    data = db.user.find(ctx.message.author.id)

    if len(data):
        pid = data[0][0]
        
        data = db.character.find(pid, name)
        
        if len(data):
            cid = data[0][0]
            
            db.character.unbind(cid)

            await ctx.send("{0} has been unbound and doesn't exist anymore.".format(name))
        else:
            await ctx.send("That character doesn't exist or doesn't belong to you!")   
    else:
        await ctx.send('You need to link and verify your discord user with a Player ID Name before you can use this command!')    
    
    
@client.command(name='setgr')
@commands.check(if_roster)
@commands.has_any_role('Leader', 'Officer', 'Member', 'Provisional')
async def setgr(ctx, acr, *, name):
    data = db.user.find(ctx.message.author.id)

    if len(data):
        pid = data[0][0]
        
        if acr == 'MH':
            group = 2
        elif acr == 'FH':
            group = 3
        elif acr == 'MN':
            group = 4
        elif acr == 'FN':
            group = 5
        elif acr == 'MC':
            group = 6
        elif acr == 'FC':
            group = 7
        elif acr == 'MD':
            group = 8
        elif acr == 'FD':
            group = 9
        else:
            group = 0
        
        if group:
            data = db.character.find(pid, name)

            if len(data):
                cid = data[0][0]

                db.character.update(cid, group)

                await ctx.send("The race and gender has been updated for {0}.".format(name))
            else:
                await ctx.send("That character doesn't exist or doesn't belong to you!")   
        else:
            await ctx.send("The race and gender acronym {0} is not valid.".format(acr))
    else:
        await ctx.send('You need to link and verify your discord user with a Player ID Name before you can use this command!')
        
    
@client.command(name='level')
@commands.check(if_roster)
@commands.has_any_role('Leader', 'Officer', 'Member', 'Provisional')
async def level(ctx, acr, lv: int, *, name):
    data = db.user.find(ctx.message.author.id)

    if len(data):
        pid = data[0][0]
        
        data = db.character.find(pid, name)
        
        if len(data):
            cid = data[0][0]
            
            fault = False
            
            if acr == 'HUN':
                db.character.job.hunter(cid, lv)
            elif acr == 'FIG':
                db.character.job.fighter(cid, lv)
            elif acr == 'RAN':
                db.character.job.ranger(cid, lv)
            elif acr == 'GUN':
                db.character.job.gunner(cid, lv)
            elif acr == 'FOR':
                db.character.job.force(cid, lv)
            elif acr == 'TEC':
                db.character.job.techter(cid, lv)
            elif acr == 'BRA':
                db.character.job.braver(cid, lv)
            elif acr == 'BOU':
                db.character.job.bouncer(cid, lv)
            elif acr == 'SUM':
                db.character.job.summoner(cid, lv)
            else:
                fault = True;
            
            if not fault:
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
async def levelall(ctx, hun: int, fig: int, ran: int, gun: int, forc: int, tec: int, bra: int, bou: int, summ: int, *, name):
    data = db.user.find(ctx.message.author.id)

    if len(data):
        pid = data[0][0]
        
        data = db.character.find(pid, name)
        
        if len(data):
            cid = data[0][0]
            
            db.character.job.update(cid, [hun, fig, ran, gun, forc, tec, bra, bou, summ])
                
            await ctx.send("The class levels has been updated for {0}.".format(name))
        else:
            await ctx.send("That character doesn't exist or doesn't belong to you!")   
    else:
        await ctx.send('You need to link and verify your discord user with a Player ID Name before you can use this command!')


@client.command(name='member')
@commands.check(if_roster)
@commands.has_any_role('Leader', 'Officer')
async def member(ctx, date, *, pid):
    data = db.player.find(pid)

    if not len(data):
        db.player.add(pid, date)
        
        await ctx.send('Player ID Name {0} has succesfully been added.'.format(pid))
    else:
        await ctx.send('Player ID Name {0} already exist and can not be added again.'.format(pid))


@client.command(name='remove')
@commands.check(if_roster)
@commands.has_any_role('Leader', 'Officer')
async def remove(ctx, *, pid):
    data = db.player.find(pid)

    if len(data):
        db.player.delete(data[0][0])
        
        await ctx.send('Player ID Name {0} has succesfully been removed.'.format(pid))
    else:
        await ctx.send('Player ID Name {0} does not exist.'.format(pid))
        
        
@client.command(name='active')
@commands.check(if_roster)
@commands.has_any_role('Leader', 'Officer', 'Member', 'Provisional')
async def active(ctx):
    data = db.user.find(ctx.message.author.id)

    if len(data):
        time = method.getTimestamp()
        db.user.active(data[0][0], time)
        
        date = method.timestampToUTC(time)
        await ctx.send('You have been updated as active at {0}.'.format(date))
    else:
       await ctx.send('You need to link and verify your discord user with a Player ID Name before you can use this command!')
        
        
@client.command(name='activate')
@commands.check(if_roster)
@commands.has_any_role('Leader', 'Officer')
async def activate(ctx, *, pid):
    data = db.player.find(pid)

    if len(data):
        time = method.getTimestamp()
        db.user.active(data[0][0], time)
        
        date = method.timestampToUTC(time)
        await ctx.send('Player ID Name {0} has been updated as active at {1}.'.format(pid,date))
    else:
        await ctx.send('Player ID Name {0} does not exist.'.format(pid))


@client.command(name='createIndex')
@commands.check(if_guide)
@commands.has_any_role('Leader', 'Officer')
async def createIndex(ctx):
    await ctx.message.delete()
    
    embed = discord.Embed(
        title='Index',
        description="",
        color=0xeeeeee
    )

    message = await ctx.send(content=None, embed=embed,)
    
    db.index.update(message.id)


@client.command(name='clearIndex')
@commands.check(if_guide)
@commands.has_any_role('Leader', 'Officer')
async def clearIndex(ctx):
    await ctx.message.delete()

    db.index.clear()
    

client.run(token)