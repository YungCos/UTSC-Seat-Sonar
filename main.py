import discord
import os
import firebase_admin
from firebase_admin import db
from discord.ext import commands
from discord.ext import tasks
import ttb

intents = discord.Intents.default()

bot = commands.Bot(command_prefix="!", help_command=None, intents=intents)

cred_obj = firebase_admin.credentials.Certificate(os.getenv("CRED_OBJ"))
default_app = firebase_admin.initialize_app(cred_obj, {
    'databaseURL': os.getenv("DB_URL")
    })


@tasks.loop(minutes = 15)
async def notify():
    users = db.reference(f"/Users").get()

    for user in users:

        userObj = await bot.fetch_user(user)

        if not userObj:
            print(user, "not found")
            continue

        for course in users[user]['Tutorials']:

            tuts = []

            for tut in users[user]['Tutorials'][course]:

                tuts.append(tut)

            available_tuts = ttb.findCourse(course, tuts)

            for i in available_tuts:

                await userObj.send(f"<@{user}> {i} for {course} has been made available. Act Quick!")
                db.reference(f"/Users/{user}/Tutorials/{course}").update({i: None})


@bot.event
async def on_ready():
    print("Bot is ready!")

    await bot.change_presence(status=discord.Status.online, activity=discord.Game("Sniping Tutorials"))
    await notify.start()


@bot.command()
async def help(ctx):
    embed=discord.Embed(title="Commands", color=0x009dff)
    embed.add_field(name="!watch [Course Code] [Tutorial Name]", value="Adds a tutorial to be watched. Note that the tutorial name needs to be exact (Ex. !watch CSCB36 TUT0001)", inline=True)
    embed.add_field(name="!courses", value="View the tutorials that you are currently watching", inline=True)
    embed.add_field(name="!remove [Course Code] [Tutorial Name]", value="Removes a tutorial from the watchlist. Note the format is the same as !watch", inline=True)
    embed.add_field(name="!removeall [Course Code](optional)", value="Removes all tutorial from the given course. If no course is given, than it will remove all tutorials from all courses", inline=True)
    await ctx.reply(embed=embed)


@bot.command()
async def watch(ctx, course, tut):

    course = course.upper()
    tut = tut.upper()

    db.reference(f"/Users/{ctx.author.id}/Tutorials/{course}").update({tut: 0})
    await ctx.reply(f"You are now watching {tut} for {course}")

@bot.command()
async def courses(ctx):

    userData = db.reference(f"/Users/{ctx.author.id}/Tutorials").get()
    embed=discord.Embed(title="Tutorials Being Watched", color=0x009dff)

    for i in userData:

        course_name = i
        tuts = []

        for j in userData[i]:

            tuts.append(j)

        embed.add_field(name=course_name, value="\n".join(tuts), inline=True)

    await ctx.reply(embed=embed)

@bot.command()
async def removeall(ctx, course = None):
    if course:

        course = course.upper()

        db.reference(f"/Users/{ctx.author.id}/Tutorials/").update({course: None})
        await ctx.reply(f"You are no longer watching any tutorials for {course}")
    else:
        db.reference(f"/Users").update({ctx.author.id: None})
        await ctx.reply(f"You are no longer watching any tutorials")


@bot.command()
async def remove(ctx, course, tut):

    course = course.upper()
    tut = tut.upper()

    db.reference(f"/Users/{ctx.author.id}/Tutorials/{course}").update({tut: None})
    await ctx.reply(f"You are no longer watching {tut} for {course}")



bot.run(os.getenv("TOKEN"))

