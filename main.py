
import discord
import os
from dotenv import load_dotenv
import random

load_dotenv()
TOKEN = os.getenv('TOKEN')
funcionalidade_servidor = 'Um Novo Sol'
lista_comandos = {
    '$ping': 'Rebate',
    '$item-descricao': 'Este comando irá buscar os detalhes do item desejado na quinta edição do sistema D&D',
    '$2d6': 'Comando utilizado para rolar dados, podendo colocar quantos dados deseja rolar e quantos lados os dados terão',
    '$2d6+5': 'Comando utilizado para rolar dados com uma soma',
    '$codigo': 'Este comando exibe o link para meu código fonte, fique livre para clonar ou contribuir para esse projeto !'
}

class KnowLow(discord.Client):
    
    async def on_ready(self):
        print(f'{client.user.name} has connected to Discord!')

    async def on_member_join(member):
        await member.create_dm()
        await member.dm_channel.send(
            f'Olá {member.name}, seja bem vindo e boa sorte na sua jornada de {funcionalidade_servidor}! Para saber mais informações sobre mim, basta digitar: $KnowLow'
        )

    async def on_message(self, message):

        if message.author == self.user:
            return

        if str(message.channel) == 'know-low':
            await self.comandos_know_low(message)

        elif str(message.channel) == 'rolagem':
            await self.comandos_rolagem(message)
        else:
            await self.avisos_canais_nao_permitidos(message)



    async def avisos_canais_nao_permitidos(self, message):
        if self._verificaComandoDados(message):
            await message.channel.send('Não é permitido usar comandos do bot nesse canal, utilize o canal de texto "rolagem"')

        elif message.content.startswith('$'):
            await message.channel.send('Não é permitido usar comandos do bot nesse canal, utilize o canal de texto "Know-low"')

    def _verificaComandoDados(self, message):
        return message.content.lower().startswith('$d') or type(message.content.lower().split('$')[1].split('d')[0])  == int
            


    async def comandos_know_low(self, message):
        #await self.avisos_canais_nao_permitidos(message)

        if message.content == '$ping':
            await message.channel.send('pong')
        elif message.content == '$KnowLow':
            await message.channel.send('Olá, meu nome é Know Low, meu criador é Vinícius Góes, tenho como objetivo te ajudar a encontrar o preço das coisas mais baratas possíveis mas também funciono como um bot de dados, utilize o comando: "$comandos" para saber mais')
        elif message.content == '$comandos': 
            resposta = "Comandos disponíveis:\n\n"
            resposta += "\n".join([f"{comando}: {descricao}" for comando, descricao in lista_comandos.items()])
            await message.channel.send(resposta)
        elif message.content == '$codigo':
            await message.channel.send('https://github.com/vgoes19/Bot-Discord')
        elif '$item' in message.content:
            await self.busca_item(message)
            


    async def busca_item(self, message):
        print('entrou em funcao de busca item')
        await message.channel.send('entrou em comando de busca de item')

    async def comandos_rolagem(self, message):

        resultado_final_somado = 0
        mensagem_retorno = ""

        content_lower = message.content.lower()
        content_parts = content_lower.split('$')[1].split('d')

        qtd_dados = int(content_parts[0]) if content_parts[0] else 1
        tipo_dados = int(content_parts[1].split('+')[0])
        dados_resultado = []

        if '+' in content_lower:
            soma = int(content_lower.split('+')[1])
            for _ in range(qtd_dados):
                resultado = random.randint(1, tipo_dados)
                dados_resultado.append(resultado)
                resultado_final_somado += resultado

            resultado_final_somado += soma
            mensagem_retorno = f'Dados: {dados_resultado} + {soma} = {resultado_final_somado}'
        else:
            for _ in range(qtd_dados):
                resultado = random.randint(1, tipo_dados)
                dados_resultado.append(resultado)
                resultado_final_somado += resultado

            mensagem_retorno = f'Dados: {dados_resultado} = {resultado_final_somado}'

        await message.channel.send(mensagem_retorno)
   


intents = discord.Intents.default()
intents.message_content = True
client = KnowLow(intents=intents)
client.run(TOKEN)