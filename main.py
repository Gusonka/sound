import pygame
from pygame import *
import sounddevice as sd

fs = 44100
chunk = 1024

width = 800
height = 400

pygame.init()
screen = display.set_mode((width, height))
display.set_caption("Візуалізатор звукових хвиль")

data = [0] * chunk

def audio_callback(indata, frames, time_info, status):
    global data
    if status:
        print(status)
    # Масштабуємо звук під висоту екрану
    data = [sample * (height // 2) for sample in indata[:, 0]]

# === Запуск потоку з мікрофона ===
stream = sd.InputStream(
    callback=audio_callback,
    channels=1,
    samplerate=fs,
    blocksize=chunk,
    dtype='float32'
)
stream.start()

running = True
clock = time.Clock()

while running:
    for e in pygame.event.get():
        if e.type == QUIT:
            running = False

    screen.fill((0, 0, 0))
    points = []

    for i, sample in enumerate(data):
        x = int(i * width / chunk)
        y = int(height / 2 + sample)
        points.append((x, y))

    if len(points) > 1:
        draw.lines(screen, (0, 255, 0), False, points, 2)

    display.update()
    clock.tick(60)

# Коректне завершення
stream.stop()
stream.close()
pygame.quit()
