import discord
from discord.ext import commands
import csv
import asyncio
import re

TOKEN = "myTOKEN"
ID_CANAL_LOG = 1370931007414603896
admins = [648283942017040425, 231169616645193738]

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

perguntas = [
    "Você faz parte da comunidade LGBTQIA+ ou é Terian? (responda apenas com 's' ou 'n')",
    "Qual a sua idade?",
    "Quem é o GOAT (melhor jogador) do basquete? (responda com A, B, C ou D)\na) Kobe Bryant\nb) LeBron James\nc) Jim Carrey\nd) Rodrigo Faro",
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
            "Responda com sinceridade. Envie cada resposta separadamente após a pergunta aparecer.\n" \
            "Você tem 2 minutos para resopnder, caso contrario sera expulso."
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

            # Validação da primeira pergunta (banimento)
            if i == 0 and resposta not in ["n", "nao", "não", "n!", "nao!", "não!"]:
                await member.send("❌ Você foi banido do servidor com base na resposta à primeira pergunta. \n https://tenor.com/view/xd-fani-gif-24750348")
                await member.ban(reason="Resposta afirmativa à pergunta 1 do questionário.")
                return

            # Validação da pergunta 2 (idade)
            if i == 1:
                if not resposta.isdigit() or len(resposta) > 2:
                    await member.send("Apenas sua idade, amigão.")
                    continue  # repete a mesma pergunta
                idade = int(resposta)
                if idade < 17:
                    await member.send("❌ Você deve ter pelo menos 17 anos para entrar no servidor. Você será removido.")
                    await member.kick(reason="Idade menor que 17.")
                    return

            # Validação da pergunta 3 (GOAT)
            if i == 2 and resposta not in ['a', 'b', 'c', 'd']:
                await member.send("❌ Resposta inválida para a pergunta 3. Use apenas: a, b, c ou d.")
                continue  # repete a mesma pergunta

            respostas.append(resposta)
            i += 1  # só avança se resposta for válida

        # Salvar respostas no CSV
        with open("respostas_questionario.csv", "a", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([member.name, member.id] + respostas)

        # Enviar para canal de logs
        canal_logs = bot.get_channel(ID_CANAL_LOG)
        if canal_logs:
            texto = f"📋 Novo questionário respondido por {member.mention}:\n"
            for idx, (pergunta, resposta) in enumerate(zip(perguntas, respostas), start=1):
                pergunta_curta = re.sub(r"\\s+", " ", pergunta.split('\n')[0].strip())
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

bot.run(TOKEN)
