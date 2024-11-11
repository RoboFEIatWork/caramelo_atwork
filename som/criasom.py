from gtts import gTTS
import os
from playsound import playsound

def gerar_audio_nomes(lista_nomes):
    # Itera sobre a lista de nomes
    for nome in lista_nomes:
        # Cria a frase que será falada
        frase = f"{nome}"
        
        # Gera o arquivo de áudio com o nome da pessoa
        tts = gTTS(text=frase, lang='pt')  # 'pt' para português
        nome_arquivo = f"{nome}.mp3"  # O arquivo será salvo com o nome da pessoa
        tts.save(nome_arquivo)
        print(f"Áudio gerado para {nome} em {nome_arquivo}")

# Exemplo de lista de nomes
lista_nomes = ["Allen Key", "Axis2", "Bearing2", "Drill","Wrench", "Spacer", "Screwdriver", "Motor2","M30", "M20", "Housing","Small Aluminium Profile Blacl", "Small Aluminium Profile Gray", "Large Aluminium Profile Black", "Large Aluminium Profile Gray",]

# Gera os arquivos de áudio
gerar_audio_nomes(lista_nomes)

# Reproduz o áudio (opcional)
playsound("Allen Key.mp3")
