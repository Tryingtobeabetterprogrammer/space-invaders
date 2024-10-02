import pygame
import os
import time
import random
pygame.font.init()

width=750
height=750
WIN=pygame.display.set_mode((width,height))

red_space_ship=pygame.image.load('C:/vscode/face recognition/assets/pixel_ship_red_small.png')
blue_space_ship=pygame.image.load('C:/vscode/face recognition/assets/pixel_ship_blue_small.png')
green_space_ship=pygame.image.load('C:/vscode/face recognition/assets/pixel_ship_green_small.png')

yellow_space_ship=pygame.image.load('C:/vscode/face recognition/assets/pixel_ship_yellow.png')

red_laser=pygame.image.load('C:/vscode/face recognition/assets/pixel_laser_red.png')
blue_laser=pygame.image.load('C:/vscode/face recognition/assets/pixel_laser_blue.png')
green_laser=pygame.image.load('C:/vscode/face recognition/assets/pixel_laser_green.png')


yellow_laser=pygame.image.load('C:/vscode/face recognition/assets/pixel_laser_yellow.png')

bg=pygame.transform.scale(pygame.image.load('C:/vscode/face recognition/assets/background-black.png'),(width,height))

class Laser:
    def __init__(self,x,y,img):

        self.x=x
        self.y=y
        self.img=img
        self.mask=pygame.mask.from_surface(self.img)

    def draw(self,window):
        window.blit(self.img,(self.x,self.y))

    def move(self,val):
        self.y+=val

    def off_screen(self,height):
        return self.y>=height and self.y<=0
    
    def collision(self,obj):
        return collide(self,obj)




class ship:
    COOLDOWN=30
    def __init__(self,x,y,health=100):
        self.x=x
        self.y=y
        self.health=health
        self.ship_img=None
        self.laser_img=None
        self.lasers=[]
        self.cool_down_counter=0

    def draw(self,window):
        window.blit(self.ship_img,(self.x,self.y))
        for laser in self.lasers:
            laser.draw(window)


    def move_lasers(self,val,obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(val)
            if laser.off_screen(height):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health-=10
                self.lasers.remove(laser)


    def cooldown(self):
        if self.cool_down_counter>=self.COOLDOWN:
            self.cool_down_counter=0
        elif self.cool_down_counter>0:
            self.cool_down_counter +=1



    def shoot(self):
        if self.cool_down_counter==0:
            laser=Laser(self.x,self.y,self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter=1


    def get_width(self):
        return self.ship_img.get_width()
    def get_height(self):

        return self.ship_img.get_height()

class Player(ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img=yellow_space_ship
        self.laser_img=yellow_laser
        self.mask=pygame.mask.from_surface(self.ship_img)
        self.max_health=health

    def move_lasers(self, val, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(val)
            if laser.off_screen(height):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        self.lasers.remove(laser)

    def draw(self,window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self,window):
        pygame.draw.rect(window,(255,0,0),(self.x,self.y+self.ship_img.get_height()+10,self.ship_img.get_width(),10))
        pygame.draw.rect(window,(0,255,0),(self.x,self.y+self.ship_img.get_height()+10,self.ship_img.get_width()*(self.health/self.max_health),10))

class Enemy(ship):
    COLOUR_MAP={
        'red':(red_space_ship,red_laser),
        'green':(green_space_ship,green_laser),
        'blue':(blue_space_ship,blue_laser)

    }

    def __init__(self,x,y,colour,health=100):
        super().__init__(x,y,health)
        self.ship_img,self.laser_img=self.COLOUR_MAP[colour]
        self.mask=pygame.mask.from_surface(self.ship_img)

    def move(self,val):
        self.y+=val


def collide(obj1,obj2):
    off_x=obj2.x-obj1.x
    off_y=obj2.y-obj1.y

    return obj1.mask.overlap(obj2.mask,(off_x,off_y)) !=None

def main():
    run=True
    FPS=70
    level=0
    lives=5
    

    main_font=pygame.font.SysFont('comicsan',50)
    lost_font=pygame.font.SysFont('comicsan',60)

    Enemies=[]
    wave_leangth=5
    Enemy_val=1

    laser_val=4


    player_val=5
    player= Player(300,650)

    clock=pygame.time.Clock()

    lost=False
    lost_count=0


    def redraw_window():
        WIN.blit(bg,(0,0))
        lives_label=main_font.render(f'lives:{lives}',1,(255,255,255))
        level_label=main_font.render(f'level:{level}',1,(255,255,255))

        WIN.blit(lives_label,(10,10))
        WIN.blit(level_label,(10,90))
        for Enemy in Enemies:
            Enemy.draw(WIN)
        
        player.draw(WIN)

        if lost:
            lost_label=lost_font.render('you have lost',1,(255,255,255))
            WIN.blit(lost_label,(width/2-lost_label.get_width()/2,350))


        

        pygame.display.update() 

 

    while run:
        clock.tick(FPS)

        if lives<=0 or player.health<=0:
            lost=True
            lost_count+=1

        if lost:
            if lost_count>FPS*5:
                run=False
            else:
                continue

        if len(Enemies)==0:
            level+=1
            wave_leangth+=5
            for i in range(wave_leangth):
                enemy=Enemy(random.randrange(50,width-100),random.randrange(-1500,-100),random.choice(['red','green','blue']))
                Enemies.append(enemy)
            
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
        keys=pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_val>0:
            player.x-=player_val
        if keys[pygame.K_d] and player.x +player_val+player.get_width()<width:
            player.x+=player_val
        if keys[pygame.K_w] and player.y - player_val>0:
            player.y-=player_val
        if keys[pygame.K_s] and player.y + player_val+player.get_height()+15<height:
            player.y+=player_val
        if keys[pygame.K_SPACE]:
            player.shoot()


        for enemy in Enemies:
            enemy.move(Enemy_val)
            enemy.move_lasers(laser_val,player)


            if random.randrange(0,500)==1:
                enemy.shoot()
                if player is Enemies==0:
                    wave_leangth+=5

            if enemy.y+enemy.get_height()>height:
                lives-=1
                
                Enemies.remove(enemy)


            if collide(enemy,player):
                player.health-=10
                Enemies.remove(enemy)
            elif enemy.y+enemy.get_height()>height:
                lives-=1
                Enemies.remove(enemy)
        player.move_lasers(-laser_val,Enemies)
        redraw_window() 


def main_menu():
    Title_fony=pygame.font.SysFont('comicsans',70)
    run=True
    while run:
        WIN.blit(bg,(0,0))
        Title_label=Title_fony.render('press the  mouses to begin....',1,(255,255,255))
        WIN.blit(Title_label,(width/2-Title_label.get_width()/2,350))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type==pygame.MOUSEBUTTONDOWN:
                main()    

    pygame.quit()
main()
