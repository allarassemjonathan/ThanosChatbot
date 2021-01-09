import youtube_dl
import discord
import os
import smtplib
import email
from email.message import EmailMessage
from discord.ext import commands
from discord.ext.commands import Cog
from discord.utils import get

intents = discord.Intents.default()
intents.members = True

rules = ["rule 0: no bad words here!", "rule 1: no stigmatization here!", "rule 2: no ad-hominem here!", 
		"rule 3: no insult here", "rule 4: all the previous rules are valid and can be subjected to adjustements!"]

insults_words = ["fuck","dick","f***","d***","pussy","p****","I don't give a"]

bad_words = ["you dumb", "you mean", "you a stupid guy", "you are a stupid guy", "you stupid guy"]

Client =  commands.Bot(command_prefix='$')





def email(receiver_email, message):
	sender_email  = 'discordTeamWork@gmail.com'
	password = 'JesusMaimeL666'
	try:
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.stattls()
		server.login(sender_email, password)
		server.sendmail(sender_email, receiver_email, message)
	except:
		print("an error")
	







@Client.event
async def on_ready():
	print("Thannos is ready")
	channel = Client.get_channel(790897408280100908)
	await channel.send("I am online")

	embed = discord.Embed(title=" I'm online!", description="Thannos is now online", colour=0xFF0000)
	fields = [("Name", "Value", True), 
	("Another field", "Another other field", True),
	("A non inline field", "This field is on its own raw", True)]
	for name, value, inline in fields:
		embed.add_field(name=name, value=value, inline=inline)
	await channel.send(embed=embed)
	

@Client.event
async def on_disconnect():
	print("Thannos left")
	await ctx.send("Goodbye friends I'm leaving! I will be back soon")


# $repeat command
@Client.command()
async def repeat(ctx, args):
	await ctx.send(args)

# $clear command
@Client.command()
@commands.has_permissions(manage_messages = True)
async def clear(ctx, number=2):
	number = number + 1
	await ctx.channel.purge(limit=number)

# $kick command
@Client.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, member : discord.Member,*,reason = "No reason provided"):
	await member.send("you have been kicked from the coding community")
	await member.kick(reason=reason)

# $list command
@Client.command()
async def list(ctx):
	members = ctx.guild.chunk(cache=True)
	for member in members:
		await ctx.send(str(member.name))
		
# $totalMembers
@Client.command()
async def totalMembers(ctx):
	n = ctx.guild.member_count
	await ctx.send(str(n))


# $ban command
@Client.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : discord.Member,*,reason = "No reason provided"):
	await member.send("you have been kicked from the coding community")
	await member.ban(reason=reason)

# $hello command
@Client.command()
async def hello(ctx):
	await ctx.send('Hello')

# $server command
@Client.command()
async def server(ctx):
	name = str(ctx.guild.name)
	description = str(ctx.guild.description)
	owner = str(ctx.guild.owner)
	region = str(ctx.guild.region)
	memberCount = str(ctx.guild.member_count)
	id =str(ctx.guild.id)
	icon = str(ctx.guild.icon_url)
	embed = discord.Embed(
		title=name + " Server Information",
		description=description,
		color=discord.Color.blue()
	)
	embed.set_thumbnail(url=icon)
	embed.add_field(name='owner', value=owner, inline=True)
	embed.add_field(name='Server ID', value=id, inline=True)
	embed.add_field(name='Region', value=region, inline=True)
	embed.add_field(name='Member Count', value=memberCount, inline=True)
	await ctx.send(embed=embed)

'''
THE FOLLOWING RULES ARE FOR THE MANAGEMENT OF MUSIC LISTENNING
'''

# $play command
@Client.command()
async def play(ctx, url_:str):
	song_there = os.path.isfile('song.mp3')
	try:
		if song_there:
			os.remove('song.mp3')
	except PermissionError:
		await ctx.send('Wait for the song to finish')
		return

	voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
	await voiceChannel.connect()
	voice = discord.utils.get(Client.voice_clients, guild=ctx.guild)

	ydl_ops = {
		'format':'bestaudio/best',
		'postprocessors':[{
			'key':'FFmpegExtractAudio',
			'preferredcodec':'mp3',
			'preferredquality': '192',
		}],
	}

	with youtube_dl.YoutubeDL(ydl_ops) as ydl:
		ydl.download([url_])
	for file in os.listdir('./'):
		if file.endswith('.mp3'):
			os.rename(file, 'song.mp3')
	voice.play(discord.FFmpegPCMAudio('song.mp3'))

# $leave command
@Client.command()
async def leave(ctx):
	 voice = discord.utils.get(Client.voice_clients, guild=ctx.guild)
	 if voice.is_connected():
	    await voice.disconnect()
	 else:
	    await ctx.send('the voice is already off')

# $pause command
@Client.command()
async def pause(ctx):
	voice = discord.utils.get(Client.voice_clients, guild=ctx.guild)
	if voice.is_playing():
		voice.pause()
	else:
		ctx.send('the voice is already paused')

# $resume command
@Client.command()
async def resume(ctx):
	voice = discord.utils.get(Client.voice_clients, guild=ctx.guild)
	if voice.is_paused():
		voice.resume()
	else:
		await ctx.send('The audio is already playing')

# $stop command
@Client.command()
async def stop(ctx):
	voice = discord.utils.get(Client.voice_clients, guild=ctx.guild)
	voice.stop()

'''
THE FOLLOWING RULES ARE FOR THE MANAGEMENT OF USERS INTERACTIONS
'''

# $rule command
@Client.command()
async def rule(ctx, number):
	embed = discord.Embed(name="rules", 
		description="These rules must be followed by users ⚠️", 
		inline=True,
		color=discord.Color.red())
	index = int(number)
	if index < len(rules):
		embed.add_field(name="Rule " + str(index), value=rules[index], inline=True)
		await ctx.send(embed=embed)
	else:
		embed.add_field(name="A little error...",value="Sorry there is no rule" + str(index), inline=True)
		await ctx.send(embed=embed)

# $allrules command
@Client.command()
async def allrules(ctx):
	embed = discord.Embed(title="RULES OF THE GROUP", 
		description="These rules must be followed for the well being of the group", 
		inline=True,
		color=discord.Color.red())
	for i in rules:
		embed.add_field(name="Rules to follow ⚠️", value=str(i), inline=True)
	await ctx.send(embed=embed)


# $email command
@Client.command()
async def gmail(ctx, email, *messages):
	msg = EmailMessage()
	string =  " "
	print(messages)
	
	for message in messages:
		string = string + " " + message

	print(string)
	msg.set_content(str(string))
	sender_email = 'discordTeamWork@gmail.com'
	msg['Subject'] = 'Test'
	msg['From'] = sender_email
	msg['To'] = str(email)
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	password = 'JesusMaimeL666'
	server.login(sender_email, password)
	server.send_message(msg)
	embed = discord.Embed(title="Notification", description="Email successfully sent to " + str(email), inline=True, color=0xFF0000)
	await ctx.send(embed=embed)



@Client.command()
async def comcast (ctx, email, *messages):
	msg = EmailMessage()
	string =  " "
	print(messages)
	
	for message in messages:
		string = string + " " + message

	print(string)
	msg.set_content(str(string))
	sender_email = 'discordTeamWork@gmail.com'
	msg['Subject'] = 'Test'
	msg['From'] = sender_email
	msg['To'] = str(email)
	server = smtplib.SMTP('smtp.mail.yahoo.com', 465)
	server.startssl()


@Client.command()
async def emailall(ctx, *words):
	sender_email = 'discordTeamWork@gmail.com'
	password = 'JesusMaimeL666'
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	print(words)
	listEmail=[]
	stringMessage = " "

	for email in words:
		if '@' in email:
			listEmail.append(email)
		else:
			stringMessage = stringMessage + " " + email

	print(stringMessage)
	print(listEmail)
	embed = discord.Embed(title="Notification", description="Email(s)  successfully sent", inline=True)
	
	for email in listEmail:
		sender_email = 'discordTeamWork@gmail.com'
		password = 'JesusMaimeL666'
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.starttls()
		server.login(sender_email, password)
		server.sendmail(sender_email, email, stringMessage)
		print(stringMessage)
		embed.add_field(name="notification to " + str(email), value="Email sent to " + str(email), inline=True)
	await ctx.send(embed=embed)


'''	
	msg = EmailMessage()
	msg.set_content(str(message))
	sender_email = 'discordTeamWork@gmail.com'
	msg['Subject'] = 'Test'
	msg['From'] = sender_email
	msg['To'] = str(email)
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	password = 'JesusMaimeL666'
	server.login(sender_email, password)
	server.send_message(msg)
	embed = discord.Embed(title="Notification", description="Email successfully sent to " + str(email), inline=True, color=0xFF0000)
	await ctx.send(embed=embed)


	
	print(string)
	slist = string.split(" ")
	stringEmail =  " "
	stringMessage = " "
	embed = discord.Embed(title="Notification", description="Email(s)  successfully  sent", inline=True)
	print(slist)
	for word in slist:
		if '@' in word:
			stringEmail = word + " " + stringEmail
		else:
			stringMessage = stringMessage + " " + word

	elist = stringEmail.split(" ")
	print(elist)
	for email in elist:
		if '@' in email:
			server = smtplib.SMTP('smtp.gmail.com', 587)
			server.starttls()
			password = 'JesusMaimeL666'
			server.login(sender_email, password)
			server.sendmail(sender_email, str(email), stringMessage)
			embed.add_field(name="Email Notification", value="Email sent to " + str(email), inline=True)
	await ctx.send(embed=embed)

'''
Client.run('')
