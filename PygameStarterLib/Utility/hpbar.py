import pygame, sys, random

pygame.init()

pygame.display.set_caption('HitPoint Bar')

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

SCREEN = pygame.display.set_mode( (SCREEN_WIDTH, SCREEN_HEIGHT) )

clock = pygame.time.Clock()

class Player:
	def __init__(self):
		self.hp = 10
		self.max_hp = 10

		self.x = 250
		self.y = 250

		self.width = 100
		self.height = 200

		self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

		self.current_hp_rect = pygame.Rect(self.x, self.y+self.height, 5, self.width)
		self.empty_hp_rect = pygame.Rect(self.x, self.y+self.height, 5, self.width)

		self.taking_damage = False
		self.take_damage_start = 0
		self.take_damage_end = 0
		self.take_damage_cd = 1 # multiple by Game FPS

	def updateHitPointHpBar(self):
		"""Represent player hp on a % scale of 1-10"""
		hp_length = round((self.hp/self.max_hp)*self.width)

		self.current_hp_rect = pygame.Rect(self.x, self.y+self.height, hp_length, 10)
		self.empty_hp_rect = pygame.Rect(self.x, self.y+self.height, self.width, 10)

	def draw(self, surface):
		"""Draw the player and hp bar"""
		self.updateHitPointHpBar()

		pygame.draw.rect(surface, "black", self.rect)
		pygame.draw.rect(surface, "dark grey", self.empty_hp_rect)
		pygame.draw.rect(surface, "green", self.current_hp_rect)

	def takeDamage(self, timer):
		if not self.taking_damage:
			self.hp -= random.randint(1, 3)
			self.taking_damage = True
			self.take_damage_start = timer
			self.take_damage_end = timer+self.take_damage_cd*60 # static for now

		if self.take_damage_end <= timer:
			self.taking_damage = False


player = Player()

timer = 0

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.display.quit()
			pygame.quit()
			sys.exit()

	timer += 1

	SCREEN.fill( "white" )

	player.draw(SCREEN)

	player.takeDamage(timer)

	pygame.display.update()
	clock.tick(60)