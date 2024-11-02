import socket
import math
import pygame

pygame.init()
WIDTH = 800
HEIGHT = 600
CC = (WIDTH // 2, HEIGHT // 2)
old = (0, 0)
radius = 50
BLACK = pygame.Color(0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Бактерии")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Настраиваем сокет
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)  # Отключаем пакетирование
sock.connect(("localhost", 10000))
font = pygame.font.Font(None, 25)
text = font.render("Leftarion", True, BLACK)
text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
screen.blit(text, text_rect)
run = True
while run:
    for event in pygame.event.get():
        if event == pygame.QUIT:
            run = False

        if pygame.mouse.get_focused():
            pos = pygame.mouse.get_pos()
            vector = pos[0] - CC[0], pos[1] - CC[1]
            lenv = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
            vector = vector[0] / lenv, vector[1] / lenv
            if lenv <= radius:
                vector = 0, 0
            if vector != old:
                old = vector
                msg = f"<{vector[0]},{vector[1]}>"
                sock.send(msg.encode())


    # Получаем
    data = sock.recv(1024).decode()
    print("Получил:", data)
    screen.fill('gray')
    pygame.draw.circle(screen, (255, 0, 0), CC, radius)
    screen.blit(text, text_rect)
    pygame.display.update()


pygame.quit()
