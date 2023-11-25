import pygame
import random

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 900, 800
CELL_SIZE = 20
GRID_WIDTH, GRID_HEIGHT = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE
FPS = 20
clock = pygame.time.Clock()

# Colores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
BLUE =(0,0,255)

# Direcciones
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


#DEBUG
SHOW_GRID = True
MOVE_ON = True

# Clase Snake
class Snake:
    def __init__(self, dist_vision):
        self.distance_vision = dist_vision
        self.body = [(10,25)]#[(GRID_WIDTH // 2 , GRID_HEIGHT // 2  )]
        self.direction = RIGHT

    def update(self):
        new_head = (self.body[0][0] + self.direction[0], self.body[0][1] + self.direction[1]) if MOVE_ON else self.body[0]
        self.body.insert(0, new_head)
        #print(len(self.body))
    def change_direction(self, new_direction):
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction

    def collides_with_self_or_wall(self):
        head = self.body[0]
        return (
            head[0] < 0 or head[0] >= GRID_WIDTH or
            head[1] < 0 or head[1] >= GRID_HEIGHT or
            head in self.body[1:]
        )
    def look_up(self, food):
        current_head = self.body[0]

        

# Función principal del juego
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Snake Game')

    snake = Snake(dist_vision=30)

    food = create_food(snake.body)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction(UP)
                elif event.key == pygame.K_DOWN:
                    snake.change_direction(DOWN)
                elif event.key == pygame.K_LEFT:
                    snake.change_direction(LEFT)
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction(RIGHT)
                elif event.key == pygame.K_r:
                        snake = Snake(dist_vision=30)
                        food = create_food(snake.body)



        next_direction = snake.look_up(food)
        snake.update()

        if snake.body[0] == food:
            food = create_food(snake.body)
        else:
            snake.body.pop()

        if snake.collides_with_self_or_wall():
            running = True

        screen.fill(BLACK)
        if SHOW_GRID:
            draw_grid(screen, WIDTH, HEIGHT, CELL_SIZE)

        draw_snake(screen, snake.body)
        draw_vision(screen, snake.body)
        draw_food(screen, food)
        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()

# Función para dibujar el grid en la pantalla
def draw_grid(screen, width, height, cell_size):
    for x in range(0, width, cell_size):
        pygame.draw.line(screen, WHITE, (x, 0), (x, height))
    for y in range(0, height, cell_size):
        pygame.draw.line(screen, WHITE, (0, y), (width, y))

def draw_vision(screen, snake):
    head = (snake[0][0]* CELL_SIZE, snake[0][1] * CELL_SIZE)
    pygame.draw.circle(screen, RED, head, 10)
    cell = (10*CELL_SIZE)
    pygame.draw.circle(screen, RED, (head[0]- (CELL_SIZE * 10), head[1] -(CELL_SIZE*10)),10)

    pygame.draw.circle(screen, GREEN, (head[0]+ (CELL_SIZE * 10), head[1] + (CELL_SIZE*10)),10)

    point1 =  (head[0]-  cell, head[1] - cell)

    r = range( point1[0],point1[0]+(cell+cell + (CELL_SIZE)), CELL_SIZE)
    for x in r:
        pygame.draw.circle(screen, GREEN,(x, point1[1]),3)
        r2 = range(point1[1], point1[1] + (cell+cell+CELL_SIZE), CELL_SIZE)
        for y in r2:
                pygame.draw.circle(screen, GREEN,(x, y),3)





def draw_snake(screen, snake):
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE) ) 

# Función para dibujar la comida en la pantalla
def draw_food(screen, food):
    pygame.draw.rect(screen, RED, (food[0] * CELL_SIZE, food[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Función para generar comida en una ubicación aleatoria
def create_food(snake_body):
    while True:
        food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if food not in snake_body:
            return food

if __name__ == "__main__":
    main()
