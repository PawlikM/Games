import pygame
from pygame import *
import random

pygame.init()

szerokosc_okna = 800
wysokosc_okna = 600
ekran = pygame.display.set_mode((szerokosc_okna, wysokosc_okna))
pygame.display.set_caption('Tanks')

#definiujemy kolory, czcionki itp...
white = (255, 255, 255)
black = (0, 0, 0)
blue = (10,50,255)
red = (200, 0, 0)
yellow = (200, 200, 0)
green = (35, 175, 75)
clock = pygame.time.Clock()
czcionka = pygame.font.SysFont("arial", 25)

#Robimy wymiary czolgow
szerokosc = 40
wysokosc = 25
lufa = 5
ziemia = 35

#Funkcja ktora okresla kat nachylenia lufy
def kat(x,y,poz):
     x = int(x)
     y = int(y)
     angle={
        8:"50",
        7:"45",
        6:"40",
        5:"35",
        4:"30",
        3:"25",
        2:"20",
        1:"15", 
        0:"10" 
        }
     angle=angle.get(poz)
     tekst = czcionka.render("Angle: " + str(angle) + " degrees", True, white)
     ekran.blit(tekst, [350, 30])

#rysujemy nasz czolg
def tank(x, y, poz):
    x = int(x)
    y = int(y)
    
    #Wypisujemy mozliwe polozenia lufy
    katy = [(x - 27, y - 2),
                       (x - 27, y - 5),
                       (x - 25, y - 8),
                       (x - 23, y - 12),
                       (x - 20, y - 14),
                       (x - 18, y - 15),
                       (x - 15, y - 17),
                       (x - 13, y - 19),
                       (x - 11, y - 21)
                       ]
    pygame.draw.circle(ekran, blue, (x, y), int(wysokosc / 2))
    pygame.draw.rect(ekran, blue, (x - wysokosc, y, szerokosc, wysokosc))
    pygame.draw.line(ekran, blue, (x, y), katy[poz], lufa)
    return katy[poz]
#rysujemy czolg przeciwnika
def enemy_tank(x, y, poz):
    x = int(x)
    y = int(y)
    katy = [(x + 27, y - 2),
                       (x + 26, y - 5),
                       (x + 25, y - 8),
                       (x + 23, y - 12),
                       (x + 20, y - 14),
                       (x + 18, y - 15),
                       (x + 15, y - 17),
                       (x + 13, y - 19),
                       (x + 11, y - 21)
                       ]    

    pygame.draw.circle(ekran, blue, (x, y), int(wysokosc / 2))
    pygame.draw.rect(ekran, blue, (x - wysokosc, y, szerokosc, wysokosc))
    pygame.draw.line(ekran, blue, (x, y), katy[poz], lufa)
    return katy[poz]

#robimy murek w losowej lokacji
def mur(loklizacja, mur_wysokosc, grubosc):
    pygame.draw.rect(ekran, green, [loklizacja, wysokosc_okna - mur_wysokosc, grubosc, mur_wysokosc])

#Definiujemy i rysujemy paski "health"
def health_bars(player_health, enemy_health):
    if player_health > 75:
        kolor_gracza = green
    elif player_health > 50:
        kolor_gracza = yellow
    else:
        kolor_gracza = red

    if enemy_health > 75:
        kolor_przeciwnika = green
    elif enemy_health > 50:
        kolor_przeciwnika = yellow
    else:
        kolor_przeciwnika = red

    pygame.draw.rect(ekran, kolor_gracza, (680, 25, player_health, 25))
    pygame.draw.rect(ekran, kolor_przeciwnika, (20, 25, enemy_health, 25))
    
#definicja strzalu czolgu
def fire(xy, tankx, tanky, poz, gun_power, xlocation, grubosc, mur_wysokosc, enemyTankX):
    fire = True
    damage = 0
    pociski = list(xy)
    while fire:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        pygame.draw.circle(ekran, red, (pociski[0], pociski[1]), 5)
        pociski[0] -= (12 - poz) * 2
        pociski[1] += int((((pociski[0] - xy[0]) * 0.015 / (gun_power / 50)) ** 2) - (poz + poz / (12 - poz)))

        #jesli pocisk jest ponad wysokoscia ziemi, spraw zeby byl niewidoczny
        if pociski[1] > wysokosc_okna - ziemia:
            hit_x = int((pociski[0] * wysokosc - ziemia) / pociski[1])
            hit_y = int(wysokosc - ziemia)
            if enemyTankX + 10 > hit_x > enemyTankX - 10:
                damage = 25
            elif enemyTankX + 15 > hit_x > enemyTankX - 15:
                damage = 20
            elif enemyTankX + 25 > hit_x > enemyTankX - 25:
                damage = 10
            fire = False

        #kiedy trafi w bariere tez spraw zeby byl niewidoczny
        check_x1 = pociski[0] <= xlocation + grubosc
        check_x2 = pociski[0] >= xlocation
        check_y1 = pociski[1] <= wysokosc_okna
        check_y2 = pociski[1] >= wysokosc_okna - mur_wysokosc

        if check_x1 and check_x2 and check_y1 and check_y2:
            hit_x = int((pociski[0]))
            hit_y = int(pociski[1])
            fire = False

        pygame.display.update()
        clock.tick(60)
    return damage

#definicja strzalu przeciwnika
def e_fire(xy, tankx, tanky, poz, gun_power, loklizacja, grubosc, mur_wysokosc, playerTankX):
    damage = 0
    #Ustawiamy losowo moc przeciwnika
    moc = random.randint(1,100)
    
    fire = True
    pociski = list(xy)

    while fire:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        #Narysuj strzal przeciwnika
        pygame.draw.circle(ekran, red, (pociski[0], pociski[1]), 5)
        #Od pierwszego kolka do kazdego nastepnego
        pociski[0] += (12 - poz) * 2
        gun_power = random.randrange(int(moc * 0.80), int(moc * 1.10))
        pociski[1] += int((((pociski[0] - xy[0]) * 0.015 / (gun_power / 50)) ** 2) - (poz + poz / (12 - poz)))

        #Spraw zeby pocisk zniknal kiedy....
        #Uderzy w ziemie
        if pociski[1] > wysokosc_okna - ziemia:
            hit_x = int((pociski[0] * wysokosc - ziemia) / pociski[1])
            hit_y = int(wysokosc - ziemia)
            fire = False
            #Ustawiamy wartosc uderzenia
            if playerTankX + 10 > hit_x > playerTankX - 10:
                damage = 25
            elif playerTankX + 15 > hit_x > playerTankX - 15:
                damage = 15
            elif playerTankX + 25 > hit_x > playerTankX - 25:
                damage = 10
                
        #Uderzy w bariere
        check_x1 = pociski[0] <= loklizacja + grubosc
        check_x2 = pociski[0] >= loklizacja
        check_y1 = pociski[1] <= wysokosc_okna
        check_y2 = pociski[1] >= wysokosc_okna - mur_wysokosc

        if check_x1 and check_x2 and check_y1 and check_y2:
            hit_x = int((pociski[0]))
            hit_y = int(pociski[1])
            fire = False

        pygame.display.update()
        clock.tick(60)
    return damage
    
#Ustawiamy moc pocisku    
def moc(level):
    tekst = czcionka.render("Power: " + str(level) + "%", True, white)
    ekran.blit(tekst, [350, 0])

#piszemy glowna petle gry!
def gameLoop():
    #Ustawiamy pozycje startowe czolgow i inne wartosci (szerokosc bariery, strzalu itp.)
    gameExit = False
    FPS = 15
    player_health = 100
    enemy_health = 100
    grubosc = 50
    mainTankX = szerokosc_okna * 0.9
    mainTankY = wysokosc_okna * 0.9
    tankMove = 0
    poz = 0
    zmiana = 0
    enemyTankX = szerokosc_okna * 0.1
    enemyTankY = wysokosc_okna * 0.9
    fire_power = 50
    z_moc = 0
    #Polozenie bariery i jej wysokosc
    loklizacja = (szerokosc_okna / 2) + random.randint(-0.1 * szerokosc_okna, 0.1 * szerokosc_okna)
    mur_wysokosc = random.randrange(wysokosc_okna * 0.1, wysokosc_okna * 0.6)

    #Jesli gra jest uruchomiona...
    while not gameExit:

        #Odczytaj co sie dzieje na ekranie
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                gameExit = True

            #Piszemy co sie dzieje po nacisnieciu jakiego guzika
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    tankMove = -5

                elif event.key == pygame.K_RIGHT:
                    tankMove = 5

                elif event.key == pygame.K_UP:
                    zmiana = 1

                elif event.key == pygame.K_DOWN:
                    zmiana = -1

                elif event.key == pygame.K_SPACE:
                    damage = fire(gun, mainTankX, mainTankY, poz, fire_power, loklizacja, grubosc, mur_wysokosc, enemyTankX)
                    enemy_health -= damage

                    #SPRAWIAMY ZEBY PRZECIWNIK SIE RUSZAL LOSOWO
                    ruchy = ['l', 'r']
                    Index = random.randrange(0, 2)

                    for x in range(random.randrange(0, 10)):

                        if szerokosc_okna * 0.3 > enemyTankX > szerokosc_okna * 0.03:
                            if ruchy[Index] == "l":
                                enemyTankX += 5
                            elif ruchy[Index] == "r":
                                enemyTankX -= 5
                            
                            #Ustawiamy tlo i wywolujemy funkcje
                            ekran.fill(black)
                            health_bars(player_health, enemy_health)
                            gun = tank(mainTankX, mainTankY, poz)
                            enemy_gun = enemy_tank(enemyTankX, enemyTankY, 8)
                            fire_power += z_moc
                            moc(fire_power)
                            kat(mainTankX, mainTankY, poz)
                            
                            mur(loklizacja, mur_wysokosc, grubosc)
                            ekran.fill(green, rect=[0, wysokosc_okna - ziemia, szerokosc_okna, ziemia])
                            pygame.display.update()

                            clock.tick(FPS)

                    damage = e_fire(enemy_gun, enemyTankX, enemyTankY, 8, 50, loklizacja, grubosc, mur_wysokosc, mainTankX)
                    player_health -= damage
                #Zmieniamy moc po przycisnieciu guzikow    
                elif event.key == pygame.K_q:
                    z_moc = -1
                elif event.key == pygame.K_e:
                    z_moc = 1
            #Czolgi przestaja sie ruszac po podniesieniu klawiszy
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    tankMove = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    zmiana = 0
                if event.key == pygame.K_q or event.key == pygame.K_e:
                    z_moc = 0
        mainTankX += tankMove
        poz += zmiana

        #OGRANICZAMY ZAKRES RUCHU LUFY
        if poz > 8:
            poz = 8
        elif poz < 0:
            poz = 0

        #Sprawiamy ze nasz czolg nie wyjdzie poza bariere
        if mainTankX - (szerokosc / 2) < loklizacja + grubosc:
            mainTankX += 5
            
        #WYSWIETLAMY KOMPONENTY
        ekran.fill(black)
        health_bars(player_health, enemy_health)
        gun = tank(mainTankX, mainTankY, poz)
        enemy_gun = enemy_tank(enemyTankX, enemyTankY, 8)
        fire_power += z_moc

        #Sprawiamy by uzytkownik wybieral moc od 1 do 100
        if fire_power > 100:
            fire_power = 100
        elif fire_power < 1:
            fire_power = 1
        moc(fire_power)
        kat(mainTankX, mainTankY, poz)

        mur(loklizacja, mur_wysokosc, grubosc)
        ekran.fill(green, rect=[0, wysokosc_okna - ziemia, szerokosc_okna, ziemia])
        pygame.display.update()

        #Drukujemy wynik i wylaczamy gre
        if player_health < 1:
            print ("GAME OVER")
            pygame.quit()
        elif enemy_health < 1:
            print ("YOU WON!!!")
            pygame.quit()
        clock.tick(FPS)

    pygame.quit()

gameLoop()