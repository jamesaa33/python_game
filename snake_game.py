import pygame
import sys
import random

'''

Issiue : 背景遮罩未添加且未设置重新开始
食物可能出现在蛇的体内


'''


class Snake:
    def __init__(self, pos_x, pos_y, commander):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.head_color = (30, 144, 255)  # 设置头部颜色
        self.body_color = (112, 128, 144)  # 设置身体颜色
        self.snake_direct = commander  # 蛇的前进方向
        self.snake_head = [self.pos_x * width / col, self.pos_y * height / row]  # 蛇头的位置创建
        self.body = [[self.pos_x * width / col, self.pos_y * height / row],
                     [(self.pos_x - 1) * width / col, self.pos_y * height / row],
                     [(self.pos_x - 2) * width / col, self.pos_y * height / row]]  # 绘制蛇的身体
        self.dead = 0  # 小蛇的存活与否，1为死亡，0为存活

    def snake_draw(self):
        for element in self.body:
            pygame.draw.rect(screen, self.head_color, (element[0] + 1, element[1] + 1, 24, 24))

    def move(self):
        global direct
        if direct == 'Top':
            self.pos_y -= 1
        elif direct == 'Right':
            self.pos_x += 1
        elif direct == 'Left':
            self.pos_x -= 1
        else:
            self.pos_y += 1
        self.snake_head = [self.pos_x * width / col, self.pos_y * height / row]
        self.body.insert(0, self.snake_head)


class Food:
    def __init__(self):
        self.pos_x = random.randint(1, 19)  # 随机食物位置
        self.pos_y = random.randint(1, 19)  # 随机食物位置
        self.position = [self.pos_x * width / col, self.pos_y * height / row]  # 食物位置
        self.food_color = (0, 255, 255)  # 食物颜色
        self.food_status = 0  # 食物状态,0表示未被吃，1表示被吃

    def draw(self):  # 绘制食物位置
        if self.food_status == 0:
            pygame.draw.rect(screen, self.food_color, (self.position[0] + 1, self.position[1] + 1, 24, 24))
        else:
            self.__init__()
            pygame.draw.rect(screen, self.food_color, (self.position[0] + 1, self.position[1] + 1, 24, 24))


def judge(food, snake):  # 判断食物是否被吃
    if food.position[0] == snake.snake_head[0] and food.position[1] == snake.snake_head[1]:
        food.food_status = 1
        snake.snake_draw()
    else:
        snake.body.pop()
        snake.snake_draw()


def reflash_background(screen, color):
    screen.fill(color)  # 绘制白色底色
    for x in range(0, 500, 25):  # 绘制直线
        pygame.draw.line(screen, (0, 0, 0), (x, 0), (x, 500), 1)
    for y in range(0, 500, 25):
        pygame.draw.line(screen, (0, 0, 0), (0, y), (500, y), 1)


def gameover():
    text = "Game Over!"
    score = "Score:  " + str(len(snake.body) - 3)
    font = pygame.font.SysFont("italic", 75)
    score_font = pygame.font.SysFont("Arial", 50)
    text_color = (0, 0, 0)
    surf = font.render(text, True, text_color)
    surf_font = score_font.render(score, True, text_color)
    screen.blit(surf, [screen.get_width() / 2 - surf.get_width() / 2, 100])
    screen.blit(surf_font, [screen.get_width() / 2 - surf.get_width() / 2, 150])


if __name__ == '__main__':
    pygame.init()
    width, height = 500, 500  # 窗口大小设置
    color = (255, 255, 255)
    row, col = 20, 20  # 初始化格子
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    pygame.display.set_caption('贪吃蛇')  # 窗口名称设置
    reflash_background(screen, color)  # 背景刷新
    direct_ran = random.randint(0, 4)  # 初始方向随机
    direct = None
    if direct_ran == 0:
        direct = 'Top'
    elif direct_ran == 1:
        direct = 'Left'
    elif direct_ran == 2:
        direct = 'Right'
    else:
        direct = 'Bottom'
    snake = Snake(10, 10, direct)  # 初始化snake
    food = Food()  # 初始化食物类

    # 游戏主循环
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 设置退出
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    direct = 'Top'
                elif event.key == pygame.K_LEFT:
                    direct = 'Left'
                elif event.key == pygame.K_RIGHT:
                    direct = 'Right'
                else:
                    direct = 'Bottom'
        if snake.pos_x > 19 or snake.pos_x < 0 or snake.pos_y < 0 or snake.pos_y > 19:
            snake.dead = 1
        if snake.dead == 0:  # 小蛇存活继续刷新页面
            reflash_background(screen, color)
            food.draw()
            snake.move()
            judge(food, snake)
        else:
            # background = screen.convert_alpha()
            # background.fill((255, 255, 255, 100))
            # pygame.draw.rect(background, (255, 255, 255, 200), pygame.Rect(0, 0, width, height))
            gameover()  # 打印结果
        pygame.display.flip()
        clock.tick(5)
