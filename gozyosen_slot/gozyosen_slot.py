from discord.ext import commands
import random
import asyncio
import yaml

# //////////////////////////////////////////////////////////////////////
# constant definition

slot_settings = yaml.load(open('token.yaml').read(), Loader=yaml.SafeLoader)['gozyosen_slot']
GOJO_EMOJI = slot_settings['emoji']['gojo']
MARKS = slot_settings['emoji']['slot_marks_gojo']
MARKS_SLOT = slot_settings['emoji']['slot_marks']
MARKS_WACCA = slot_settings['emoji']['wacca']

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
