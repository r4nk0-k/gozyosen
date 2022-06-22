from discord.ext import commands
import random
import asyncio

# //////////////////////////////////////////////////////////////////////
# constant definition
GOJO_EMOJI = "<:gojo:836228626957074453>"
MARKS = ["<:emoji_48:986146778279718912>", "<:gojo:836228626957074453>"]
MARKS_SLOT = ["<:emoji_47:981211597093621771>", "<:emoji_46:981211581587279883>", "<:dayu_coume:929077269568294934>", "<:koume_another:937032580182728774>", "<:fushigidane:838103311734669393>", "<:seikintv:885186342907170906>", "<:chiikawa_bakemon:929075742296399954>", "<:emoji_48:986146778279718912>", "<:gojo:836228626957074453>"]
MARKS_WACCA = ["<:su:986850329998028831>", "<:teki:986850365951578115>", "<:da:986850393357172757>", "<:ne:986850420439810078>"]

# //////////////////////////////////////////////////////////////////////
# commands 
async def wacca(ctx):
    results = lottery(MARKS_WACCA, 4)
    txt = ""
    for r in results:
        txt = txt + r + " "
    await ctx.send(txt)

async def gozyosen_slot(ctx):
    await do_slot(MARKS, ctx)

async def slot(ctx):
    options = ctx.message.content.split()

    for option in options:
        if option == "-l":
            txt = "図柄一覧\n"
            for mark in MARKS_SLOT:
                txt = txt + mark

            await ctx.send(txt)
            await ctx.send("当選確率: 1/" + str(pow(len(MARKS_SLOT), 3)))
            return

    await do_slot(MARKS_SLOT, ctx)

# //////////////////////////////////////////////////////////////////////
# utility
def lottery(marks, try_num):
    results = []
    for leel in range(try_num):
        index = random.randint(0, len(marks)-1)
        results.append(marks[index])

    return results

def check_match(results):
    previous_r = results[0]
    for r in results:
        if previous_r != r:
            return False
    
    return True

async def do_slot(marks, ctx):
    results = lottery(marks, 3)
    line1 = ""
    line2 = ""
    message = await ctx.send("ｸﾞﾙｸﾞﾙｸﾞﾙｸﾞﾙ...")
    message2 = None
    for index, r in enumerate(results):
        await asyncio.sleep(0.3)
        if results[0] == results[1] and index == len(results) - 1:
            line_reach = line1
            line_reach += "ﾘｰﾁ！"
            await message.edit(content=line_reach)

            performance_num = random.randint(10,15)
            for index in range(performance_num):
                if index == performance_num - 1:
                    await message2.edit(content=line2 + MARKS_SLOT[MARKS_SLOT.index(results[0])])
                    await asyncio.sleep(1)
                else:
                    mark_index = random.randint(0, len(MARKS_SLOT) - 1)
                    await message2.edit(content=line2 + MARKS_SLOT[mark_index])
                    await asyncio.sleep(0.3)
        
        line1 += "ﾁﾝｯ "
        line2 += r 

        await message.edit(content=line1)
        if message2 is None:
            message2 = await ctx.send(line2)
        else:
            await message2.edit(content=line2)

    if check_match(results):
        await ctx.send(GOJO_EMOJI + GOJO_EMOJI + GOJO_EMOJI + GOJO_EMOJI + GOJO_EMOJI + GOJO_EMOJI + " < Congrats...")
