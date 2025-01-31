from turtledemo.nim import COLOR

import pygame
import random

# Inicialización de PyGame
pygame.init()
pygame.mixer.init()

# Colores
white = (255, 255, 255)
black = (0, 0, 0)
LightSalmon = (255, 160, 122)

# Configuración de pantalla
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pygame Game :)")
clock = pygame.time.Clock()

# Vista puntuacion
def draw_text(surface, text, size, x, y):
	font = pygame.font.SysFont("Arial", size)
	text_surface = font.render(text, True, (255, 255, 255))
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x, y)
	surface.blit(text_surface, text_rect)

def life_bar(surface, x, y, percentage):
	lenght_bar = 100
	height_bar = 10
	fill = (percentage / 100) * lenght_bar
	border = pygame.Rect(x, y, lenght_bar, height_bar)
	fill = pygame.Rect(x, y, fill, height_bar)
	pygame.draw.rect(surface, LightSalmon, fill)
	pygame.draw.rect(surface, white, border, 2)


#Carro
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/carro.png").convert()
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.centerx = width // 2
        self.rect.bottom = height - 10
        self.speed_x = 0
        self.life = 100

    def update(self):
        self.speed_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed_x = -5
        if keystate[pygame.K_RIGHT]:
            self.speed_x = 5
        self.rect.x += self.speed_x
        if self.rect.right > width:
            self.rect.right = height
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        tirar_sound.play()

#Enemigo
class Enemigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice(enemigo_img)
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(width - self.rect.width)
        self.rect.y = random.randrange(-160, -90)
        self.speedy = random.randrange(1, 10)
        self.speedx = random.randrange(-5, 5)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > height + 10 or self.rect.left < -30 or self.rect.right > width + 22:
            self.rect.x = random.randrange(width - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("assets/bala.png")
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

def menu_screen():
    draw_text(screen, "Pygame Game ;)", 65, width // 2, height / 4)
    draw_text(screen, "Instructions", 65, width // 2, height // 2)
    draw_text(screen, " Press key to begin", 65, width // 2, height * 3 / 4)

    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False


# Aleatorios las machas de aceite 'Enemigos' grandes, medianas, pequelas
enemigo_img = []
enmigo_list = ["assets/enemigo.png", "assets/enemigo2.png", "assets/enemigo3.png"]

for img in enmigo_list:
	enemigo_img.append(pygame.image.load(img).convert())


# Auidos
tirar_sound = pygame.mixer.Sound("assets/audios/tirar.mp3")
choque_sound = pygame.mixer.Sound("assets/audios/choque.mp3")
pygame.mixer.music.load("assets/audios/audioFondo.mp3")
pygame.mixer.music.set_volume(0.2)

# Fondo
background = pygame.image.load("assets/fondoo.png").convert()


# Musica de fondo
pygame.mixer.music.play(loops= -1)

# Game over
game_over =  True

# Bucle - Procesando los eventos
running = True
while running:
    if game_over:
        game_over = False
        menu_screen()
        # Listas
        all_sprites = pygame.sprite.Group()
        enemigo_list = pygame.sprite.Group()
        bullets = pygame.sprite.Group()

        player = Player()
        all_sprites.add(player)

        for i in range(8):
            enemigo = Enemigo()
            all_sprites.add(enemigo)
            enemigo_list.add(enemigo)
        score = 0

    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Actualizar coliciones
    all_sprites.update()
    hits = pygame.sprite.groupcollide(enemigo_list, bullets, True, True)
    for hit in hits:
        score += 10
        choque_sound.play()
        enemigo = Enemigo()
        all_sprites.add(enemigo)
        enemigo_list.add(enemigo)

    hits = pygame.sprite.spritecollide(player, enemigo_list, True)
    for hit in hits:
        player.life -= 25
        enemigo = Enemigo()
        all_sprites.add(enemigo)
        enemigo_list.add(enemigo)
        if player.life <= 0:
            game_over = True


    screen.blit(background, [0, 0])
    all_sprites.draw(screen)

    # Valor marcador
    draw_text(screen, str(score), 25, width // 2, 10)
    life_bar(screen, 10, 10, player.life)

    pygame.display.flip()

pygame.quit()

