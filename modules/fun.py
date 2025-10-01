import discord
from discord.ext import commands
import requests
import random
from bs4 import BeautifulSoup 
from PIL import  Image, ImageFont, ImageDraw, ImageChops
import io

class fun:
    def __init__(self, client, db, cursor, cfg):
        self.client = client
        self.db = db
        self.cursor = cursor
        self.cfg = cfg


        @client.slash_command(description='Отпавить анонимное сообщение')
        async def anonym(interaction:discord.Interaction, 
                         message: discord.Option(str, name = "сообщение", 
                                                 description="анонимное сообщение, которое вы хотите отправить"), mention: discord.Option(discord.Member, name = "упоминание", description="Если указать пользователя, то при отправке он получит упоминание.", required=False)): # type: ignore
            embed = discord.Embed(title="📩 Новое анонимное сообщение", description=f"```{message}```", color=discord.Color.from_rgb(43,45,49))
            embed.set_image(url = "https://cdn.discordapp.com/attachments/1225874573774553191/1225877520457662524/anonym.png")
            if mention is None:
                await client.get_channel(1225878942494359582).send(embed = embed)
                await interaction.response.send_message(embed = discord.Embed(title="", description=f"Ваше анонимное сообщение отправлено 😉", color=discord.Color.from_rgb(43,45,49)),ephemeral=True)
            else:
                if mention == interaction.user:
                    await interaction.response.send_message(embed = discord.Embed(title="", description=f"Вы не можете указать сами себя.", color=discord.Color.from_rgb(43,45,49)),ephemeral=True)
                else:
                    await client.get_channel(cfg.ANON_CHAT).send(mention.mention)
                    await client.get_channel(cfg.ANON_CHAT).send(embed = embed)
                    await interaction.response.send_message(embed = discord.Embed(title="", description=f"Ваше анонимное сообщение отправлено 😉", color=discord.Color.from_rgb(43,45,49)),ephemeral=True)



        @client.slash_command(description='случайная паста')
        async def pasta(interaction: discord.Interaction):
            try:
                url = f"https://copypastas.ru/copypasta/{random.randint(1, 1600)}/"
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                copypasta_div = soup.find('div', class_='K32Wd')
                
                if copypasta_div:
                    text = copypasta_div.get_text(strip=True)
                
                    if len(text) > 2000:
                        text = text[:1997] + "..."
                    await interaction.response.send_message(text)
                else:
                    await interaction.response.send_message(
                        "❌ Не удалось найти пасту. Попробуйте снова!",
                        ephemeral=True
                    )
                    
            except requests.RequestException as e:
                await interaction.response.send_message(
                    f"❌ Ошибка при получении пасты: {str(e)}",
                    ephemeral=True
                )
            except Exception as e:
                await interaction.response.send_message(
                    f"❌ Неизвестная ошибка: {str(e)}",
                    ephemeral=True
                )
        
        @client.event
        async def on_ready():
            activity = discord.Activity(type=discord.ActivityType.watching, name="by exxortq")
            await client.change_presence(status=discord.Status.online, activity=activity)
            print("[!] Bot is active")
            print("[!] Author: exxortq | t.me/moveax064")
            for guild in client.guilds:
                for member in guild.members:
                    if cursor.execute(f"""SELECT id FROM users WHERE id = {member.id}""").fetchone() is None:
                        cursor.execute(f"INSERT INTO users VALUES({member.id}, {0},{0})")
                    if cursor.execute(f"""SELECT user1, user2, user3 FROM fun WHERE rowid = {1}""").fetchone() is None:
                        cursor.execute(f"INSERT INTO fun VALUES({0}, {0}, {0})")
            db.commit()

        @client.event
        async def on_member_join(member):
            for guild in client.guilds:
                for member in guild.members:
                    if cursor.execute(f"""SELECT id FROM users WHERE id = {member.id}""").fetchone() is None:
                        cursor.execute(f"INSERT INTO users VALUES({member.id}, {0}, {0})")
            db.commit()

            guild = client.get_guild(842061336879955968)
            emoji = discord.utils.get(guild.emojis, name="dogalert")
            image = Image.open("source/source.png")
            draw = ImageDraw.Draw(image)
            font = ImageFont.truetype("source/font.ttf", 90, encoding='unic')
            text = member.name
            draw.text(xy=(280, 170), text=text, fill=(0,0,0), font=font)
            memberavatar = member.avatar._url
            if memberavatar == None:
                memberavatar = "https://i.pinimg.com/736x/7e/ca/92/7eca921a1c1aad67284fed28a36e4ded.jpg"
            avatarImage = Image.open(requests.get(memberavatar, stream=True).raw).convert("RGBA")
            avatarImage = avatarImage.resize((170,170))
            cornersMask = Image.new('L', avatarImage.size)
            cornersDraw = ImageDraw.Draw(cornersMask)
            w, h = cornersMask.size
            cornersDraw.rounded_rectangle([ 0, 0, w, h ], radius=160, fill=255)
            image.paste(avatarImage, (67,149), mask=cornersMask)
            buffer = io.BytesIO()
            image.save(buffer, format='PNG')
            buffer.seek(0)
            file = discord.File(buffer, filename="image.png")

            embed = discord.Embed(description=f"Добро пожаловать на наш сервер.\n"
            f"В канале <#984781239963770890> ты можешь узнать о нашем сервере больше\n"
            f"Изучи <#952877399979212840>, чтобы избежать нарушения правил\n", color=discord.Color.from_rgb(43,45,49))

            embed.set_image(url="attachment://image.png")
            await client.get_channel(cfg.chat).send(f"{emoji} NEW MEMBER ALERT {emoji}\n{member.mention}",file=file, embed=embed)






        
                    
        

            


