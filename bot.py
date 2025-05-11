import discord
from discord.ext import commands
from discord import Member
import csv

# CONFIGURAÇÕES
TOKEN = "MTI0ODIzMjMyODUxMDMxMjQ5MQ.GHYwDc.aPWa4tO5ZN6zz9AnDuDmVspk0DmU8Zu_k-TxVU"  # Substitua pelo token do seu bot
ID_CANAL_LOG = 1370931007414603896  # Substitua pelo ID do canal de log
admins = [648283942017040425, 231169616645193738]  # IDs reais dos admins

# INTENTS
intents = discord.Intents.default()
intents.members = True

# CRIAÇÃO DO BOT
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"🤖 Bot online como {bot.user}")

@bot.event
async def on_member_join(member):
    try:
        await member.send(
            f"Olá, {member.mention}! Vamos começar um pequeno questionário de entrada no servidor.\n"
            "Responda com sinceridade. Envie cada resposta separadamente após a pergunta aparecer.\n"
        )

        perguntas = [
            "1. Você se identifica como mulher ou homem?",
            "2. Você faz parte da comunidade LGBTQIA+ ou é Terian? (responda apenas com 's' ou 'n')",
            "3. Qual a sua idade?",
            "4. Quem é o GOAT (melhor jogador) do basquete?\n"
            "   a) Kobe Bryant\n"
            "   b) LeBron James\n"
            "   c) Jim Carrey\n"
            "   d) Rodrigo Faro\n",
            "5. Quem era mais perigoso no prime: P. Diddy ou 4lan?",
            "6. O que você acha do Davi Brito?"
        ]

        respostas = []

        def check(m):
            return m.author == member and isinstance(m.channel, discord.DMChannel)

        for i, pergunta in enumerate(perguntas):
            await member.send(pergunta)
            msg = await bot.wait_for('message', check=check, timeout=120.0)
            resposta = msg.content.strip().lower()

            if i == 3 and resposta not in ['a', 'b', 'c', 'd']:
                await member.send("Resposta inválida para a pergunta 4. Use apenas: a, b, c ou d.")
                return

            respostas.append(resposta)

        # 🔹 SALVA RESPOSTAS EM CSV
        with open("respostas_questionario.csv", "a", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([member.name, member.id] + respostas)

        # 🔹 ENVIA PARA CANAL DE LOG
        canal_logs = bot.get_channel(ID_CANAL_LOG)
        if canal_logs:
            await canal_logs.send(
                f"📋 Novo questionário respondido por {member.mention}:\n"
                + "\n".join([f"{i+1}. {res}" for i, res in enumerate(respostas)])
            )

        # 🔹 NOTIFICA ADMINS SE MULHER
        if respostas[0] == "sim":
            for admin_id in admins:
                admin = bot.get_user(admin_id)
                if admin:
                    await admin.send(
                        f"👤 Novo membro identificado como mulher: {member.name} ({member.id})\n"
                        "📋 Respostas:\n" + "\n".join([f"{i+1}. {res}" for i, res in enumerate(respostas)])
                    )

        # 🔹 BANIR SE PERTENCER À COMUNIDADE
        if respostas[1] == "sim":
            await member.send("Você foi removido do servidor com base nas respostas fornecidas.")
            await member.ban(reason="Respondeu 'sim' à pergunta 2 do questionário.")
            for admin_id in admins:
                admin = bot.get_user(admin_id)
                if admin:
                    await admin.send(
                        f"🚫 {member.name} foi banido com base na resposta à pergunta 2.\n"
                        "📋 Respostas:\n" + "\n".join([f"{i+1}. {res}" for i, res in enumerate(respostas)])
                    )
            return

        await member.send("✅ Questionário concluído. Seja bem-vindo(a) ao servidor!")

    except Exception as e:
        print(f"[ERRO] {e}")
        try:
            await member.send("Ocorreu um erro durante o questionário ou você demorou demais para responder.")
        except:
            pass

# INICIA O BOT
bot.run(TOKEN)
