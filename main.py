import discord
from discord.ext import commands
# from discord_slash import SlashCommand
import os
import requests
import json
from tabulate import tabulate
from replit import db
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email_validator import validate_email
from keep_alive import keep_alive
api_url = 'https://api.api-ninjas.com/v1/quotes?category=happiness'
api_base_url = 'https://api.api-ninjas.com/v1/nutrition?query='

# server = ctx.message.server

def get_quote():
    response = requests.get(api_url, headers={'X-Api-Key': 'os.environ['api']'})
    json_data = json.loads(response.text)
    quote = json_data[0]["quote"] + " - " + json_data[0]["author"]
    return quote

def get_nutrition(query):
    api_url2 = api_base_url + query
    response = requests.get(api_url2, headers={'X-Api-Key': 'os.environ['nutritionAPI']'})
    json_data = json.loads(response.text)
    try:
        calories = str(json_data[0]["calories"]) + " - CALORIES"
        protein = str(json_data[0]["protein_g"]) + " - PROTEIN (g)"
        sodium = str(json_data[0]["sodium_mg"]) + " - SODIUM (mg)"
        potassium = str(json_data[0]["potassium_mg"]) + " - POTASSIUM (mg)"
        carbohydrates = str(json_data[0]["carbohydrates_total_g"]) + " - CARBOHYDRATES TOTAL (g)"
        nutrition = f"{calories}\n{protein}\n{sodium}\n{potassium}\n{carbohydrates}"
        return nutrition
    except (KeyError, IndexError):
        return "Nutrition information not found."

embed = discord.Embed(
    title="Quote List Categories",
    description="> Categories\n```\nage\namazing\nanger\narchitecture\nart\nattitude\nbeauty\nbest\nbirthday\ncar\ncommunications\ncomputers\ncool\ncourage\ndating\ndesign\ndreams\nexperience\nfailure\nfamous\nfitness\nfood\nfriendship\nfunny\nfuture\ngraduation\ngreat\nhealth\nhome\nhope\nhumor\nimagination\ninspire\nintelligence\nknowledge\nleadership\nlearning\nlife\nlove\nmoney\nmorning\nmovies\nsuccess\n\n```",
    colour=0x00b0f4
)
embed.set_author(name="Yuri")
embed2 = discord.Embed(title="Help Commands",
                      url="https://example.com",
                      description="> Ping Command\n```\nqalive - reacts\nqping - replies\n```\n> Quotes\n```\nqquotescategories -  quotes genre\nqinspire - random words of wisdom\n```\n> for Fitness Addicts\n```\nqnutrition (anyDish/ anyFruit/ anything)\nqnutrition egg\n```",
                      colour=0x6ef500)

embed2.set_author(name="Yuri ---- Help")

embed2.set_footer(text="by MihirA",
                 icon_url="https://slate.dan.onl/slate.png")

# --------------------------------------------bad words list tl;dr-------------------------
bad_words = os.environ['badwords']
# ----------------------------------end of list -------------------------------

async def send_email(receiver, subject, body):
    sender_email = "mihiramin2004@gmail.com"
    password = os.environ['GMAIL']  # Replace with your email password
    message = f"Subject: {subject}\n\n{body}"

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver, message)
        print("Email sent successfully!")
    except smtplib.SMTPException as e:
        print(f"Error sending email: {e}")





class MyClient(commands.Bot):
    async def on_ready(self):
        print('Logged on as', self.user)
        user = await self.fetch_user(722859224169709658)
        await client.change_presence(status=discord.Status.idle, activity=discord.Activity(type = discord.ActivityType.listening, name='you talk'))
        await user.send("Hello there. I'm online as of now!")

    async def on_message(self, message):
        if message.author == self.user:
            return

        await self.process_commands(message)  # Add this line to process commands

        if message.content == 'qping':
            await message.channel.send('pong')

        if message.content == 'qhello':
            await message.channel.send('Heya!')

        if message.content == 'qinspire':
            quote = get_quote()
            await message.channel.send(quote)

        if message.content == 'qquotescategories':
            await message.channel.send(embed=embed)

        if message.content.startswith('qnutrition '):
            query = message.content.split(' ', 1)[1]
            nutrition = get_nutrition(query)
            await message.channel.send(nutrition)

        if message.content == 'qhelpme':
            await message.channel.send(embed=embed2)

        msg = message.content

        # if any(word in msg for word in bad_words):
        #     await message.delete()
        #     await message.channel.send('Don\'t send that message again or actions would be taken!')

        alive = '\N{THUMBS UP SIGN}'
        if message.content == 'qalive':
            await message.add_reaction(alive)

          

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = MyClient(command_prefix='q', intents=intents)

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member):
    await member.kick(reason=None)
    await ctx.send(f'User {member} has been kicked')



embed2 = discord.Embed(title="Help Commands",
                      url="https://example.com",
                      description="> Ping Command\n```\nqalive - reacts\nqping - replies\n```\n> Quotes\n```\nqquotescategories -  quotes genre\nqinspire - random words of wisdom\n```\n> for Fitness Addicts\n```\nqnutrition (anyDish/ anyFruit/ anything)\nqnutrition egg\n```",
                      colour=0x6ef500)

embed2.set_author(name="Yuri ---- Help")

embed2.set_footer(text="by MihirA",
                 icon_url="https://slate.dan.onl/slate.png")




@client.command(name="mail")
async def qmail(ctx, receiver, subject, *, body):
    await ctx.send(f"Sending an email to {receiver}...")

    # Check if the receiver email is valid
    if not validate_email(receiver):
        await ctx.send("Invalid email address!")
        return

    await send_email(receiver, subject, body)
    await ctx.send("Email sent!")



keep_alive()
client.run(os.environ['TOKEN'])
