import discord
import re
import datetime
import yaml

# //////////////////////////////////////////////////////////////////////
# constant definition
EMOJI_NUM = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
HAS_31_DAYS_MONTH = [1,3,4,7,8,10,12]

async def poll(ctx, question):
    choices = ctx.message.content.split()
    if question == None or len(choices) < 3:
        await ctx.send("Usage: &poll <question> <choices1> <choices2>...")
        return

    if len(choices) > 13:
        await ctx.send("選択肢は10個以上作れません")
        return
    
    if "-d" in choices:
        del choices[choices.index("-d")]
        if re.match("[0-9]{2}/[0-9]{2}-[0-9]{2}/[0-9]{2}", choices[2]):
            start_end_date = choices[2].split("-")
            start_date = start_end_date[0].split("/")
            end_date = start_end_date[1].split("/")

            if not check_datetime(int(start_date[0]), int(start_date[1])) or not check_datetime(int(end_date[0]), int(end_date[1])):
                await ctx.send("日付指定に誤りがあります")
                return

            start_datetime = datetime.datetime.strptime(start_end_date[0], '%m/%d')
            end_datetime = datetime.datetime.strptime(start_end_date[1], '%m/%d')
            
            if end_datetime.month > start_datetime.month or (start_datetime.month == end_datetime.month and end_datetime.day < start_datetime.day):
                await ctx.send("日付指定に誤りがあります")
                return

            diff = end_datetime - start_datetime
            if 10 < diff:
                await ctx.send("選択肢は10個以上作れません")
                return
            dates = []
            for date in range(diff.days):
                tmp_datetime = start_datetime + datetime.timedelta(days=date)
                dates.append(tmp_datetime.strftime("%m/%d"))
            
            dates.append(end_datetime.strftime("%m/%d"))

            embed = discord.Embed(title="Q." + question,description=question)
            for index, date in enumerate(dates):
                embed.add_field(name = EMOJI_NUM[index] + " " + date, value = "None")

            message = await ctx.send(embed=embed)
            embed.insert_field_at(0, name = "message_id", value = message.id, inline = False)
            for index in range(len(embed.fields)):
                await message.add_reaction(EMOJI_NUM[index])

        else:
            await ctx.send("-dオプションを使うときは、`&poll -d mm/dd-mm/dd`の形式で指定してください")
        return

    if "-e" in choices:
        if len(choices) < 4:
            await ctx.send("引数が足りません")
            return

        message_id = choices[-1]
        message = await ctx.fetch_message(message_id)

        embed = message.embeds[0]
        new_choice = choices[-2]

        index = len(embed.fields) - 1

        embed.add_field(name = EMOJI_NUM[index] + " " + new_choice, value = "None")
        await message.edit(embed=embed)
        await message.add_reaction(EMOJI_NUM[index])
        return

    del choices[0:2]
    if len(choices) > 10:
        await ctx.send("選択肢は10個以下にしてください")
        return

    embed = discord.Embed(title="Q." + question,description=question)
    for index, choice in enumerate(choices):
        embed.add_field(name = EMOJI_NUM[index] + " " + choice, value = "None")

    message = await ctx.send(embed=embed)
    embed.insert_field_at(0, name = "message_id", value = message.id, inline = False)
    await message.edit(embed = embed)
    for index in range(len(embed.fields) - 1):
        await message.add_reaction(EMOJI_NUM[index])

async def on_raw_reaction_add(payload, embed, message, user):
    select_num = None
    for index in range(len(embed.fields) - 1):
        if EMOJI_NUM[index] == str(payload.emoji):
            select_num = index + 1

    if select_num == None:
        return
    
    previous_value = embed.fields[select_num].value
    if previous_value == "None":
        previous_value = ""
    else:
        previous_value = previous_value + ", "

    value = previous_value + user.mention
    embed.set_field_at(select_num, name=embed.fields[select_num].name, value=value)

    await message.edit(embed = embed)

async def on_raw_reaction_remove(payload, embed, message, user):
    select_num = None
    for index in range(len(embed.fields) - 1):
        if EMOJI_NUM[index] == str(payload.emoji):
            select_num = index + 1

    if select_num == None:
        return
    
    previous_value = embed.fields[select_num].value
    value = previous_value.replace(", " + user.mention, "")
    value = value.replace(user.mention, "")
    if value == "":
        value = "None"
    
    embed.set_field_at(select_num, name=embed.fields[select_num].name, value=value)

    await message.edit(embed = embed)

# //////////////////////////////////////////////////////////////////////
# utility 
def check_datetime(month, day):
    if month > 12 or month <= 0:
        return False

    if day > 31 or day < 0:
        return False
    
    if month not in HAS_31_DAYS_MONTH:
        days = 30
        if month == 2:
            days = 28
        if day > days:
            return False

    return True