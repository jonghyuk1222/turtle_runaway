import tkinter as tk
import turtle, random, time

class RunawayGame:
    def __init__(self, canvas, runner, chaser, hunter, catch_radius=30):
        self.canvas = canvas
        self.runner = runner
        self.chaser = chaser
        self.hunter = hunter
        self.catch_radius2 = catch_radius**2
        self.game_is_over = False

        self.runner.shape('turtle')
        self.runner.color('blue')
        self.runner.penup()

        self.chaser.shape('turtle')
        self.chaser.color('red')
        self.chaser.penup()
        
        self.hunter.shape('turtle')
        self.hunter.color('green')
        self.hunter.penup()

        self.drawer = turtle.RawTurtle(canvas)
        self.drawer.hideturtle()
        self.drawer.penup()
        self.start_time = None
        self.score = 0

    def is_catch(self):
        p = self.runner.pos()
        q = self.chaser.pos()
        dx, dy = p[0] - q[0], p[1] - q[1]
        return dx**2 + dy**2 < self.catch_radius2
    
    def being_catched(self):
        p = self.chaser.pos()
        q = self.hunter.pos()
        dx, dy = p[0] - q[0], p[1] - q[1]
        return dx**2 + dy**2 < self.catch_radius2

    def start(self, init_dist=400, ai_timer_msec=100):
        self.runner.setpos((-init_dist / 2, 0))
        self.runner.setheading(0)
        self.chaser.setpos((+init_dist / 2, 0))
        self.chaser.setheading(180)

        self.ai_timer_msec = ai_timer_msec
        self.start_time = time.time()
        self.canvas.ontimer(self.step, self.ai_timer_msec)
        
    def catch(self):
        self.score += 1 
        self.drawer.undo()
        self.drawer.penup()
        self.drawer.setpos(-300, 300)
        self.drawer.write(f'경과한 시간: {time.time() - self.start_time:.2f} 초 \n 점수: {self.score}')
        
    def catched(self):
        self.score -= 1 
        self.drawer.undo()
        self.drawer.penup()
        self.drawer.setpos(-300, 300)
        self.drawer.write(f'경과한 시간: {time.time() - self.start_time:.2f} 초 \n 점수: {self.score}')

    def step(self):
        if self.game_is_over:
            return
        
        self.runner.run_ai(self.chaser.pos(), self.chaser.heading())
        self.chaser.run_ai(self.runner.pos(), self.runner.heading())
        self.hunter.run_ai(self.chaser.pos(), self.chaser.heading())
 
        if not (-350 <= self.runner.xcor() <= 350 and -350 <= self.runner.ycor() <= 350):
         self.runner.setpos(max(min(self.runner.xcor(), 350), -350), max(min(self.runner.ycor(), 350), -350))
        if not (-350 <= self.chaser.xcor() <= 350 and -350 <= self.chaser.ycor() <= 350):
         self.chaser.setpos(max(min(self.chaser.xcor(), 350), -350), max(min(self.chaser.ycor(), 350), -350))
        
        elapsed_time = time.time() - self.start_time
        
        if self.is_catch():
            self.catch()
            
        if self.being_catched():
            self.catched()
            
        self.drawer.undo()
        self.drawer.penup()
        self.drawer.setpos(-300, 300)
        self.drawer.write(f'경과한 시간: {elapsed_time:.2f} 초 \n 점수 : {self.score}')
        
        if not self.game_is_over:
            self.canvas.ontimer(self.step, self.ai_timer_msec)

    def game_over(self):
        self.game_is_over = True
        self.drawer.undo()
        self.drawer.penup()
        self.drawer.setpos(0,0)
        self.drawer.write(f'최종 점수: {self.score}', align='center', font=('Arial', 24, 'normal'))
        
        if self.score >= 20:
            message = 'WONDERFUL!!'
        elif self.score >= 15:
            message = 'GREAT!'
        elif self.score >= 10:
            message = 'GOOD!'
        elif self.score >= 5:
            message = 'Not Bad.'
        elif self.score >= 0:
            message = 'Hmm...'
        elif self.score >= -10:
            message = 'Bad...'
        else:
            message = 'VERY BAD!!!'

        self.drawer.setpos(0, -50)
        self.drawer.write(message, align='center', font=('Arial', 24, 'normal'))
        
        self.drawer.setpos(0, -100)

class ManualMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=30):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

        canvas.onkeypress(lambda: self.forward(self.step_move), 'Up')
        canvas.onkeypress(lambda: self.backward(self.step_move), 'Down')
        canvas.onkeypress(lambda: self.left(self.step_turn), 'Left')
        canvas.onkeypress(lambda: self.right(self.step_turn), 'Right')
        canvas.listen()
    
    def run_ai(self, opp_pos, opp_heading):
        pass

class RandomMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=50, step_turn=50):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

    def run_ai(self, opp_pos, opp_heading):
        mode = random.randint(0, 2)
        if mode == 0:
            self.forward(self.step_move)
        elif mode == 1:
            self.left(self.step_turn)
        elif mode == 2:
            self.right(self.step_turn)
            
class HuntMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=20, step_turn=50):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn
        
    def run_ai(self, opp_pos, opp_heading):
        angle = self.towards(opp_pos[0], opp_pos[1])
        self.setheading(angle)
        self.forward(self.step_move)          

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Turtle Runaway")
    canvas = tk.Canvas(root, width=700, height=700)
    canvas.pack()
    screen = turtle.TurtleScreen(canvas)
    screen.bgcolor("#D8FFDA")

    runner = RandomMover(screen)
    chaser = ManualMover(screen)
    hunter = HuntMover(screen)

    game = RunawayGame(screen, runner, chaser, hunter)
    game.start()
    
    screen.ontimer(game.game_over, 60000)
    
    screen.mainloop()
