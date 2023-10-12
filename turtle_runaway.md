# turtle_runaway
Turtle Runaway Game

🔵Runner(Blue Turtle) : 임의의 방향으로 계속해서 빠르게 이동

🔴Chaser(Red Turtle) : 키보드의 화살표 키로 조작

🟢Hunter(Green Turtle) : Chaser을 향해 느리게 이동

Runaway 클래스:

  __init__ : Turtle, time, score 등의 초기 설정
  
  is_catch, being_catched : chaser가 runner의 일정 범위 내에 있는지, hunter가 chaser의 일정 범위 내에 있는지 확인
  
  start : 게임이 시작될 때 거북이들의 위치, 시간 시작 등 설정
  
  catch, catched : chaser가 runner를 잡았을 때 1점씩 추가, hunter가 chaser을 잡았을 때 1점씩 감소
  
  step : 각 Turtle에게 움직임을 적용, Turtle이 화면 밖을 벗어나지 않게 움직임의 범위를 제한, 경과한 시간을 측정하고 표시
  
  game_over : 정해진 시간이 다 되었을때 시간을 멈추고 최종 점수와 결과를 출력

ManualMover 클래스 : 화살표 버튼을 눌렀을 때 일정 방향만큼 고개를 돌리거나 움직이도록 함

RandomMover 클래스 : 임의의 방향으로 계속해서 움직이도록 함

HuntMover 클래스 : 지정한 방향(이 경우엔 Chaser의 위치)으로 계속해서 움직이도록 함

__main__ : 화면을 구성하고 게임이 진행될 시간을 설정
