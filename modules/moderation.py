import discord
from discord.ext import commands
import asyncio
from datetime import timedelta


class Moderation(commands.Cog):
    def __init__(self, client, db, cursor, cfg):
        self.client = client
        self.db = db
        self.cursor = cursor
        self.cfg = cfg

        @client.slash_command(description='забанить пользователя')
        @commands.has_any_role(cfg.AdminRole) 
        async def ban(
                interaction: discord.Interaction,
                user: discord.Option(discord.Member, name="юзер", description="Пользователь"), # type:ignore
                reason: discord.Option(str, name="причина", description="Причина бана") # type:ignore
            ):
            embed = discord.Embed(title="Ban", description=f"Администратор {interaction.user.mention} забанил {user.mention}\nПричина:{reason}")
            await interaction.response.send_message(embed=embed)
            await client.get_channel(cfg.log_chat).send(embed = embed)
            await user.ban(reason=reason)

        @client.slash_command(description='кикнуть пользователя')
        @commands.has_any_role(cfg.AdminRole) 
        async def kick(
                interaction: discord.Interaction,
                user: discord.Option(discord.Member, name="юзер", description="Пользователь"), # type:ignore
                reason: discord.Option(str, name="причина", description="Причина кика") # type:ignore
            ):
            embed = discord.Embed(title="Kick", description=f"Администратор {interaction.user.mention} кик {user.mention}\nПричина:{reason}")
            await interaction.response.send_message(embed=embed)
            await client.get_channel(cfg.log_chat).send(embed = embed)
            await user.kick(reason=reason)


        @client.slash_command(description='выдать таймаут пользователю')
        @commands.has_any_role(cfg.AdminRole)
        async def timeout(
            interaction: discord.Interaction,
            user: discord.Option(discord.Member, name="юзер", description="Пользователь"), # type:ignore
            duration: discord.Option(int, name="время", description="Длительность таймаута", 
                                    choices=[
                                        discord.OptionChoice(name="1 минута", value=1),
                                        discord.OptionChoice(name="5 минут", value=5),
                                        discord.OptionChoice(name="10 минут", value=10),
                                        discord.OptionChoice(name="30 минут", value=30),
                                        discord.OptionChoice(name="1 час", value=60),
                                        discord.OptionChoice(name="1 день", value=1440),
                                        discord.OptionChoice(name="1 неделя", value=10080)
                                    ]), # type:ignore
            reason: discord.Option(str, name="причина", description="Причина таймаута") # type:ignore
            ):
            timeout_duration = discord.utils.utcnow() + timedelta(minutes=duration)
            
            await user.timeout(timeout_duration, reason=reason)
            
            duration_names = {
                1: "1 минута",
                5: "5 минут", 
                10: "10 минут",
                30: "30 минут",
                60: "1 час",
                1440: "1 день",
                10080: "1 неделя"
            }
            
            duration_text = duration_names.get(duration, f"{duration} минут")
            
            # Создаем embed
            embed = discord.Embed(
                title="Таймаут",
                description=f"Администратор {interaction.user.mention} выдал таймаут {user.mention}\nПричина: {reason}\nДлительность: {duration_text}",
                color=discord.Color.orange()
            )
            await interaction.response.send_message(embed=embed)
        
            await client.get_channel(cfg.log_chat).send(embed=embed)
            

            

                