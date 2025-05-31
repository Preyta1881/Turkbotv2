import os
import re
import discord
from discord.ext import commands
from dotenv import load_dotenv
import aiohttp
from urllib.parse import quote

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
        description=f"**Şikayetçi:** {ctx.author.mention}\n**Sebep:** {sebep}",
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

# --- Burada eski !sunucu komutu kaldırıldı ---

@bot.command(name="sunucu")
async def oyunculistesi(ctx):
    hedef_sunucu_adi = "[TURK] FatherOfTheTurks JOIN: discord.gg/TURKBF1"
    encoded_query = quote("[TURK]")
    url = f"https://api.gametools.network/bf1/servers/?name={encoded_query}"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    await ctx.send(f"API hatası: HTTP {resp.status}")
                    return

                json_data = await resp.json()

                if isinstance(json_data, dict) and "error" in json_data:
                    await ctx.send(f"API Hatası: {json_data['error']}")
                    return

                if "servers" not in json_data:
                    await ctx.send("Sunucu listesi verisi alınamadı.")
                    return

                sunucular = json_data["servers"]
                hedef = next(
                    (srv for srv in sunucular if hedef_sunucu_adi in srv.get("prefix", "")),
                    None
                )

                if not hedef:
                    await ctx.send("Sunucu bulunamadı. Adı tam olarak eşleşmedi.")
                    return

                player_amount = hedef.get("playerAmount", "Bilinmiyor")
                max_players = hedef.get("maxPlayers", "Bilinmiyor")
                current_map = hedef.get("currentMap", "Bilinmiyor")
                mode = hedef.get("mode", "Bilinmiyor")
                region = hedef.get("region", "Bilinmiyor")
                queue_count = hedef.get("inQue", 0)
                server_url = hedef.get("url", None)

                embed = discord.Embed(
                    title=f"🎮 {hedef_sunucu_adi} - Sunucu Bilgisi",
                    color=discord.Color.blue()
                )

                embed.add_field(name="Harita", value=current_map, inline=True)
                embed.add_field(name="Mod", value=mode, inline=True)
                embed.add_field(name="Bölge", value=region, inline=True)
                embed.add_field(name="Oyuncu Sayısı", value=f"{player_amount} / {max_players}", inline=True)

                if queue_count and int(queue_count) > 0:
                    embed.add_field(name="Sıradaki Oyuncu Sayısı", value=str(queue_count), inline=True)

                if server_url:
                    embed.set_thumbnail(url=server_url)

                embed.set_footer(text="Sunucunun anlık durumudur.")
                embed.timestamp = discord.utils.utcnow()

                await ctx.send(embed=embed)

    except Exception as e:
        print(f"[HATA] {e}")
        await ctx.send("Bir hata oluştu.")



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
    embed.add_field(name="!sunucu", value="Battlefield 1 sunucusunun anlık durumu ve oyuncu sayısını gösterir", inline=False)
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

# BOT NESNESİNİ EXPORT ET (main.py'de import için)
__all__ = ["bot"]

if __name__ == "__main__":
    bot.run(BOT_TOKEN)
