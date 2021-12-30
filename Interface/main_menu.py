import pygame, sys, os
from pygame.constants import K_ESCAPE, KEYDOWN, MOUSEBUTTONDOWN
from Interface.play_game import WHITE

path = os.path.join(os.path.dirname(__file__))
sys.path.insert(1, path)
import play_game

width = 800
height = 600


clock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption("Sliding Puzzle")
screen = pygame.display.set_mode((width, height), 0)
background_color = (253, 253, 101)
BLACK = (0, 0, 0)
YELLOW = (255, 247, 0)


def draw_text(text, font, color, surface, x_coor, y_coor):
    textObject = font.render(text, True, color)
    textRect = textObject.get_rect()
    textRect.center = (x_coor, y_coor)
    surface.blit(textObject, textRect)


def button(
    text_content,
    font,
    surface,
    dx,
    dy,
    width=200,
    height=50,
    text_color=(255, 255, 255),
    button_color=(255, 0, 0),
):
    btn = pygame.Rect(dx, dy, width, height)
    pygame.draw.rect(surface, button_color, btn)
    draw_text(
        text_content, font, text_color, surface, dx + width // 2, dy + height // 2
    )
    return btn


def main_menu():

    click = False  # check if click on button or not

    while True:

        mx, my = pygame.mouse.get_pos()

        screen.fill(background_color)
        x_main_menu, y_main_menu = 300, 100
        draw_text("MAIN MENU",pygame.font.SysFont("san", 40),(0, 0, 0),screen,x_main_menu,y_main_menu,)

        btn1 = button("New game",pygame.font.SysFont("san", 30),screen,200,y_main_menu + 50,)
        btn2 = button("About",pygame.font.SysFont("san", 30),screen,200,y_main_menu + 150,)

        # if(btn1.collidepoint((mx, my))):
        #     if click:
        #         play_game()
        #         click = False

        # if btn2.collidepoint((mx,my)):
        #     if click:
        #         pass

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == MOUSEBUTTONDOWN:
                if btn1.collidepoint((mx, my)):
                    play()

                if btn2.collidepoint((mx, my)):
                    about()

            if event.type == pygame.KEYUP:
                if event.key == K_ESCAPE: 
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        clock.tick(60)


def play(): #for new game button

    running = True

    while running:
        screen.fill(background_color)
        offset = 50
        btn = []

        font = pygame.font.SysFont("san", 20)
        draw_text("Choose size of board:",pygame.font.SysFont("san", 40),BLACK,screen,width//2,100)
        for i in range(2, 6): 
            text = str(i)+"x"+str(i)
            btn.append(button(text, font, screen, (2*i-3)*width//8- offset, 200, 100, 40))
        
        for i in range (6, 10):
            text = str(i)+"x"+str(i)
            btn.append(button(text, font, screen, (i*2-11)*width//8- offset, 250, 100, 40))

        chooseFromFileBtn = button("Choose from file", font, screen, width/2-100, 400, 200, 40, text_color=(255,0,0), button_color=WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == MOUSEBUTTONDOWN:
                for i in range(0,8): 
                    if btn[i].collidepoint(pygame.mouse.get_pos()):
                        play_game.main(i+2)
                
                if chooseFromFileBtn.collidepoint(pygame.mouse.get_pos()):
                    play_game.main(0,1)

        pygame.display.update()
        clock.tick(60)


def about():
    # thông tin thành viên nhóm
    running = True

    while running:
        screen.fill(background_color)
        draw_text("About: ",pygame.font.SysFont("times", 30),(0, 0, 0),screen,width//2,100)
        draw_text("Các thành viên trong nhóm bao gồm: ",pygame.font.SysFont("times", 20),(0, 0, 0),screen,width//2,150)
        draw_text("1. Phạm Trung Việt ",pygame.font.SysFont("times", 20),(0, 0, 0),screen,width//2,200)
        draw_text("2. Nguyễn Thị Thùy Trang ",pygame.font.SysFont("times", 20),(0, 0, 0),screen,width//2,250)
        draw_text("3. Quách Thế Trường ",pygame.font.SysFont("times", 20),(0, 0, 0),screen,width//2,300)
        draw_text("4. Trần Văn Nghĩa ",pygame.font.SysFont("times", 20),(0, 0, 0),screen,width//2,350)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                if event.key == K_ESCAPE:
                    running = False

        pygame.display.update()
        clock.tick(60)

# if __name__ == "__main__":
#     main_menu()
