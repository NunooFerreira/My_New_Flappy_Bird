import pygame
import random
import sys

# Funcoes:
def game_floor():
    screen.blit(floor_base, (floor_x_pos, 900))
    screen.blit(floor_base, (floor_x_pos + 576, 900))

def check_collision(pipes):
    #COLISAO DOS PIPES:
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            die_sound.play()
            print(tempo/100, "segundos")
            return False
    #COLISAO DA JANELA:
    # verificar se nao acertamos no chao:
    # DUVIDA: PORQUE E QUE QUANDO METO == SO APARECE 1 HIT, mas com < > aparecem todos.
    if bird_rect.top <= -100 or bird_rect.bottom >= 913:
        die_sound.play()
        return False
    else:
        return True

def create_pipe():
    random_pip_pos = random.choice(pipe_height)  #replace with a random
    bottom_pipe = pipe_surface.get_rect(midtop =(700, random_pip_pos))
    top_pipe = pipe_surface.get_rect(midbottom =(700, random_pip_pos - 300))
    return bottom_pipe, top_pipe

    
def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipe_surface,pipe)
        else:
            flipe_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flipe_pipe,pipe)
        

def move_pipes(pipes):
    if game_active:  # só move os canos se o jogo estiver ativo
        for i,pipe in enumerate(pipes):
            if pipe.centerx < -150:
                pipe_list.pop(i)
            else:
                pipe.centerx -= pipvelocity
    return pipes


def show_time(screen, tempo, number_images):
    # Converte tempo para segundos
    segundos = tempo // 120  # Supondo que o jogo esteja rodando a 120 frames por segundo
    # Divide o tempo em dígitos
    digits = [int(d) for d in str(segundos)]
    # Para cada dígito
    for i, digit in enumerate(digits):
        # Obtém a imagem do número correspondente
        number_image = number_images[digit]
        # Exibe a imagem na tela
        screen.blit(number_image, (10 + i * 21, 10))  # Ajuste as coordenadas e o espaçamento conforme necessário

def ShowScore(score):
    for i in range(0,len(pipe_list),2):
        if pipe_list[i].centerx <= bird_rect.centerx +80 + pipvelocity/2 and pipe_list[i].centerx > bird_rect.centerx +80 - pipvelocity/2:
            point_sound.play()
        if pipe_list[i].centerx <= bird_rect.centerx + pipvelocity/2 and pipe_list[i].centerx > bird_rect.centerx - pipvelocity/2:
            score += 1
            print(score)
    return score

def ShowScoreEcra(screen, score, number_images):
    scoredigit = score  # Supondo que o jogo esteja rodando a 120 frames por segundo
    # Divide o tempo em dígitos
    digits = [int(d) for d in str(scoredigit)]
    # Para cada dígito
    for i, digit in enumerate(digits):
        # Obtém a imagem do número correspondente
        number_image = number_images[digit]
        # Exibe a imagem na tela
        screen.blit(number_image, (280 + i *21,100)) # Ajustar as coordenadas e o espaçamento conforme necessário
   


def BestScore(score):
    file = open("highest_score.txt", "r")
    highest_score = int(file.read()) 
    if score > highest_score:
        file = open("highest_score.txt", "w")
        file.write(str(score))
        

def draw_text(text,font,text_col,x,y):
    img = font.render(text,True,text_col)
    screen.blit(img,(x,y))



# DEFINICOES DO JOGO:
pygame.init()
clock = pygame.time.Clock()

# Variveis:
gravity = 0.25
bird_movement = 0
screen = pygame.display.set_mode((576, 1024))
tempo = 0
text_font = pygame.font.SysFont(None,40,bold=True)
score = 0
pipvelocity = 4 
flappyfont = pygame.font.SysFont(None,40)


                


# LOAD IMAGENS:

# BACKGROUND:
# import image variavel background
background = pygame.image.load("assets/background-day.png").convert()
background = pygame.transform.scale2x(background)

# BIRD:
bird = pygame.image.load("assets/yellowbird-midflap.png").convert_alpha()
bird = pygame.transform.scale2x(bird)
bird_rect = bird.get_rect(center=(100, 512))  
flappy_morto = pygame.image.load("assets/flappy-morto.png").convert_alpha()
flappy_morto = pygame.transform.scale2x(flappy_morto)


# FLOOR
floor_base = pygame.image.load("assets/base.png").convert()
floor_base = pygame.transform.scale2x(floor_base)
floor_x_pos = 0
game_active = True

# GAME OVER
# conver_alpha HUGE para tirar background
loser_message = pygame.image.load("assets/gameover.png").convert_alpha()
loser_message = pygame.transform.scale2x(loser_message)


# START MESSAGE:
message = pygame.image.load("assets/message.png").convert_alpha()
again_message = message.get_rect(center=(288, 512))  # coordenadas das mensagens


#BOARD SCORE
board = pygame.image.load("assets/Board.png").convert()
board = pygame.transform.scale(board,(360,230))
board_ecra = board.get_rect(center=(288,535))


# PIPES
pipe_surface = pygame.image.load("assets/pipe-green.png")
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
pipe_height = [400,600,800]
SPAWN_PIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWN_PIPE,1200)


#SONS:
flap_sound = pygame.mixer.Sound('sound/wing.wav')
die_sound = pygame.mixer.Sound('sound/hit.wav')
point_sound = pygame.mixer.Sound('sound/point.wav')

#NUMEROS DE 0 a 9:
# Carregar imagens dos números
number_images = {
    0: pygame.image.load("assets/0.png").convert_alpha(),
    1: pygame.image.load("assets/1.png").convert_alpha(),
    2: pygame.image.load("assets/2.png").convert_alpha(),
    3: pygame.image.load("assets/3.png").convert_alpha(),
    4: pygame.image.load("assets/4.png").convert_alpha(),
    5: pygame.image.load("assets/5.png").convert_alpha(),
    6: pygame.image.load("assets/6.png").convert_alpha(),
    7: pygame.image.load("assets/7.png").convert_alpha(),
    8: pygame.image.load("assets/8.png").convert_alpha(),
    9: pygame.image.load("assets/9.png").convert_alpha(),
}



# CICLO DO JOGO
while True:

    for event in pygame.event.get():  # ficar a espera de instrucoes:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and  game_active:
                bird_movement =  - 9     # Subir 12 casas quando clicas ESPACO
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                score = 0
                bird_rect.center = (100, 512)
                bird_movement = 0
                pipe_list.clear()
                tempo = 0
                game_active = True
        if event.type == SPAWN_PIPE and game_active:
            pipe_list.extend(create_pipe())
 
    # Mete a imagem "background" no screen, nas coordernadas 0,0 que e o top left do screen
    screen.blit(background, (0, 0))
    
    if game_active:
        score = ShowScore(score)
        tempo += 1
        bird_movement = bird_movement + gravity
        bird_rect.centery = bird_rect.centery + bird_movement  # Colisao mas n entendi
        screen.blit(bird, bird_rect)  # Meter o bird com o seu movimento.

        #Mostar os Pipes:
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        # CHECKAR A COLISAO:
        game_active = check_collision(pipe_list)
        ShowScoreEcra(screen, score, number_images) #Mostra o Score na tela
        show_time(screen, tempo, number_images)  # Mostra o tempo na tela
    else:
        BestScore(score)
        
        show_time(screen, tempo, number_images)  # Mostra o tempo final na tela depois que o jogo termina
        # screen.blit(bird, bird_rect)  # Mostrar o pássaro no local da colisão
        draw_pipes(pipe_list)  # Mostrar os canos no local de colisão
        screen.blit(flappy_morto,bird_rect)             #Flappy morto
        # screen.blit(message, again_message)             # MESSAGEM DE REPETIR
        screen.blit(loser_message, (100, 100))          # MESSAGEM DE PERDEDOR
        screen.blit(board,board_ecra)                   # BOARD DO SCORE:
        floor_x_pos = 0                                 #Para o chao de mover


        draw_text("Boosted",flappyfont,(0,0,0),230,435)      #Escrever nome da conta que esta a jogar
        draw_text("Highest Score:",flappyfont,(0,0,0),150,520)      #Escrever higest score ecra
        draw_text("Score:",flappyfont,(0,0,0),150,560)      #Escrever Score Atual ecra

        #Isto e para meter numa funcao mas nao consegui deu erro?
        #PRINTAR O HIGEHST SCORE NO ECRA:
        file = open("highest_score.txt", "r")           
        highest_score = (file.read())
        draw_text(highest_score,text_font,(0,0,0),400,520)
        #Isto e para meter numa funcao mas nao consegui deu erro?
        
        #PRINTAR O SCORE NO ECRA:
        score = str(score)
        draw_text(score,text_font,(0,0,0),400,560)
        score = int(score)
            


    # Criar o chao, e fazer lo mover ao longo do while:
    floor_x_pos = floor_x_pos - 1
    game_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)  # FLUIDEZ DO JOGO
