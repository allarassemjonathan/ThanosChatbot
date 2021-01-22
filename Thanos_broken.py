import youtube_dl
import wikipedia
import discord
import os
import smtplib
import email
import random
from email.message import EmailMessage
from discord.ext import commands
from discord.ext.commands import Cog
from discord.utils import get
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
intents = discord.Intents.default()
intents.members = True

''' Important lists and dictionnary'''

rules = ["rule 0: no bad words here!", "rule 1: no stigmatization here!", "rule 2: no ad-hominem here!", 
		"rule 3: no insult here", "rule 4: all the previous rules are valid and can be subjected to adjustements!"]

insults_words = ["fuck","dick","f***","d***","pussy","p****","I don't give a"]

bad_words = ["you dumb", "you mean", "you a stupid guy", "you are a stupid guy", "you stupid guy"]

colors_hex = [0xFF0000, 0xFF7F00, 0xFFFF00, 0x00FF00, 0x0000FF, 0x2E2B5F, 0x8B00FF]

dic_commands = {
	'play': 'Thannos starts a voice call and play music with the command. To play some music type $play urlmusic',
	'allrules': 'Print all the rules of the chat (rules can be subject to modifications). To print the rules type $allrules',
	'ban' : 'Ban a member of the guild. Command available only to the owner. To ban someone type $ban username',
	'clear': 'Clear some message of the chat. Command available only to the owner. To clear type $clear followed by the number of message you want to erase',
	'gmail' : 'Thannos send an email with a message using gmail server. To send an email type $gmail user@gmail.com message',
	'hello': 'Thannos say hello. Type $hello and Thannos will answer you',
	'server' : 'Thannos prints all the information relative to the server. Type $server to access this information',
	'wiki' : 'Thannos will search on Wikipedia a page with the query provided. If Thannos doesnt find one, he will suggest a list of existing pages that may match the query. To search the page of someone type $wiki followed by the  title of thepage',
	'DM' : 'Thannos will send a message with the words message to the user member (providing also the name of the author of the request). To DM type $DM username message',
	'rule' : 'Thannos prints the rule that you are asking to view. To do that type $rule followed by the number of the rule',
	'stop' : 'Thannos stops the music. To do that type $stop after starting the music',
	'leave' : 'Thannos leaves the voice call. To do that type $leave after starting the music',
	'pause' : 'Thannos stops the music. To do that type $pause after starting the music',
	'repeat': 'Thannos repeats what you said after $repeat. To do that type $repeat followed by the word you want the bot to repeat',
	'resume': 'Thannos resumes the music. To do that type $resume',
	'wanted': 'Thannos will make a wanted poster with the photo of the user wanted!'
}




'''Commands'''

Client =  commands.Bot(command_prefix='$')



def rand(arr):
	return random.choice(arr)


@Client.event
async def on_ready():
	print("Thannos is ready")
	channel = Client.get_channel(790897408280100908)
	file = open("commands.txt")
	string = file.read()
	file.close()

	embed = discord.Embed(
		title="Hi guys!",
		description="My name is Thannos, I'm a discord bot built by Jonathan Allarassem. "
			+"I provide simple services like sending emails "
			+ "or reading a wikipedia page.",
		color=rand(colors_hex),
		inline=True)
	embed.add_field(name='Below are some interesting commands! Feel free to test one!', value=string)
	await channel.send(embed=embed)
	

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


@Client.command()
async def DM (ctx, member : discord.Member, *messages):
	string = ''
	for message in messages:
		string = string + ' ' + str(message)
	await member.send(string)

@Client.command()
async def commands(ctx):
	file = open("commands.txt")
	string = file.read()
	file.close()

	embed = discord.Embed(
		title="Commands\nDescription of the bot",
		description="Thanos is a python discord bot built by Jonathan Allarassem "
			+"that interacts with users and provide simple services like sending emails "
			+ "or reading a wikipedia page.",
		color=rand(colors_hex),
		inline=True)
	embed.add_field(name='List of commands', value=string)
	await ctx.send(embed=embed)


@Client.command()
async def infobot(ctx):
	embed = discord.Embed(title='Description', 
		description="Thanos is a python discord bot built by Jonathan Allarassem "
			+"that interacts with users and provide simple services like sending emails "
			+ 'or reading a wikipedia page. See the github repository for more infotmation',
		inline=True, color=rand(colors_hex))
	embed.add_field(name='Github Link', value='https://github.com/allarassemjonathan/ThanosChatbot', 
		inline=True)
	await ctx.send(embed=embed)


# $hello command
@Client.command()
async def hello(ctx):
	await ctx.send('Hello')


@Client.command()
async def Help(ctx, command):
	string = dic_commands[command]
	embed = discord.Embed(title='Help ' + str(command), 
		description='help for the command ' + str(command), 
		inline=True, 
		color=rand(colors_hex))
	embed.add_field(name='$' + command, value=string, inline=True)
	await ctx.send(embed=embed)

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

@Client.command()
async def wanted (ctx, user: discord.Member):

	if user==None:
		user = ctx.author
	
	background = Image.open('wanted_500.png')
	asset = user.avatar_url_as(size = 256)
	data = BytesIO(await asset.read())
	photo = Image.open(data)

	

	background.paste(photo, (120,144))

	background.save('wanted_photo.png')

	await ctx.send(file=discord.File('wanted_photo.png'))


@Client.command()
async def write (ctx, color, *text):
	sentences = ''
	for word in text:
		sentences = sentences + ' ' + word

	background = Image.new('RGB', (500,500), str(color))
	font = ImageFont.truetype('BelieveIt-DvLE.ttf', 24)
	draw = ImageDraw.Draw(background)
	draw.text((166,254), sentences, (0,0,0))

	background.save('text.png')
	await ctx.send(file=discord.File('text.png'))

'''
THE FOLLOWING RULES ARE FOR THE MANAGEMENT OF MUSIC LISTENNING
'''
@Client.command()
async def bible (ctx, version, *passage):
	url_temp = 'https://www.biblegateway.com/passage/?search='
	version_temp = '&version='
	number = ['1','2','3','4','5','6','7','8','9']

	string = ''
	for word in passage:
		string  = string + word

	verse_numb = list(())
	book = ''
	for e in string:
		if e in number:
			verse_numb.append(e)
		else:
			book = book + e

	book = book.capitalize()

	
	cite = ''
	for i in verse_numb:
			cite = cite + i
	url = url_temp + book + cite+ version_temp + version

	embed = discord.Embed(title="Bible citation", 
		description='we want to quote the bible using a simple command',
		color=0xffffff )

	embed.add_field(name=string, value=url, inline=True)

	await ctx.send(embed=embed)









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


# BROKEN CODE!!!
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

# BROKEN CODE!!!
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


@Client.command()
async def wiki (ctx, *query):
	print(query)

	string = ""
	
	for i in query :
		string = string + " " + i

	print(string)

	embed = discord.Embed(title="Query : " + string, 
			description="Information taken from Wikipedia", 
			inline=True, 
			color=rand(colors_hex))
	try:
		page = wikipedia.page(string, auto_suggest=False)
		images = page.images
		picture = images[random.randrange(len(images))]
		print(picture)
		url = page.url
		content = page.content[0:1000] + '[...]'
		embed.set_image(url = picture)
		embed.add_field(name=string, value=content, inline=True)
		embed.add_field(name='Link to the page', value=url, inline=True)
	except:
		topics = wikipedia.search(string)
		result = ''

		for topic in topics:
				result = result  + '🔎 ' + str(topic) + '\n'

		summary = 'Your query is ambigous, see the following options to continue your research. \n' + result
		embed.add_field(name="Error: Ambiguous query", value=summary, inline=True)
		
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
