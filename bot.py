import discord
from discord.ext import commands
import csv
import asyncio
import re

TOKEN = "MY TOKEN!"
ID_CANAL_LOG = 1370931007414603896
admins = [648283942017040425, 231169616645193738]
DONO_ID = 648283942017040425

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

perguntas = [
    "Você faz parte da comunidade LGBTQIA+ ou é Therian? (responda apenas com 's' ou 'n')",
    "Qual a sua idade?",
    "Quem é o GOAT?\n A) Kobe Bryant\n B) Kanye West\n C) Rodrigo Faro\n D) Coelho do Nesquik (prime 2000)",
    "Quem era mais perigoso no prime: P. Diddy ou 4lan?",
    "O que você acha do Davi Brito?"
]

@bot.event
async def on_ready():
    print(f"✅ Bot online como {bot.user}")

@bot.event
async def on_member_join(member):
    spam_count = 0
    tentativas = 0

    try:
        await member.send(
            f"Olá, {member.mention}! Vamos começar um pequeno questionário de entrada no servidor.\n"
            "Responda com sinceridade. Envie cada resposta separadamente após a pergunta aparecer.\n"
            "Você tem 2 minutos para responder cada pergunta, caso contrário será expulso."
        )

        respostas = []

        def check(m):
            nonlocal spam_count
            if m.author == member and isinstance(m.channel, discord.DMChannel):
                spam_count += 1
                return True
            return False

        i = 0
        while i < len(perguntas):
            pergunta = perguntas[i]
            await member.send(pergunta)

            try:
                msg = await bot.wait_for("message", check=check, timeout=120.0)
            except asyncio.TimeoutError:
                await member.send("⏰ Você demorou demais para responder. Você será removido do servidor.")
                await member.kick(reason="Demorou demais para responder ao questionário.")
                return

            resposta = msg.content.strip().lower()

            # Controle de spam
            if spam_count > 5:
                tentativas += 1
                if tentativas >= 2:
                    await member.send("🚫 Você foi expulso por spam.")
                    await member.kick(reason="Spam no questionário.")
                    return
                await member.send("⚠️ Por favor, pare de spamar ou será expulso. Vamos recomeçar o questionário.")
                return await on_member_join(member)

            # Validação da pergunta 1 (banimento)
            if i == 0 and resposta not in ["n", "nao", "não", "n!", "nao!", "não!"]:
                await member.send("❌ Você foi banido do servidor com base na resposta à primeira pergunta.\nhttps://tenor.com/view/xd-fani-gif-24750348")
                await member.ban(reason="Resposta afirmativa à pergunta 1 do questionário.")
                dono = await bot.fetch_user(DONO_ID)
                if dono:
                    await dono.send(f"🚨 {member.name} ({member.id}) foi banido por responder '{resposta}' na pergunta 1.")
                return

            # Validação da pergunta 2 (idade)
            if i == 1:
                if not resposta.isdigit() or len(resposta) > 2:
                    await member.send("Apenas sua idade, amigão.")
                    continue
                idade = int(resposta)
                if idade < 17:
                    await member.send("❌ Você deve ter pelo menos 17 anos para entrar no servidor. Você será removido.")
                    await member.kick(reason="Idade menor que 17.")
                    return

            # Validação da pergunta 3 (GOAT)
            if i == 2:
                if resposta not in ['a', 'a)', 'kobe', 'kobe bryant']:
                    await member.send("❌ Tenta dnv ai amigão")
                    continue

            respostas.append(resposta)
            i += 1

        # Salvar no CSV
        with open("respostas_questionario.csv", "a", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([member.name, member.id] + respostas)

        # Log para o canal
        canal_logs = bot.get_channel(ID_CANAL_LOG)
        if canal_logs:
            texto = f"📋 Novo questionário respondido por {member.mention}:\n"
            for idx, (pergunta, resposta) in enumerate(zip(perguntas, respostas), start=1):
                pergunta_curta = re.sub(r"\s+", " ", pergunta.split('\n')[0].strip())
                texto += f"{idx}. {pergunta_curta} ➜ {resposta}\n"
            await canal_logs.send(texto)

        await member.send("✅ Questionário concluído. Seja bem-vindo(a) ao servidor!")

    except Exception as e:
        print(f"[ERRO] {e}")
        try:
            await member.send("❌ Ocorreu um erro durante o questionário. Você será removido do servidor.")
            await member.kick(reason="Erro durante o questionário.")
        except:
            pass

@bot.command()
async def logs(ctx, quantidade: int = 5):
    if ctx.author.id not in admins:
        await ctx.send("❌ Você não tem permissão para usar este comando.")
        return

    try:
        with open("respostas_questionario.csv", "r", encoding="utf-8") as f:
            linhas = f.readlines()
            if not linhas:
                await ctx.send("⚠️ Nenhum log encontrado.")
                return

            ultimos = linhas[-quantidade:]
            resposta = "📄 **Últimos logs de questionário:**\n"
            for linha in ultimos:
                partes = linha.strip().split(',')
                nome = partes[0]
                user_id = partes[1]
                respostas = partes[2:]
                resposta += f"👤 `{nome}` ({user_id}) ➜ {' | '.join(respostas)}\n"

            await ctx.send(resposta)

    except FileNotFoundError:
        await ctx.send("❌ Arquivo de log não encontrado.")

bot.run(TOKEN)
