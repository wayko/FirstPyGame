import pygame
import os
import json
pygame.font.init()
pygame.mixer.init()

data = {
    'yellow_wins':0,
    'red_wins' : 0
}

try:
    with open('PlayerStats.txt') as player_stats:
        data = json.load(player_stats)
except Exception as e:
    print("File not created yet")
   
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)
YELLOW_WIN_FONT = pygame.font.SysFont('comicsans', 20)
RED_WIN_FONT = pygame.font.SysFont('comicsans', 20)

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My First PyGame")

FPS = 60
VEL = 5
FILL = (255, 255, 255)

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55,40
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join(
    'Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE,(SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join(
    'Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(
        RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)
BORDER_COLOR = (0,0,0)
BULLET_VEL = 7
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))
MAX_BULLETS = 3
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2
RED = (255, 0 , 0)
YELLOW = (255, 255, 0)


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    print(data['yellow_wins'])
    pygame.draw.rect(WIN, BORDER_COLOR, BORDER)
    WIN.blit(SPACE, (0, 0))
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, FILL)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1 , FILL)
    red_wins_text = RED_WIN_FONT.render("Red's Total Wins: " + str(data['red_wins']), 1, FILL)
    yellow_wins_text = YELLOW_WIN_FONT.render("Yellow's Total Wins: "+ str(data['yellow_wins']), 1, FILL)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 30, 10))
    WIN.blit(red_wins_text, (WIDTH - red_wins_text.get_width() - 30, 80))
    WIN.blit(yellow_health_text, (10,10))
    WIN.blit(yellow_wins_text, (10,80))
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    
    pygame.display.update()

def yellow_handle_movement(keys_pressed, yellow):
     if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: #Left
        yellow.x -= VEL
     if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x: #Right
        yellow.x += VEL
     if keys_pressed[pygame.K_w] and yellow.y - 100 - VEL > 0: #Up
        yellow.y -= VEL
     if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15: #Down
        yellow.y += VEL

def red_handle_movement(keys_pressed, red):
     if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width: #Left
        red.x -= VEL
     if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH: #Right
        red.x += VEL
     if keys_pressed[pygame.K_UP] and red.y - 100 - VEL > 0: #Up
        red.y -= VEL
     if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15: #Down
        red.y += VEL
    

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, FILL)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red_bullets = []
    yellow_bullets = []
    red_health = 10
    yellow_health = 10
    clock = pygame.time.Clock()
    winner_text = ""
    while True:
        try:
            with open('PlayerStats.txt', 'w') as player_stats:
                json.dump(data,player_stats)
        except Exception as e:
            print("File not created yet")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               pygame.quit()
               break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()
        
        if red_health <= 0:
            draw_window(red, yellow, red_bullets, yellow_bullets, 0, yellow_health)
            winner_text = "Yellow Wins!"
            data['yellow_wins'] += 1
            
        if yellow_health <= 0:
            draw_window(red, yellow, red_bullets, yellow_bullets, red_health, 0)
            winner_text = "Red Wins!"
            data['red_wins'] += 1
        if winner_text !="":
            draw_winner(winner_text)
            break
        
        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)
        
        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)
        
    main()

if __name__ == "__main__":
    main()
