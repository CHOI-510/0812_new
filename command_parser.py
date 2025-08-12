# command_parser.py

# 나중에 robot_manager 객체를 받아오기 위한 준비
# from robot_manager import ROSARobotManager 

class CommandParser:
    """사용자의 텍스트 명령을 분석하여 로봇 매니저에 전달하는 클래스입니다."""

    def __init__(self, robot_manager):
        # ROSARobotManager 객체를 직접 참조합니다.
        self.robot_manager = robot_manager
        print("✅ 명령어 해석기 준비 완료.")

    def parse_command(self, command: str):
        """명령어 문자열을 분석하여 적절한 함수를 호출합니다."""
        
        print(f"명령 수신: '{command}'")
        parts = command.split() # 공백을 기준으로 명령어를 단어들로 분리

        if len(parts) < 2:
            print("❌ 명령이 너무 짧습니다. (예: '3번 왼쪽방 가')")
            return

        # 1. 로봇 이름 찾기
        robot_name = None
        if "3번" in command:
            robot_name = "DP_03"
        elif "8번" in command:
            robot_name = "DP_08"
        elif "9번" in command:
            robot_name = "DP_09"

        if not robot_name:
            print("❌ 로봇 번호(3번, 8번, 9번)를 찾을 수 없습니다.")
            return

        # 2. 목적지 이름 찾기
        # self.robot_manager를 통해 waypoints 데이터에 접근
        destination_name = None
        available_destinations = [d['name'] for d in self.robot_manager.waypoints['destinations']]
        
        for part in parts:
            if part in available_destinations:
                destination_name = part
                break
        
        if not destination_name:
            print("❌ 목적지를 찾을 수 없습니다.")
            print(f"💡 사용 가능한 목적지: {', '.join(available_destinations)}")
            return
            
        # 3. 로봇 매니저의 함수 호출
        print(f"▶️ 실행: {robot_name} 로봇을 {destination_name}으로 이동시킵니다.")
        self.robot_manager.navigate_robot(robot_name, destination_name)

# ---- 여기까지만 작성 ----