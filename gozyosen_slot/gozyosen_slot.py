from discord.ext import commands
import random
import asyncio
import yaml

# //////////////////////////////////////////////////////////////////////
# commands 

class GozyosenSlot(commands.Cog, yaml_path='settings.yaml'):
    def __init__(self, bot):
        self.bot = bot
        slot_settings = yaml.load(open('settings.yaml').read(), Loader=yaml.SafeLoader)['gozyosen_slot']
        self.GOJO_EMOJI = slot_settings['emoji']['gojo']
        self.MARKS = slot_settings['emoji']['slot_marks_gojo']
        self.MARKS_SLOT = slot_settings['emoji']['slot_marks']
        self.MARKS_WACCA = slot_settings['emoji']['wacca']
        self.ENABLE_CHANNELS = slot_settings['enable_channels']
        self.PROBABILITY = slot_settings['probability']

    @commands.command(name="素敵だね")
    async def wacca(self, ctx):
        results = lottery(self.MARKS_WACCA, 4)
        txt = ""
        for r in results:
            txt = txt + r + " "
        await ctx.send(txt)

    @commands.command(name="ごじょせんスロット")
    async def gozyosen_slot(self, ctx):
        await self.do_slot(self.MARKS, ctx, self.PROBABILITY)

    @commands.command(aliases=['s'])
    async def slot(self, ctx):
        options = ctx.message.content.split()

        for option in options:
            if option == "-l":
                txt = "図柄一覧\n"
                for mark in self.MARKS_SLOT:
                    txt = txt + mark

                await ctx.send(txt)
                await ctx.send("当選確率: 1/" + str(self.PROBABILITY))
                return

        await self.do_slot(self.MARKS_SLOT, ctx, self.PROBABILITY)

    async def do_slot(marks, ctx, probability):
        n = random.randint(1, probability)
        if n == 1:
            mark = random.randint(0, len(marks))
            results = [marks[mark] for _ in range(3)]
        else:
            results = lottery_no_hit(marks, 3)

        line1 = ""
        line2 = ""
        message = await ctx.send("ｸﾞﾙｸﾞﾙｸﾞﾙｸﾞﾙ...")
        message2 = None

        for index, r in enumerate(results):
            await asyncio.sleep(0.3)
            if results[0] == results[1] and index == len(results) - 1:
                await self.do_reach(marks, ctx)
            
            line1 += "ﾁﾝｯ "
            line2 += r 

            await message.edit(content=line1)
            if message2 is None:
                message2 = await ctx.send(line2)
            else:
                await message2.edit(content=line2)

        if check_match(results):
            await ctx.send(self.GOJO_EMOJI + self.GOJO_EMOJI + self.GOJO_EMOJI + self.GOJO_EMOJI + self.GOJO_EMOJI + self.GOJO_EMOJI + " < Congrats...")

    async def do_reach(marks, ctx):
        line_reach = line1
        line_reach += "ﾘｰﾁ！"
        await message.edit(content=line_reach)

        performance_num = random.randint(10,15)
        for index in range(performance_num):
            if index == performance_num - 1:
                await message2.edit(content=line2 + marks[marks.index(results[0])])
                await asyncio.sleep(1)
            else:
                mark_index = random.randint(0, len(marks) - 1)
                await message2.edit(content=line2 + marks[mark_index])
                await asyncio.sleep(0.3)

# //////////////////////////////////////////////////////////////////////
# utility
def lottery_no_hit(marks, try_num):
    results = []
    for _ in range(try_num - 1):
        index = random.randint(0, len(marks)-1)
        results.append(marks[index])

    while True:
        index = random.randint(0, len(marks)-1)
        if not marks[index] in results:
            results.append(marks[index])
            break

    return results

def lottery(marks, try_num):
    results = []
    for _ in range(try_num):
        index = random.randint(0, len(marks)-1)
        results.append(marks[index])

    return results

def check_match(results):
    previous_r = results[0]
    for r in results:
        if previous_r != r:
            return False
    
    return True


def setup(bot):
    return bot.add_cog(GozyosenSlot(bot))
