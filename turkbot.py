import os
import re
import discord
from discord.ext import commands
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

# Ortam değişkenlerini al
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ROLE_ID = int(os.getenv("ADMIN_ROLE_ID"))
TARGET_BOT_ID = int(os.getenv("TARGET_BOT_ID"))
VIP_CHANNEL_ID = int(os.getenv("VIP_CHANNEL_ID"))

# Harita emojileri
MAP_EMOJIS = {
    "Sinai Desert": "🏜️",
    "Nivelle Nights": "🌃",
    "Amiens": "🏘️",
    "Verdun Heights": "🔥",
    "Ballroom Blitz": "🎭",
    "Achi Baba": "☪️",
    "Suez ": "🌴 ",
    # Yeni haritalar ekleyebilirsin
}

# İzinler
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
intents.presences = True
intents.members = True

# Bot başlat
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot giriş yaptı: {bot.user}")

# -- KOMUTLAR --

@bot.command()
async def report(ctx, *, sebep="Sebep belirtilmedi."):
    embed = discord.Embed(
        title="📢 Şikayet Bildirimi",
        description=(
            f"**Şikayetçi:** {ctx.author.mention}\n"
            f"**Sebep:** {sebep}"
        ),
        color=discord.Color.red()
    )
    await ctx.send(
        content=f"<@&{ADMIN_ROLE_ID}>",
        embed=embed,
        allowed_mentions=discord.AllowedMentions(roles=[discord.Object(id=ADMIN_ROLE_ID)])
    )

@bot.command()
async def klan(ctx):
    embed = discord.Embed(
        title=":medal: Klanımıza Katılma Şartları",
        description=(
            "Stratejik, saygılı ve eğlenceli bir topluluk kurmayı amaçlıyoruz.\n\n"
            ":white_check_mark: Takım oyunu bilinci\n"
            ":white_check_mark: Aktif iletişim (Discord)\n"
            ":white_check_mark: Saygılı davranışlar\n"
            ":white_check_mark: Deneme sürecine hazır olma\n\n"
            "Not: Klanımız sadece oyun grubu değil, aynı zamanda bir dostluk ortamıdır."
        ),
        color=discord.Color.purple()
    )
    await ctx.send(embed=embed)

@bot.command()
async def sunucu(ctx):
    TARGET_BOT_ID = 1346398667912777738
    guild = ctx.guild

    target = guild.get_member(TARGET_BOT_ID)
    if not target:
        return await ctx.send("❌ Hedef bot bu sunucuda bulunamadı veya bilgisine erişilemiyor.")

    activities = target.activities
    if not activities:
        return await ctx.send("ℹ️ Hedef botun herhangi bir aktivitesi yok.")

    # Debug: aktiviteleri listele
    activity_names = [getattr(act, "name", str(act)) for act in activities]
    print(f"DEBUG - Aktiviteler: {activity_names}")

    # Sıra opsiyonel
    pattern = re.compile(r"(\d+)\s*/\s*(\d+)(?:\s*\[(\d+)\])?\s*-\s*(.+)")

    for act in activities:
        name = getattr(act, "name", None)
        if not name:
            continue

        match = pattern.match(name)
        if match:
            current, maximum, slot, map_name = match.groups()
            current, maximum = int(current), int(maximum)
            percent_full = current / maximum if maximum else 0

            if percent_full >= 0.9:
                color = discord.Color.red()
            elif percent_full >= 0.5:
                color = discord.Color.gold()
            else:
                color = discord.Color.green()

            emoji = MAP_EMOJIS.get(map_name.strip(), "")
            map_display = f"{emoji} {map_name.strip()}" if emoji else map_name.strip()

            embed = discord.Embed(
                title="🎮 Battlefield 1 Sunucu Durumu",
                color=color
            )
            embed.add_field(name="🗺️ Harita", value=map_display, inline=False)
            embed.add_field(name="👥 Oyuncu Sayısı", value=f"{current} / {maximum}", inline=True)
            if slot:
                embed.add_field(name="🧩 Sıra", value=f"[{slot}]", inline=True)
            embed.set_footer(text="Sunucu durumu gerçek zamanlıdır.")
            return await ctx.send(embed=embed)

    await ctx.send("⚠️ Aktivite içinde uygun bilgi bulunamadı.")

@bot.command()
async def vip(ctx):
    embed = discord.Embed(
        title="🌟 VIP Üyelik Sistemi",
        description=(
            "Sunucumuzu destekleyerek hem topluluğumuza katkıda bulunabilir hem de özel ayrıcalıklardan faydalanabilirsiniz!\n\n"
            "[VIP hakkında detaylı bilgi için tıklayın.](https://discord.com/channels/1263798839567978616/1332591877953814528/1332593141106212926)"
        ),
        color=discord.Color.gold()
    )
    await ctx.send(embed=embed)

@bot.command()
async def yardim(ctx):
    embed = discord.Embed(
        title="📘 Yardım Menüsü",
        description="Botun mevcut komutları aşağıdadır:",
        color=discord.Color.blue()
    )
    embed.add_field(name="!vip", value="VIP üyelik hakkında bilgi verir", inline=False)
    embed.add_field(name="!report [sebep]", value="Yetkililere şikayet bildirimi gönderir", inline=False)
    embed.add_field(name="!kurallar", value="Sunucu kurallarını gösterir", inline=False)
    embed.add_field(name="!bf1", value="Battlefield 1 sunucu kurallarını gösterir", inline=False)
    embed.add_field(name="!klan", value="Klan katılım koşullarını listeler", inline=False)
    embed.add_field(name="!sunucu", value="Battlefield 1 sunucusunun durumu ve oyuncu sayısını gösterir", inline=False)
    embed.add_field(name="!link", value="Sunucu davet bağlantısını gönderir", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def kurallar(ctx):
    embed = discord.Embed(
        title="📜 Sunucu Kuralları",
        description=(
            "• Herhangi bir üyeye veya yetkiliye karşı küfür veya hakaret kesinlikle yasaktır.\n"
            "• Ticaret yasaktır.\n"
            "• Duruma küfür, hakaret veya reklam yazısı yazmak yasaktır.\n"
            "• Sansürlü küfür yasaktır.\n"
            "• Din / dil / ırk gibi şeylerle dalga geçmek yasaktır.\n"
            "• Onur kırıcı, yaş, isim gibi konularda alay yasaktır.\n"
            "• Siyaset yapmak, +18 içerik paylaşmak yasaktır.\n"
            "• Flood, spam, caps lock kullanımı yasaktır.\n"
            "• Klan/etiket topluluklarının küfürlü davranışı yasaktır.\n"
            "• Cinsel yönelimlere hakaret yasaktır.\n"
            "• Ses kanallarında küfürlü müzikler veya yüksek sesli içerikler yasaktır.\n"
            "• Kuralları kabul etmiyorsanız sunucudan ayrılmanız önerilir."
        ),
        color=discord.Color.orange()
    )
    await ctx.send(embed=embed)

@bot.command()
async def bf1(ctx):
    embed = discord.Embed(
        title="🎮 Battlefield 1 Sunucu Kuralları",
        description=(
            "• Küfür yasak\n"
            "• RAM yasak\n"
            "• Base Rape yasak\n"
            "• Siyaset yasak\n\n"
            "[Detaylı bilgi için buraya tıklayın](https://discord.com/channels/1263798839567978616/1327393737810251837)"
        ),
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)

@bot.command()
async def link(ctx):
    await ctx.send("🔗 Sunucumuza katılmak için: https://discord.gg/TURKBF1")

# BOTU ÇALIŞTIR
bot.run(BOT_TOKEN)
