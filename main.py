import pygame
import time
import random
pygame.font.init()

#window, e in pixeli
WIDTH, HEIGHT =  1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space")

#aici punem imaginea de background
BG =pygame.transform.scale(pygame.image.load("pozaJoc.jpg"),(WIDTH,HEIGHT))

FONT = pygame.font.SysFont("comicsans",30)#aici alegi tipul fontului

def draw(player, elapsed_time, proiectile):
    WIN.blit(BG, (0,0))#ia de la coltul din stanga sus imaginea
    #aici afisam "timpul" la care a ajuns jocul
    time_text = FONT.render(f"Timpul:{round(elapsed_time)}s",1,"orange")
    WIN.blit(time_text,(10, 10))
    
    pygame.draw.rect(WIN, "orange", player)
    for proiectil in proiectile:
        pygame.draw.rect(WIN,"yellow",proiectil)
    
    pygame.display.update()
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
PLAYER_VEL = 5
PROIECTIL_WIDTH = 10
PROIECTIL_HEIGHT = 20
PROIECTIL_VEL = 2

# avem nevoie de structura repetitiva ce functioneaza cat jocul functioneaza
def main():
    functioneaza = True
    #aici am creat punctul
    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)#asta pentru ca avem nevoie sa fie jos de tot
    #Avem nevoie de un clock pentru while, deoarece, initial, punctul se misca prea repede
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0
    #o sa proiectez anumite "proiectile", care, cu trecerea timpului in joc, devin tot mai multe, crescand dificultatea jocului
    proiectil = pygame.Rect(100, HEIGHT - PROIECTIL_HEIGHT, PROIECTIL_WIDTH, PROIECTIL_HEIGHT)
    proiectil_add_increment = 2000
    proiectil_count = 0
    proiectile = []
    hit = False
    while functioneaza:
        proiectil_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        if proiectil_count > proiectil_add_increment:
            for _ in range(3):
                proiectil_x = random.randint(0,WIDTH-PROIECTIL_WIDTH)
                proiectil = pygame.Rect(proiectil_x, PROIECTIL_HEIGHT, PROIECTIL_WIDTH, PROIECTIL_HEIGHT)
                proiectile.append(proiectil)
            proiectil_add_increment = max(200, proiectil_add_increment-50)
            proiectil_count = 0



        for event in pygame.event.get():
         
            if event.type == pygame.QUIT:
                functioneaza = False
                break

         #aici o sa miscam punctul, folosindu-ne de tasta ce utilizatorul o apasa
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >=0 :#trebuie sa avem grija ca punctul sa nu iasa din imagine
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:#trebuie si aici sa avem grija sa nu iasa din imagine
            player.x += PLAYER_VEL

    #aici "miscam" proiectilele
        for proiectil in proiectile[:]:
            proiectil.y += PROIECTIL_VEL
        #sterge in cazul in care proiectilul nu a fost plasat bine in imagine
            if proiectil.y > HEIGHT:
                proiectile.remove(proiectil)
            elif proiectil.y + proiectil.height >= player.y and proiectil.colliderect(player):
                proiectile.remove(proiectil)
                hit = True
                break
        #aici verificam cazul in care utilizatorul a pierdut, in cazul acesta afisam ceva pe ecran
        if hit:
            lost_text = FONT.render("Wasted!",1,"white")
            WIN.blit(lost_text,(WIDTH/2 - lost_text.get_width()/2,HEIGHT/2 - lost_text.get_height()/2))#aici punem textul la mijlocul desenului
            pygame.display.update()
            pygame.time.delay(4000)
            break
        draw(player, elapsed_time, proiectile)
    pygame.quit()

if __name__ == "__main__":
    main() 