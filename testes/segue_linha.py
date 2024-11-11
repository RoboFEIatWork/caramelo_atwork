import cv2
import threading
import numpy as np
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import String

class RobotController(Node):
    def _init_(self):
        super()._init_('robot_controller')
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.timer_callback)  # 10Hz
        self.vel_msg = Twist()  # Inicia a mensagem de movimento
        self.cap = cv2.VideoCapture(1)  # Abertura da câmera
        self.points = [(249, 285), (344, 282), (431, 283)]  # Pontos a serem monitorados
        self.color_thread = threading.Thread(target=self.color_detection_thread)
        self.color_thread.start()

    def timer_callback(self):
        # Aqui você pode definir a lógica de movimento, que será chamada a cada ciclo do timer
        colors = self.color_detection_thread()
        if colors[0] >= [230, 235, 235] and colors[1] >= [0, 0, 230] and colors[2] >= [235, 235, 235]:
            self.vel_msg.linear.x = 0.5  # Avançar para frente
            self.vel_msg.angular.z = 0.0  # Parar de girar
        elif colors[0] >= [230, 235, 235] and colors[1] >= [0, 0, 230] and colors[2] >= [0, 0, 230]:
            self.vel_msg.linear.x = 0.0  # Parar de ir para frente
            self.vel_msg.angular.z = -0.5  # Girar para a direita
        elif colors[0] >= [0, 0, 235] and colors[1] >= [0, 0, 230] and colors[2] >= [230, 230, 230]:
            self.vel_msg.linear.x = 0.0  # Parar de ir para frente
            self.vel_msg.angular.z = 0.5  # Girar para a esquerda
        else:
            self.vel_msg.linear.x = 0.0  # Parar de ir para frente
            self.vel_msg.angular.z = 0.5  # Gira em busca de uma linha

        self.cmd_vel_pub.publish(self.vel_msg)

    def identify_colors(self, frame):
        colors = []
        for point in self.points:
            color = frame[point[1], point[0]]
            colors.append(color)
        print("Cores nos pontos:", ", ".join(f"{color}" for color in colors))
        return colors

    def detect_line_direction(self, frame, colors):
        for point in self.points:
            cv2.circle(frame, point, radius=5, color=(255, 255, 255), thickness=-1)
        return frame

    def color_detection_thread(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Falha ao capturar a imagem da câmera.")
                break

            # Identifica as cores nos pontos
            colors = self.identify_colors(frame)

            # Desenha os pontos na imagem
            frame_with_points = self.detect_line_direction(frame, colors)

            # Exibe a imagem
            cv2.imshow("Camera with Points", frame_with_points)

            # Sai ao pressionar 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
            return colors

    def run(self):
        # Roda a aplicação ROS2
        rclpy.spin(self)

def main():
    rclpy.init()
    robot_controller = RobotController()
    robot_controller.run()
    robot_controller.cap.release()
    cv2.destroyAllWindows()

if  '_name_' == '_main_':
    main()