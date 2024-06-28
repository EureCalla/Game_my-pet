import random
import sys
import time

import pygame

# 初始化Pygame
pygame.init()

# 設置窗口
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("寵物養成遊戲")

# 顏色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# 字體
font = pygame.font.Font(None, 32)


# 寵物類
class Pet:
    def __init__(self, species, image):
        self.species = species
        self.image = image
        self.hunger = 50
        self.happiness = 50
        self.x = WIDTH // 2
        self.y = HEIGHT // 2

    def feed(self):
        self.hunger = max(0, self.hunger - 20)

    def pet(self):
        self.happiness = min(100, self.happiness + 20)

    def move(self):
        self.x += random.randint(-5, 5)
        self.y += random.randint(-5, 5)
        self.x = max(0, min(WIDTH - 64, self.x))
        self.y = max(0, min(HEIGHT - 64, self.y))

    def random_event(self):
        event_type = random.choice(["hunger_increase", "happiness_decrease"])
        if event_type == "hunger_increase":
            self.hunger = min(100, self.hunger + 10)
            print("Event: Hunger increased")
        elif event_type == "happiness_decrease":
            self.happiness = max(0, self.happiness - 10)
            print("Event: Happiness decreased")


# 創建寵物圖像
def create_pet_image(color):
    image = pygame.Surface((64, 64), pygame.SRCALPHA)
    image.fill((0, 0, 0, 0))  # 透明背景

    # 身體
    pygame.draw.ellipse(image, color, [8, 16, 48, 32])

    # 腳
    pygame.draw.line(image, color, (18, 48), (18, 58), 4)
    pygame.draw.line(image, color, (46, 48), (46, 58), 4)
    pygame.draw.line(image, color, (18, 54), (18, 64), 4)
    pygame.draw.line(image, color, (46, 54), (46, 64), 4)

    # 耳朵
    pygame.draw.polygon(image, color, [(20, 16), (10, 0), (30, 8)])
    pygame.draw.polygon(image, color, [(44, 16), (54, 0), (34, 8)])

    return image


# 寵物選擇
def choose_pet():
    pets = [
        ("Lazy Dog : Vigo", (79, 59, 59)),  # 深棕色
        ("Angelic Cat : Bega", (97, 124, 76)),  # 淺灰色
        ("Crazy Dog : Mego", (200, 170, 93)),  # 黃色
    ]

    chosen = False
    choice = 0

    while not chosen:
        screen.fill(WHITE)
        title = font.render("Choose your pet:", True, BLACK)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

        for i, (name, color) in enumerate(pets):
            pet_img = create_pet_image(color)
            x_pos = WIDTH // 2 - 32 + (i - 1) * 200
            y_pos = HEIGHT // 2 - 32
            if i == choice:
                pygame.draw.rect(screen, RED, (x_pos - 5, y_pos - 5, 74, 74), 3)
            screen.blit(pet_img, (x_pos, y_pos))
            name_text = font.render(name, True, BLACK)
            screen.blit(
                name_text, (x_pos - name_text.get_width() // 2 + 32, y_pos + 82)
            )

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    choice = (choice - 1) % 3
                elif event.key == pygame.K_RIGHT:
                    choice = (choice + 1) % 3
                elif event.key == pygame.K_RETURN:
                    chosen = True

    return Pet(pets[choice][0], create_pet_image(pets[choice][1]))


# 主遊戲循環
def main():
    pet = choose_pet()
    clock = pygame.time.Clock()
    last_event_time = time.time()
    event_interval = random.randint(20, 60)

    while True:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    pet.feed()
                elif event.key == pygame.K_p:
                    pet.pet()

        # 檢查是否應該觸發隨機事件
        current_time = time.time()
        if current_time - last_event_time > event_interval:
            pet.random_event()
            last_event_time = current_time
            event_interval = random.randint(20, 60)

        pet.move()

        # 繪製寵物
        screen.blit(pet.image, (pet.x, pet.y))

        # 顯示狀態
        hunger_text = font.render(f"Hunger: {pet.hunger}", True, BLACK)
        happiness_text = font.render(f"Happiness: {pet.happiness}", True, BLACK)
        screen.blit(hunger_text, (10, 10))
        screen.blit(happiness_text, (10, 50))

        # 顯示操作說明
        instructions = font.render("Press F to feed, press P to caress", True, BLACK)
        screen.blit(instructions, (WIDTH - instructions.get_width() - 10, HEIGHT - 40))

        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
        pygame.quit()
        sys.exit()
