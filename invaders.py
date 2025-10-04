#Ethan's Alien Invaders

import random
import time
import turtle
import os
import sys

FRAME_RATE = 30 
TIME_FOR_1_FRAME = 1 / FRAME_RATE  
CANNON_STEP = 10
LASER_LENGTH = 20
LASER_SPEED = 20
PLAYER_SHOT_COOLDOWN = 1.0 
ALIEN_SPAWN_INTERVAL = 1.5 
ALIEN_SPEED = 3
ALIEN_H_STEP = 10
ALIEN_MOVE_INTERVAL = 0.5
ALIEN_MIN_MOVE_INTERVAL = 0.08
ALIEN_DROP = 25
ALIEN_SIZE = 2.8
ALIEN_HALF_WIDTH = ALIEN_SIZE * 10
ALIEN_ALIGNMENT_THRESHOLD = 30  
ALIEN_SPEED_EXPONENT = 2.0  
ALIEN_SHOOT_INTERVAL_BASE = 2.0  
ALIEN_SHOOT_JITTER = 1.2
ALIEN_LASER_SPEED = 14
ALIEN_LASER_LENGTH = 20


window = turtle.Screen()
window.tracer(0)
window.setup(0.5, 0.75)
window.bgcolor(0.2, 0.2, 0.2)
window.title("Ethan's Alien Invaders")

LEFT = -window.window_width() / 2
RIGHT = window.window_width() / 2
TOP = window.window_height() / 2
BOTTOM = -window.window_height() / 2
FLOOR_LEVEL = 0.9 * BOTTOM
GUTTER = 0.025 * window.window_width()

cannon = turtle.Turtle()
cannon.penup()
cannon.color(1, 1, 1)
cannon.shape("square")
cannon.setposition(0, FLOOR_LEVEL)
cannon.cannon_movement = 0 

text = turtle.Turtle()
text.penup()
text.hideturtle()
text.setposition(LEFT * 0.8, TOP * 0.8)
text.color(1, 1, 1)

lasers = []
aliens = []
alien_direction = 1 
last_alien_move_time = 0
alien_lasers = []
last_alien_shot_time = 0

next_alien_shot_interval = random.uniform(
    max(0.1, ALIEN_SHOOT_INTERVAL_BASE - ALIEN_SHOOT_JITTER),
    ALIEN_SHOOT_INTERVAL_BASE + ALIEN_SHOOT_JITTER,
)
initial_aliens_count = 0
last_player_shot_time = 0

def draw_cannon():
    cannon.clear()
    cannon.turtlesize(1, 4)
    cannon.stamp()
    cannon.sety(FLOOR_LEVEL + 10)
    cannon.turtlesize(1, 1.5)
    cannon.stamp()
    cannon.sety(FLOOR_LEVEL + 20)
    cannon.turtlesize(0.8, 0.3)  
    cannon.stamp()
    cannon.sety(FLOOR_LEVEL)

def move_left():
    cannon.cannon_movement = -1

def move_right():
    cannon.cannon_movement = 1

def stop_cannon_movement():
    cannon.cannon_movement = 0

def create_laser():
    global last_player_shot_time
 
    if time.time() - last_player_shot_time < PLAYER_SHOT_COOLDOWN:
        return
    laser = turtle.Turtle()
    laser.penup()
    laser.color(1, 0, 0)
    laser.hideturtle()
    laser.setposition(cannon.xcor(), cannon.ycor())
    laser.setheading(90)
    laser.forward(20)
    laser.pendown()
    laser.pensize(5)

    lasers.append(laser)
    last_player_shot_time = time.time()

def move_laser(laser):
    laser.clear()
    laser.forward(LASER_SPEED)
    laser.forward(LASER_LENGTH)
    laser.forward(-LASER_LENGTH)

def create_alien():
    alien = turtle.Turtle()
    alien.penup()
    alien.turtlesize(ALIEN_SIZE)
    alien.setposition(
        random.randint(
            int(LEFT + GUTTER),
            int(RIGHT - GUTTER),
        ),
        TOP,
    )
    alien.shape("arrow")
    alien.setheading(-90)
    alien.color(random.random(), random.random(), random.random())
    aliens.append(alien)

def create_alien_grid(rows=3, cols=8, x_spacing=60, y_spacing=40):
    start_x = -((cols - 1) * x_spacing) / 2
    start_y = TOP - 50
    for r in range(rows):
        for c in range(cols):
            alien = turtle.Turtle()
            alien.penup()
            alien.turtlesize(ALIEN_SIZE)
            alien.setposition(start_x + c * x_spacing, start_y - r * y_spacing)
            alien.shape("arrow")
            alien.setheading(-90)
            alien.color(random.random(), random.random(), random.random())
            aliens.append(alien)

def remove_sprite(sprite, sprite_list):
    sprite.clear()
    sprite.hideturtle()
    window.update()
    sprite_list.remove(sprite)
    turtle.turtles().remove(sprite)

def create_alien_laser(x, y):
    laser = turtle.Turtle()
    laser.penup()
    laser.color(1, 0.6, 0)
    laser.hideturtle()
    laser.setposition(x, y)
    laser.setheading(-90)
    laser.pendown()
    laser.pensize(6)
    alien_lasers.append(laser)


def move_alien_laser(laser):
    laser.clear()
    laser.forward(ALIEN_LASER_SPEED)
    laser.forward(ALIEN_LASER_LENGTH)
    laser.forward(-ALIEN_LASER_LENGTH)

window.onkeypress(move_left, "Left")
window.onkeypress(move_right, "Right")
window.onkeyrelease(stop_cannon_movement, "Left")
window.onkeyrelease(stop_cannon_movement, "Right")
window.onkeypress(create_laser, "space")
window.onkeypress(turtle.bye, "q")
window.listen()

draw_cannon()

create_alien_grid(rows=4, cols=8, x_spacing=90, y_spacing=70)

initial_aliens_count = len(aliens)

alien_timer = 0
game_timer = time.time()
score = 0
game_running = True
game_won = False
TIME_BONUS = 5
TIME_BONUS_INTERVAL = 60.0
last_time_bonus = time.time()
per_alien_extra = 0
previous_move_interval = ALIEN_MOVE_INTERVAL
while game_running:
    timer_this_frame = time.time()

    time_elapsed = time.time() - game_timer
    if time.time() - last_time_bonus >= TIME_BONUS_INTERVAL:
        score += TIME_BONUS
        last_time_bonus = time.time()
    text.clear()
    text.write(
        f"Time: {time_elapsed:5.1f}s\nScore: {score:5}",
        font=("Courier", 20, "bold"),
    )
    new_x = cannon.xcor() + CANNON_STEP * cannon.cannon_movement
    if LEFT + GUTTER <= new_x <= RIGHT - GUTTER:
        cannon.setx(new_x)
        draw_cannon()

    for laser in lasers.copy():
        move_laser(laser)
        if laser.ycor() > TOP:
            remove_sprite(laser, lasers)
            continue
        for alien in aliens.copy():
            if laser.distance(alien) < 20:
                remove_sprite(laser, lasers)
                try:
                    old_color = alien.color()
                    alien.color(1, 0, 0)
                    window.update()
                    time.sleep(0.06)
                    alien.color(old_color)
                except Exception:
                    pass
                remove_sprite(alien, aliens)
                score += 10 + per_alien_extra
                if not aliens:
                    game_won = True
                    game_running = False
                break

    if initial_aliens_count > 0:
        alive_fraction = max(0.01, len(aliens) / initial_aliens_count)
        dynamic_move_interval = max(
            ALIEN_MIN_MOVE_INTERVAL, ALIEN_MOVE_INTERVAL * (alive_fraction ** ALIEN_SPEED_EXPONENT)
        )
    try:
        if dynamic_move_interval < previous_move_interval:
            per_alien_extra += 5
            previous_move_interval = dynamic_move_interval
    except NameError:
        previous_move_interval = dynamic_move_interval
        per_alien_extra = 0
    else:
        dynamic_move_interval = ALIEN_MOVE_INTERVAL

    if time.time() - last_alien_move_time > dynamic_move_interval:
        min_x = min((a.xcor() for a in aliens), default=0)
        max_x = max((a.xcor() for a in aliens), default=0)
        will_hit_right = (max_x + ALIEN_H_STEP * alien_direction + ALIEN_HALF_WIDTH) > (RIGHT - GUTTER)
        will_hit_left = (min_x + ALIEN_H_STEP * alien_direction - ALIEN_HALF_WIDTH) < (LEFT + GUTTER)
        if (alien_direction == 1 and will_hit_right) or (alien_direction == -1 and will_hit_left):
            for a in aliens:
                a.sety(a.ycor() - ALIEN_DROP)
                if a.ycor() < FLOOR_LEVEL:
                    game_running = False
            alien_direction *= -1
        else:
            for a in aliens:
                a.setx(a.xcor() + ALIEN_H_STEP * alien_direction)

        last_alien_move_time = time.time()

    if time.time() - last_alien_shot_time > next_alien_shot_interval and aliens:
        aligned = [a for a in aliens if abs(a.xcor() - cannon.xcor()) < ALIEN_ALIGNMENT_THRESHOLD]
        if aligned and random.random() < 0.8:
            shooter = random.choice(aligned)
        else:
            shooter = random.choice(aliens)
        create_alien_laser(shooter.xcor(), shooter.ycor() - 10)
        last_alien_shot_time = time.time()
        next_alien_shot_interval = random.uniform(
            max(0.1, ALIEN_SHOOT_INTERVAL_BASE - ALIEN_SHOOT_JITTER),
            ALIEN_SHOOT_INTERVAL_BASE + ALIEN_SHOOT_JITTER,
        )

    for alat in alien_lasers.copy():
        move_alien_laser(alat)
        if alat.ycor() < BOTTOM:
            remove_sprite(alat, alien_lasers)
            continue
        if alat.distance(cannon) < 20:
            remove_sprite(alat, alien_lasers)
            try:
                old_color = cannon.color()
                cannon.color(1, 0, 0)
                draw_cannon()
                window.update()
                time.sleep(0.12)
                cannon.color(old_color)
                draw_cannon()
            except Exception:
                pass
            game_running = False
            break

    for alien in aliens:
        if alien.ycor() < FLOOR_LEVEL:
            game_running = False
            break

    if not aliens:
        game_won = True
        game_running = False
        break

    time_for_this_frame = time.time() - timer_this_frame
    if time_for_this_frame < TIME_FOR_1_FRAME:
        time.sleep(TIME_FOR_1_FRAME - time_for_this_frame)
    window.update()

splash_text = turtle.Turtle()
splash_text.hideturtle()
splash_text.color(1, 1, 1)
t = globals().get('game_won', False)
if t:
    splash_text.write("YOU WON!", font=("Courier", 40, "bold"), align="center")
else:
    splash_text.write("GAME OVER", font=("Courier", 40, "bold"), align="center")
splash_text.sety(splash_text.ycor() - 40)
splash_text.write("Press 'R' to restart", font=("Courier", 18, "normal"), align="center")


def restart_game():
    python = sys.executable
    os.execl(python, python, *sys.argv)

window.onkeypress(restart_game, "r")
window.listen()
turtle.done()
