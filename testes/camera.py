import cv2
from dt_apriltags import Detector

# Índice da câmera ZED
camera_index = 1

# Abre a câmera ZED
cap = cv2.VideoCapture(camera_index)

# Verifica se a câmera foi aberta corretamente
if not cap.isOpened():
    print("Erro: Não foi possível acessar a câmera.")
    exit()

# Configuração do detector de AprilTags
detector = Detector()

# Loop para capturar os frames
while True:
    # Captura o frame atual
    ret, frame = cap.read()

    # Verifica se o frame foi capturado com sucesso
    if not ret:
        print("Erro: Não foi possível capturar o frame.")
        break

    # Converte a imagem para escala de cinza
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detecta as AprilTags na imagem
    results = detector.detect(gray, estimate_tag_pose=False)

    # Desenha retângulos ao redor das tags detectadas
    for r in results:
        # Obtém os pontos das bordas da tag
        (ptA, ptB, ptC, ptD) = r.corners
        ptA = (int(ptA[0]), int(ptA[1]))
        ptB = (int(ptB[0]), int(ptB[1]))
        ptC = (int(ptC[0]), int(ptC[1]))
        ptD = (int(ptD[0]), int(ptD[1]))

        # Desenha as linhas para formar o retângulo
        cv2.line(frame, ptA, ptB, (0, 255, 0), 2)
        cv2.line(frame, ptB, ptC, (0, 255, 0), 2)
        cv2.line(frame, ptC, ptD, (0, 255, 0), 2)
        cv2.line(frame, ptD, ptA, (0, 255, 0), 2)

        # Desenha o centro da tag
        (cX, cY) = (int(r.center[0]), int(r.center[1]))
        cv2.circle(frame, (cX, cY), 5, (0, 0, 255), -1)

        # Exibe o ID da tag detectada
        tag_id = r.tag_id
        cv2.putText(frame, f"ID: {tag_id}", (cX, cY - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Mostra o frame com as deteções
    cv2.imshow("Detecção de AprilTags", frame)

    # Sai do loop se a tecla 'q' for pressionada
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera a câmera e fecha as janelas
cap.release()
cv2.destroyAllWindows()