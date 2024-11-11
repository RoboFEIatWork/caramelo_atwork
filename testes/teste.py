#!/usr/bin/env python3

from argparse import ArgumentParser
import cv2
import apriltag
from playsound import playsound
import os
from gtts import gTTS
import time

# Mapeamento de IDs de tags para nomes de ferramentas e peças
tag_to_name = {
    1: "Small Aluminium Profile Black",
    2: "Small Aluminium Profile Gray",
    3: "Large Aluminium Profile Black",
    4: "Large Aluminium Profile Gray",
    6: "M20",
    7: "M30",
    20: "Axis2",
    21: "Bearing2",
    22: "Housing",
    23: "Motor2",
    24: "Spacer",
    25: "Wrench",
    26: "Drill",
    28: "Allen Key"
}

# Função para gerar áudio se não existir
def gerar_audio(nome):
    diretorio_audio = "./audios"
    os.makedirs(diretorio_audio, exist_ok=True)
    caminho_arquivo = os.path.join(diretorio_audio, f"{nome}.mp3")

    # Se o arquivo não existe, cria-o
    if not os.path.exists(caminho_arquivo):
        frase = f"Detectado: {nome}"
        tts = gTTS(text=frase, lang='pt')
        tts.save(caminho_arquivo)
    return caminho_arquivo

def main():
    parser = ArgumentParser(description='AprilTag detector with audio feedback.')
    parser.add_argument('device_or_movie', metavar='INPUT', nargs='?', default=0,
                        help='Movie to load or integer ID of camera device')
    apriltag.add_arguments(parser)
    options = parser.parse_args()

    try:
        cap = cv2.VideoCapture(int(options.device_or_movie))
    except ValueError:
        cap = cv2.VideoCapture(options.device_or_movie)

    window = 'Camera'
    cv2.namedWindow(window)

    detector = apriltag.Detector(options)
    last_detection_time = 0  # Armazena o horário da última detecção válida

    while True:
        success, frame = cap.read()
        if not success:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        detections, dimg = detector.detect(gray, return_image=True)

        num_detections = len(detections)
        print(f'Detected {num_detections} tags.\n')

        for detection in detections:
            tag_id = detection.tag_id
            print(f"Tag ID detectada: {tag_id}")

            # Verifica se a tag ID está no mapeamento
            if tag_id in tag_to_name:
                current_time = time.time()
                # Só executa o áudio se passaram 5 segundos desde a última detecção válida
                if current_time - last_detection_time >= 5:
                    nome_ferramenta = tag_to_name[tag_id]
                    print(f"Ferramenta ou peça detectada: {nome_ferramenta}")
                    
                    # Gera ou localiza o áudio correspondente
                    caminho_audio = gerar_audio(nome_ferramenta)
                    
                    # Toca o áudio
                    playsound(caminho_audio)
                    
                    # Atualiza o horário da última detecção válida
                    last_detection_time = current_time
            else:
                print("Tag ID não mapeada.")

        overlay = frame // 2 + dimg[:, :, None] // 2
        cv2.imshow(window, overlay)
        k = cv2.waitKey(1)

        if k == 27:  # Press 'ESC' to exit
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
