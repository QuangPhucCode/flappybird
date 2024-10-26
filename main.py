# Các thư viện cần thiết cho main.
import pygame
import configs
import assets
from objects.background import Background
from objects.floor import Floor
from objects.column import Column
from objects.bird import Bird
from objects.gamestart import GameStart
from objects.gameover import GameOver
from objects.score import Score

pygame.init()

# Tạo cửa sổ cho game, tiêu đề vs icon.
screen = pygame.display.set_mode((configs.SCREEN_WIDTH, configs.SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')
icon = pygame.image.load('assets/icons/red_bird.png')
pygame.display.set_icon(icon)


clock = pygame.time.Clock()
column_create_event = pygame.USEREVENT
running  = True
gameover = False
gamestarted = False
score = 0
high_score = 0


assets.load_sprites()
assets.load_audios()


sprites = pygame.sprite.LayeredUpdates()

def create_sprites():
    # Chèn background.
    Background(0, sprites)
    Background(1, sprites)

    # Chèn Floor.
    Floor(0, sprites)
    Floor(1, sprites)

    
    return Bird(sprites), GameStart(sprites), Score(sprites)

bird, game_start, score = create_sprites()


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == column_create_event:
            Column(sprites)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not gamestarted and not gameover:
                gamestarted = True
                game_start.kill()
                pygame.time.set_timer(column_create_event, 1500)
            if event.key == pygame.K_ESCAPE and gameover:
                gameover = False
                gamestarted = False
                sprites.empty()
                bird, game_start, score = create_sprites()
            
    
        bird.handle_event(event)

    screen.fill(0)

    sprites.draw(screen)

    if gamestarted and not gameover:
        sprites.update()

    if bird.check_collision(sprites) and not gameover:
        gameover = True
        gamestarted = False
        game_Over = GameOver(sprites)
        pygame.time.set_timer(column_create_event, 0)
        assets.play_audios("hit")


    for sprite in sprites:
        if type(sprite) is Column and sprite.is_passed():
            score.value += 1
            assets.play_audios("point")
        
    pygame.display.flip()
    clock.tick(configs.FPS)  

pygame.quit()