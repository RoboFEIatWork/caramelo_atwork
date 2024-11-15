#!/usr/bin/env python3
import os
from argparse import ArgumentParser
import cv2
import apriltag
import time
from dynamixel_sdk import *  

# Configura a variável de ambiente para usar o backend X11
os.environ["QT_QPA_PLATFORM"] = "xcb"

class DynamixelMotor:
    def __init__(self, motor_id, port_handler):
        self.motor_id = motor_id
        self.port_handler = port_handler
        self.packet_handler = PacketHandler(2.0)
        self.ADDR_TORQUE_ENABLE = 64
        self.ADDR_GOAL_POSITION = 116
        self.ADDR_PRESENT_POSITION = 132
        self.ADDR_GOAL_VELOCITY = 104
        self.ADDR_PRESENT_VELOCITY = 128
        self.ADDR_PROFILE_ACCELERATION = 108
        self.ADDR_PROFILE_VELOCITY = 112

    def enable_torque(self):
        result, error = self.packet_handler.write1ByteTxRx(self.port_handler, self.motor_id, self.ADDR_TORQUE_ENABLE, 1)
        if result != COMM_SUCCESS:
            print(f"Erro ao habilitar torque no motor {self.motor_id}: {self.packet_handler.getTxRxResult(result)}")
            return False
        return True

    def disable_torque(self):
        result, error = self.packet_handler.write1ByteTxRx(self.port_handler, self.motor_id, self.ADDR_TORQUE_ENABLE, 0)
        if result != COMM_SUCCESS:
            print(f"Erro ao desabilitar torque no motor {self.motor_id}: {self.packet_handler.getTxRxResult(result)}")
            return False
        return True

    def set_goal_position(self, position):
        result, error = self.packet_handler.write4ByteTxRx(self.port_handler, self.motor_id, self.ADDR_GOAL_POSITION, position)
        if result != COMM_SUCCESS:
            print(f"Erro ao definir posição no motor {self.motor_id}: {self.packet_handler.getTxRxResult(result)}")
            return

        # Monitoramento da posição atual
        attempts = 0
        while attempts < 200:  # Limita o número de tentativas para evitar loop infinito
            present_position, _, error = self.packet_handler.read4ByteTxRx(self.port_handler, self.motor_id, self.ADDR_PRESENT_POSITION)
            if error != 0:
                print(f"Erro ao ler posição: {self.packet_handler.getRxPacketError(error)}")
                break
            print(f"Posição Atual: {present_position}")

            if abs(position - present_position) < 20:
                print(f"Alcançou a posição {position}")
                break
            time.sleep(0.1)
            attempts += 1
        if attempts == 200:
            print(f"Limite de tentativas alcançado. Posição não foi alcançada.")

    def set_profile(self, acceleration, velocity):
        # Define o perfil de aceleração
        result, error = self.packet_handler.write4ByteTxRx(self.port_handler, self.motor_id, self.ADDR_PROFILE_ACCELERATION, acceleration)
        if result != COMM_SUCCESS:
            print(f"Erro ao definir aceleração no motor {self.motor_id}: {self.packet_handler.getTxRxResult(result)}")
            return

        # Define o perfil de velocidade
        result, error = self.packet_handler.write4ByteTxRx(self.port_handler, self.motor_id, self.ADDR_PROFILE_VELOCITY, velocity)
        if result != COMM_SUCCESS:
            print(f"Erro ao definir velocidade no motor {self.motor_id}: {self.packet_handler.getTxRxResult(result)}")
            return
    
    def move_slow(self, goal_position):
        # Definir uma aceleração muito baixa e uma velocidade mínima
        min_velocity = 30      # Valor mínimo para a velocidade
        min_acceleration = 10   # Valor baixo para aceleração

        # Definir o perfil de movimento com aceleração e velocidade baixas
        self.set_profile(min_acceleration, min_velocity)

        # Movimentar o motor para a posição desejada com a menor velocidade possível
        self.set_goal_position(goal_position)

def main():
    parser = ArgumentParser(description='Test Apriltag Python bindings')
    parser.add_argument('device_or_movie', metavar='INPUT', nargs='?', default=0, help='Movie to load or integer ID of camera device')
    apriltag.add_arguments(parser)
    options = parser.parse_args()

    # Garantir que device_or_movie seja tratado como string antes de usar isdigit()
    device_or_movie = str(options.device_or_movie)

    try:
        # Abrindo a câmera
        if device_or_movie.isdigit():
            cap = cv2.VideoCapture(int(device_or_movie))
        else:
            cap = cv2.VideoCapture(device_or_movie)

        window = 'Camera'
        cv2.namedWindow(window)

        detector = apriltag.Detector(options)

        # Inicializar port_handler
        port_handler = PortHandler(r'/dev/ttyUSB2')
        if not port_handler.openPort():
            raise Exception("Não foi possível abrir a porta.")
        if not port_handler.setBaudRate(1000000):
            raise Exception("Não foi possível configurar a taxa de baud.")
        
        print("Porta aberta com sucesso.")

        # Criar motores
        motores = [DynamixelMotor(motor_id=i, port_handler=port_handler) for i in range(1, 7)]

        # Habilitar torque
        for motor in motores:
            motor.enable_torque()
        print("Torque habilitado com sucesso em todos os motores.")

        # Loop de detecção e movimento
        while True:
            success, frame = cap.read()
            if not success:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            detections, dimg = detector.detect(gray, return_image=True)

            num_detections = len(detections)
            print(f'Detected {num_detections} tags.\n')

            for i, detection in enumerate(detections):
                print(f'Detection {i + 1} of {num_detections}:')
                print(detection.tostring(indent=2))
                print()

            overlay = frame // 2 + dimg[:, :, None] // 2
            cv2.imshow(window, overlay)

            k = cv2.waitKey(1)
            if k == 27:  # Press 'ESC' to exit
                break

        # Desabilitar torque após o movimento
        for motor in motores:
            motor.disable_torque()
        print("Torque desabilitado em todos os motores.")

    except Exception as e:
        print(f"Erro: {str(e)}")
    finally:
        # Fechar porta
        if port_handler and port_handler.is_open:
            port_handler.closePort()
            print("Comunicação com a porta finalizada.")
        if cap.isOpened():
            cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
