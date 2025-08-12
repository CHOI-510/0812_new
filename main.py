# main.py

import rclpy
import threading

# 우리가 만든 클래스들을 가져옵니다.
from robot_manager import ROSARobotManager
from command_parser import CommandParser

def main():
    """ROSA 시스템의 메인 실행 함수"""

    # 1. ROS 2 시스템을 초기화합니다.
    rclpy.init()

    # 2. 로봇 매니저(관제탑) 객체를 생성합니다.
    #    이 객체가 생성되면서 ROS 노드가 되고, waypoint를 로딩하며, 토픽 구독을 시작합니다.
    robot_manager = ROSARobotManager()

    # 3. 명령어 해석기 객체를 생성하고, 로봇 매니저와 연결합니다.
    command_parser = CommandParser(robot_manager)
    
    # 4. 사용자 입력을 별도의 스레드에서 계속 받도록 처리합니다.
    def get_user_input():
        """사용자 입력을 받아 명령어 해석기로 전달하는 함수"""
        while True:
            try:
                command = input("명령어 입력 > ")
                if command:
                    command_parser.parse_command(command)
            except (KeyboardInterrupt, EOFError):
                print("\n입력 스레드를 종료합니다.")
                break

    input_thread = threading.Thread(target=get_user_input, daemon=True)
    input_thread.start()

    # 5. ROS 2 노드를 계속 실행하며 콜백 함수 등을 처리합니다. (메인 스레드)
    #    Ctrl+C 로 종료하기 전까지 여기서 계속 대기하게 됩니다.
    try:
        rclpy.spin(robot_manager)
    except KeyboardInterrupt:
        print("프로그램을 종료합니다.")
    finally:
        # 6. 종료 시 노드를 깔끔하게 정리합니다.
        robot_manager.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()