import math
import random
import pygame
import time

#Global Variables
rows = 20
width = 800

def getImage(imagePath, head = False):
  image = pygame.image.load("Images/" + imagePath)
  if head:
    picture = pygame.transform.scale(image, (80, 80))
  else:
    picture = pygame.transform.scale(image, (width // rows, width // rows))

  return picture

#Global Images
hieu = getImage("hieu.PNG", True)
banana = getImage("banana.jpg")
bomb = getImage("bomb.jpg")
watermelon = getImage("watermelon.jpg")
rice = getImage("rice.jpg")

class Square(object):
  def __init__(self, start, x_direction = 1, y_direction = 0, color = (255,192,203)):
    self.pos = start
    self.x_direction = 1
    self.y_direction = 0
    self.color = color
    self.rows = rows
    self.width = width

  def move(self, x_direction, y_direction):
    self.x_direction = x_direction
    self.y_direction = y_direction
    self.pos = (self.pos[0] + self.x_direction, self.pos[1] + self.y_direction)

  def draw(self, surface, imageType):
    distance = self.width // self.rows
    i = self.pos[0]
    j = self.pos[1]

    if imageType == "snakeHead":
      surface.blit(hieu, (i * distance - 20, j * distance - 20))

    elif imageType == "snakeBody":
      surface.blit(rice, (i * distance + 1, j * distance + 1))

    elif imageType == "banana":
      surface.blit(banana, (i * distance + 1, j * distance + 1))

    elif imageType == "bomb":
      surface.blit(bomb, (i * distance + 1, j * distance + 1))

    elif imageType == "watermelon":
      surface.blit(watermelon, (i * distance + 1, j * distance + 1))

    else:
      pygame.draw.rect(surface, self.color, (i * distance + 1, j * distance + 1, distance - 2, distance - 2))

class Snake(object):
  body = []
  turns = {}

  def __init__(self, color, pos):
    self.color = color
    self.head = Square(pos)
    self.body.append(self.head)
    self.x_direction = 0
    self.y_direction = 1

  def move(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()

      keys = pygame.key.get_pressed()

      for key in keys:
        if keys[pygame.K_LEFT]:
          if len(self.body) > 1 and self.body[1].x_direction == 1:
            pass
          else:
            self.x_direction = -1
            self.y_direction = 0
            self.turns[self.head.pos[:]] = [self.x_direction, self.y_direction]

        elif keys[pygame.K_RIGHT]:
          if len(self.body) > 1 and self.body[1].x_direction == -1:
            pass
          else:
            self.x_direction = 1
            self.y_direction = 0
            self.turns[self.head.pos[:]] = [self.x_direction, self.y_direction]

        elif keys[pygame.K_UP]:
          if len(self.body) > 1 and self.body[1].y_direction == 1:
            pass
          else:
            self.x_direction = 0
            self.y_direction = -1
            self.turns[self.head.pos[:]] = [self.x_direction, self.y_direction]

        elif keys[pygame.K_DOWN]:
          if len(self.body) > 1 and self.body[1].y_direction == -1:
            pass
          else:
            self.x_direction = 0
            self.y_direction = 1
            self.turns[self.head.pos[:]] = [self.x_direction, self.y_direction]

    for i, currentPos in enumerate(self.body):
      p = currentPos.pos[:]
      if p in self.turns:
        turn = self.turns[p]
        currentPos.move(turn[0], turn[1])
        if i == len(self.body) - 1:
          self.turns.pop(p)

      else:
        if currentPos.x_direction == -1 and currentPos.pos[0] <= 0:
          currentPos.pos = (currentPos.rows - 1, currentPos.pos[1])

        elif currentPos.x_direction == 1 and currentPos.pos[0] >= currentPos.rows - 1:
          currentPos.pos = (0, currentPos.pos[1])

        elif currentPos.y_direction == -1 and currentPos.pos[1] <= 0:
          currentPos.pos = (currentPos.pos[0], currentPos.rows - 1)

        elif currentPos.y_direction == 1 and currentPos.pos[1] >= currentPos.rows - 1:
          currentPos.pos = (currentPos.pos[0], 0)

        else:
          currentPos.move(currentPos.x_direction, currentPos.y_direction)

  def reset(self, pos):
    self.head = Square(pos)
    self.body = [self.head]
    self.turns = {}
    self.x_direction = 0
    self.y_direction = 1

  def addSquare(self):
    tail = self.body[-1]
    direct_x, direct_y = tail.x_direction, tail.y_direction

    if direct_x == 1 and direct_y == 0:
        self.body.append(Square((tail.pos[0]-1, tail.pos[1])))
    elif direct_x == -1 and direct_y == 0:
        self.body.append(Square((tail.pos[0]+1, tail.pos[1])))
    elif direct_x == 0 and direct_y == 1:
        self.body.append(Square((tail.pos[0], tail.pos[1]-1)))
    elif direct_x == 0 and direct_y == -1:
        self.body.append(Square((tail.pos[0], tail.pos[1]+1)))

    self.body[-1].x_direction = direct_x
    self.body[-1].y_direction = direct_y

  def delSquare(self):
    if len(self.body) > 1:
      self.body = [self.head]

  def draw(self, surface):
    for i, currentPos in enumerate(self.body):
      if i == 0:
        currentPos.draw(surface, 'snakeHead')
      else:
        currentPos.draw(surface, 'snakeBody')

def drawGrid(width, rows, surface):
  sizeofSquare = width // rows

  x = 0
  y = 0
  for length in range(rows):
    x += sizeofSquare
    y += sizeofSquare

    #Vertical line
    pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, width))

    #Horizontal line
    pygame.draw.line(surface, (255, 255, 255), (0, y), (width, y))

def reDrawWindow(surface):
  global rows, width, snake
  surface.fill((0, 0, 0))
  snake.draw(surface, )

  goodSnack.draw(surface, "banana")

  badSnack.draw(surface, 'bomb')

  timerSnack.draw(surface, 'watermelon')

  drawGrid(width, rows, surface)
  pygame.display.update()

def randomSnack(rows, item):
  positions = item.body

  while True:
    x = random.randrange(rows)
    y = random.randrange(rows)
    if len(list(filter(lambda z: z.pos == (x,y), positions))) > 0:
      continue
    else:
      break

  return (x, y)

def main():
  global snake, goodSnack, badSnack, timerSnack

  window = pygame.display.set_mode((width, width))
  snake = Snake((255,192,203), (10, 10))

  #Bad Snack
  goodSnack = Square(randomSnack(rows, snake))

  #Good Snack
  badSnack = Square(randomSnack(rows, snake), color = (255, 0, 0))

  #Timer Snack
  timerSnack = Square(randomSnack(rows, snake), color = (255, 204, 255))

  game = True

  clock = pygame.time.Clock()

  time_start = time.time()

  while game:

    pygame.time.delay(15)
    clock.tick(90)
    snake.move()

    if snake.body[0].pos == goodSnack.pos:
      snake.addSquare()

      goodSnack = Square(randomSnack(rows, snake), color = (0, 255, 0))

    if snake.body[0].pos == badSnack.pos:
      snake.delSquare()

      badSnack = Square(randomSnack(rows, snake), color = (255, 0, 0))

    seconds = int(time.time() - time_start)

    if snake.body[0].pos == timerSnack.pos and seconds < 2:
      snake.addSquare()
      snake.addSquare()
      timerSnack = Square(randomSnack(rows, snake), color = (255, 204, 255))
      time_start = time.time()

    elif seconds >= 2:
      timerSnack = Square(randomSnack(rows, snake), color = (255, 204, 255))
      time_start = time.time()


    for x in range(len(snake.body)):
        if snake.body[x].pos in list(map(lambda z:z.pos,snake.body[x+1:])):
          print('Score: ', len(snake.body))
          snake.reset((10, 10))
          break

    reDrawWindow(window)

main()