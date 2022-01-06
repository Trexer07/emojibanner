from discord import user
from discord_components import DiscordComponents, ComponentsBot, Select, SelectOption, Button, ButtonStyle, ActionRow
import discord, sqlite3, datetime, randomstring, os, setting, random
from discord_components.ext.filters import user_filter
import asyncio, requests, json
from setting import admin_id, bot_name
from datetime import timedelta
from discord_webhook import DiscordEmbed, DiscordWebhook
from discord_buttons_plugin import ButtonType
import asyncio
import os

master_id = [자신의 아이디를 넣어주세요.]
client=discord.Client()

def get_logwebhk(serverid):
    con = sqlite3.connect("../DB/" + str(serverid) + ".db")
    cur = con.cursor()
    cur.execute("SELECT logwebhk FROM serverinfo;")
    data = cur.fetchone()[0]
    con.close()
    return data

def now():
    return str(datetime.datetime.now()).split(".")[0]

def make_expiretime(days):
    ServerTime = datetime.datetime.now()
    ExpireTime = ServerTime + timedelta(days=days)
    ExpireTime_STR = (ServerTime + timedelta(days=days)).strftime('%Y-%m-%d %H:%M')
    return ExpireTime_STR

def nowstr():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

def add_time(now_days, add_days):
    ExpireTime = datetime.datetime.strptime(now_days, '%Y-%m-%d %H:%M')
    ExpireTime_STR = (ExpireTime + timedelta(days=add_days)).strftime('%Y-%m-%d %H:%M')
    return ExpireTime_STR

def is_expired(time):
    ServerTime = datetime.datetime.now()
    ExpireTime = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M')
    if ((ExpireTime - ServerTime).total_seconds() > 0):
        return False
    else:
        return True

@client.event
async def on_ready():
    DiscordComponents(client)
    print(f"초대링크: https://discord.com/oauth2/authorize?client_id={client.user.id}&permissions=8&scope=bot\n[!] 로그인 시간 : {now()}\n[!] 봇 이름 : {client.user.name}\n[!] 봇 아이디 : {client.user.id}\n[!] 참가 중인 서버 : {len(client.guilds)}개")
    while True:
        await client.change_presence(activity=discord.Game(f"이모지배너봇 | {len(client.guilds)}서버 사용중"),status=discord.Status.dnd)
        await asyncio.sleep(5)
        await client.change_presence(activity=discord.Game(f"이모지배너봇 | {len(client.guilds)}서버 사용중"),status=discord.Status.dnd)
        await asyncio.sleep(5)
        
@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.author.id in master_id:
        if (message.content.startswith("!생성 ")):
            try:
                create_amount = int(message.content.split(" ")[1])
                if (create_amount <= 0 or create_amount > 60):
                    raise TypeError
            except:
                await message.channel.send("라이센스를 만들 수 없습니다.\n1~60 숫자를 입력하세요.")
                return
            try:
                license_length = int(message.content.split(" ")[2])
                assert license_length != 0
            except:
                license_length = 30

            con = sqlite3.connect("../DB/" + "license.db")
            cur = con.cursor()
            created_licenses = []

            for n in range(create_amount):
                code = "TXBUTTON-" + randomstring.pick(8).upper()
                cur.execute("INSERT INTO license Values(?, ?, ?, ?, ?);", (code, license_length, 0, "None", 0))
                created_licenses.append(code + f"  `{license_length}`일권")

            con.commit()
            con.close()
            await message.channel.send("**생성된 라이센스**\n" + "\n".join(created_licenses))
         
    if message.author.id in master_id:   
        if (message.content.startswith("!검색 ")):
            license_tosearch = message.content.split(" ")[1]
            con = sqlite3.connect("../DB/" + "license.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM license WHERE code == ?;", (license_tosearch,))
            search_result = cur.fetchone()
            if (search_result != None):
                if (search_result[2] != 0):
                    await message.channel.send("**라이센스 검색 결과**\n기간단위 : " + str(search_result[1]) + " 일\n사용 여부 : 사용됨\n사용 시간 : " + str(search_result[3]) + "\n사용된 서버 : " + str(search_result[4]))
                else:
                    await message.channel.send("**라이센스 검색 결과**\n기간단위 : " + str(search_result[1]) + " 일\n사용 여부 : 사용되지 않음")
            else:
                await message.channel.send("라이센스 검색 실패 : 그 라이센스가 없음.")
                
    if message.author.id in master_id:
        if (message.content.startswith("!삭제 ")):

            license_todel = message.content.split(" ")[1:]
            con = sqlite3.connect("../DB/" + "license.db")
            cur = con.cursor()
            for license_ in license_todel:
                cur.execute("DELETE FROM license WHERE code == ?;", (license_,))
            con.commit()
            con.close()
            await message.reply(embed=discord.Embed(title=":white_check_mark:성공",description="라이센스 삭제가 완료되었습니다.", color=0x5c6cdf))
            
            
    if message.content.startswith('!등록 '):
        if message.author.guild_permissions.administrator or message.author.id == int(admin_id):
            license_key = message.content.split(" ")[1]
            con = sqlite3.connect("../DB/" + "license.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM license WHERE code == ?;", (license_key,))
            search_result = cur.fetchone()
            con.close()
            if (search_result != None):
                if (search_result[2] == 0):
                    if not (os.path.isfile("../DB/" + str(message.guild.id) + ".db")):
                        con = sqlite3.connect("../DB/" + str(message.guild.id) + ".db")
                        cur = con.cursor()
                        cur.execute("CREATE TABLE serverinfo (id TEXT, expiredate TEXT, message TEXT, category TEXT, bannername TEXT, emojimsg)
                        con.commit()
                        cur.execute("INSERT INTO serverinfo VALUES(?, ?, ?, ?, ?, ?)(mesage.guild.id, make_expiretime(int(sqlite3.connect("../DB/" + "license.db").cursor().execute("SELECT * FROM license WHERE code == ?;", (license_key,)).fetchone()[1])), "배너조건이 없습니다.", "카테고리가 지정되지않았습니다.", "배너명이 지정되지않았습니다."))
                        con.commit()
                        con.close()
                        con = sqlite3.connect("../DB/" + "license.db")
                        cur = con.cursor()
                        cur.execute("UPDATE license SET isused = ?, useddate = ?, usedby = ? WHERE code == ?;", (1, nowstr(), message.guild.id, license_key))
                        con.commit()
                        con.close()
                        con = sqlite3.connect("../DB/" + "license.db")
                        cur = con.cursor()
                        cur.execute("SELECT * FROM license WHERE code == ?;", (license_key,))
                        await message.author.send(embed=discord.Embed(title="서버 등록 성공", description=f"서버가 성공적으로 등록되었습니다.\n라이센스 기간: `!세팅명령어를 입력하고, 서버정보 버튼을 눌러 확인해주세요.`\n만료일: `" + make_expiretime(int(sqlite3.connect("../DB/" + "license.db").cursor().execute("SELECT * FROM license WHERE code == ?;", (license_key,)).fetchone()[1])) + "`", color=0x4461ff),
                        components = [
                            ActionRow(
                                Button(style=ButtonType().Link,label = "공식디스코드",url="https://buttonvending.xyz/discord"),
                            )
                        ]
                    )
                        await message.channel.send(embed=discord.Embed(title="서버 등록 성공", description="서버가 성공적으로 등록되었습니다.", color=0x5c6cdf))
                        con.close()
                    else:
                        await message.channel.send(embed=discord.Embed(title="서버 등록 실패", description="이미 등록된 서버이므로 등록할 수 없습니다.\n기간 추가를 원하신다면 !세팅명령어를 입력하고, 연장버튼을 눌러 이용해주세요.", color=0x5c6cdf))
                else:
                    await message.channel.send(embed=discord.Embed(title="서버 등록 실패", description="이미 사용된 라이센스입니다.\n관리자에게 문의해주세요.", color=0x5c6cdf))
            else:
                await message.channel.send(embed=discord.Embed(title="서버 등록 실패", description="존재하지 않는 라이센스입니다.", color=0x5c6cdf))
    if message.author.id in master_id:
      if (message.content.startswith("!이모지)):
         if (os.path.isfile("../DB/" + str(message.guild.id) + ".db")):
            try:
               await message.delete()
               
      
client.run(setting.token)
