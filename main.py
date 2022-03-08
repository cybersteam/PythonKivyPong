#__version__ = “1.0.0”

#currently uses python 3.5
# https://tecadmin.net/install-python-3-5-on-ubuntu/
#The tut
#https://www.youtube.com/watch?v=s3PZykOo2uo&list=PLhTjy8cBISEpobkPwLm71p5YNBzPH9m9V&index=2

#important path to remember - usr/lib/python3/dist-packages/kivy/

# axis are 0,0 - left to right is x top to bott is y

# App is the main module that is needed in kivy always
from kivy.app import App
# Widget is the basic UI building block it provides a canvas to draw to and it receives events and responds
from kivy.uix.widget import Widget
# ReferenceListProperty will automatically change the values of e.g x and y accordingly if they are NumericProperty's
# Using NumericProperty specifies the value as an integer - this is because android(java)and iphone(c++) need to know...
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
# The Vector represents a 2D vector (x, y)
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint

class PongPaddle(Widget):
    score = NumericProperty(0)
    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            ball.velocity_x *= -1.1


class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

class PongGame(Widget):
    # this tells java etc. that this is an object..
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)
    # this is where the velocities actually get values
    def serve_ball(self):
        # passing x,y coordinates into the ball object as well as random rotation
        self.ball.velocity = Vector(4,0).rotate(randint(0, 360))
    # whatever needs to update goes in here
    def update(self, timeframes):
        # passing in the move method from PongBall
        self.ball.move()
        # bounce off sides and topbott and increase score
        # the -50 is because the ball itself is 50px and bounces when the left and top of ball reaches side..
        if (self.ball.y < 0) or (self.ball.y > self.height -50):
            self.ball.velocity_y *= -1

        if self.ball.x < 0:
            self.ball.velocity_x *= -1
            self.player1.score += 1
        if self.ball.x > self.width - 50:
            self.ball.velocity_x *= -1
            self.player2.score += 1

        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)


    def on_touch_move(self, touch):
        if touch.x < self.width / 1/4:
            self.player1.center_y = touch.y
        if touch.x > self.width * 3/4:
            self.player2.center_y = touch.y

class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        # using the Clock class, schedule_interval method passed into our "game" obj - in 1 sec 60 frames happen
        # the update fucntion gets called 60 times per second...
        Clock.schedule_interval(game.update,1.0/60.0)
        return game

# instantiate the app as mygame
mygame = PongApp()
#
if __name__ == '__main__' :
    mygame.run()
