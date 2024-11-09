import cv2

# Configura o índice da câmera USB (0, 1, 2, etc.)
# Normalmente, 0 é a câmera principal, e 1 ou mais para outras câmeras conectadas.
camera_index = 0
 # Ajuste para o índice da sua câmera USB

# Inicia a captura de vídeo a partir da câmera USB
cap = cv2.VideoCapture(camera_index)

if not cap.isOpened():
    print("Erro ao abrir a câmera.")
    exit()

# Janela para mostrar o vídeo da câmera
cv2.namedWindow("Câmera USB", cv2.WINDOW_NORMAL)

while True:
    # Lê o frame da câmera
    ret, frame = cap.read()

    # Verifica se o frame foi capturado corretamente
    if not ret:
        print("Erro ao capturar o frame.")
        break

    # Exibe o frame na janela
    cv2.imshow("Câmera USB", frame)

    # Sai do loop ao pressionar 'ESC'
    if cv2.waitKey(1) == 27:  # 27 é o código para a tecla ESC
        break

# Libera a câmera e fecha as janelas
cap.release()
cv2.destroyAllWindows()
