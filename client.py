import math
import socket
import tkinter as tk
import tkinter.messagebox
from tkinter import ttk

import pygame


def scroll(event):
    global color
    color = combo.get()
    style.configure("TCombobox", fieldbackground=color, background="white")


def login():
    global name
    name = row.get()
    if name and color:
        root.destroy()
        root.quit()
    else:
        tk.messagebox.showerror("Ошибка", "Ты не выбрал цвет или не ввёл имя!")


def find(vector: str):
    first = None
    for num, sign in enumerate(vector):
        if sign == "<":
            first = num
        if sign == ">" and first is not None:
            second = num
            result = vector[first + 1:second]  # Поменяли
            return result
    return ""


def draw_bacteries(data: list[str]):
    for num, bact in enumerate(data):
        data = bact.split(" ")  # Разбиваем по пробелам подстроку одной бактерии
        x = CC[0] + int(data[0])
        y = CC[1] + int(data[1])
        size = int(data[2])
        color = data[3]
        pygame.draw.circle(screen, color, (x, y), size)


pygame.init()
WIDTH = 800
HEIGHT = 600
CC = (WIDTH // 2, HEIGHT // 2)
old = (0, 0)
radius = 50
name = ""
color = ""
BLACK = pygame.Color(0, 0, 0)
colors = ['Maroon', 'DarkRed', 'FireBrick', 'Red', 'Salmon', 'Tomato', 'Coral', 'OrangeRed', 'Chocolate', 'SandyBrown',
          'DarkOrange', 'Orange', 'DarkGoldenrod', 'Goldenrod', 'Gold', 'Olive', 'Yellow', 'YellowGreen', 'GreenYellow',
          'Chartreuse', 'LawnGreen', 'Green', 'Lime', 'Lime Green', 'SpringGreen', 'MediumSpringGreen', 'Turquoise',
          'LightSeaGreen', 'MediumTurquoise', 'Teal', 'DarkCyan', 'Aqua', 'Cyan', 'Dark Turquoise', 'DeepSkyBlue',
          'DodgerBlue', 'RoyalBlue', 'Navy', 'DarkBlue', 'MediumBlue']

root = tk.Tk()
root.title("Логин")
root.geometry("300x200")

style = ttk.Style()
style.theme_use('default')
name_label = tk.Label(root, text="Введи свой никнейм:")
name_label.pack()
row = tk.Entry(root, width=30, justify="center")
row.pack()
color_label = tk.Label(root, text="Выбери цвет:")
color_label.pack()
colors = ['Maroon', 'DarkRed', 'FireBrick', 'Red', 'Salmon', 'Tomato', 'Coral', 'OrangeRed', 'Chocolate', 'SandyBrown',
          'DarkOrange', 'Orange', 'DarkGoldenrod', 'Goldenrod', 'Gold', 'Olive', 'Yellow', 'YellowGreen', 'GreenYellow',
          'Chartreuse', 'LawnGreen', 'Green', 'Lime', 'SpringGreen', 'MediumSpringGreen', 'Turquoise',
          'LightSeaGreen', 'MediumTurquoise', 'Teal', 'DarkCyan', 'Aqua', 'Cyan', 'DeepSkyBlue',
          'DodgerBlue', 'RoyalBlue', 'Navy', 'DarkBlue', 'MediumBlue']

combo = ttk.Combobox(root, values=colors, textvariable=color)
combo.bind("<<ComboboxSelected>>", scroll)
combo.pack()
name_btn = tk.Button(root, text="Зайти в игру", command=login)
name_btn.pack()
root.mainloop()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Бактерии")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Настраиваем сокет
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)  # Отключаем пакетирование
sock.connect(("localhost", 10000))
# Отправляем цвет и имя
sock.send(("color:<" + name + "," + color + ">").encode())
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
    # print("Получил:", data)
    data = find(data).split(",")  # Разбиваем на шары
    screen.fill('gray')
    if data != ['']:
        radius = int(data[0])  # Сохраняем размер из сообщения в переменную
        draw_bacteries(data[1:])  # Срезаем размер, чтобы он не попадал в ф-ию рисования соседей
    pygame.draw.circle(screen, color, CC, radius)
    screen.blit(text, text_rect)
    pygame.display.update()

pygame.quit()
