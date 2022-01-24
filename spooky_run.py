import pygame 

from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):  # Sprite class zawiera surface i rectangle, może być ona rysowana i update'owana w łatwy sposob 
	def __init__(self):				# dlatego Player musi dziedziczyć po Sprite
		super().__init__()
		player_walk_1 = pygame.image.load('graphics/player/walk_1.png').convert_alpha() # wczytujemy pierwszy obrazek chodu gracza 
		player_walk_2 = pygame.image.load('graphics/player/walk_2.png').convert_alpha() # i drugi obrazek 
		self.player_walk = [player_walk_1,player_walk_2] # lista dwóch obrazków chodzenia 
		self.player_index = 0 # na początku pokazujemy obrazek nr 1 
		self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha() # wczytujemy zdjęcie podskoku gracza

		self.image = self.player_walk[self.player_index]  # tu zaznaczamy który obrazek powinniśmy pokazać 
		self.rect = self.image.get_rect(midbottom = (80,300)) #tu tworzymy Rectangle dla gracza, get_rect bierze surface gracza i rysuje wokół niego prostokąt
		self.gravity = 0 # dopóki gracz nie podskoczy grawitacja musi być równa 0 

		self.jump_sound = pygame.mixer.Sound('audio/jump.mp3') #importujemy dźwięk
		self.jump_sound.set_volume(0.5) # zmniejszamy głośność o połowę 

	def player_input(self):
		keys = pygame.key.get_pressed() # tworzymy listę wszystkich możliwych do naciśnięcia przycisków
		if keys[pygame.K_SPACE] and self.rect.bottom >= 300:  # jeśli naciśniemy spację i gracz jest na pozycji podłoża == nie podskoczył jeszcze 
			self.gravity = -20 # dodajemy grawitację
			self.jump_sound.play() # włączamy dźwięk podskoku

	def apply_gravity(self):
		self.gravity += 1
		self.rect.y += self.gravity
		if self.rect.bottom >= 300: # tu sie upewniamy że gracz nie spadnie poniżej podłoża 
			self.rect.bottom = 300

	def animation_state(self):
		if self.rect.bottom < 300:  # jeśli gracz nie znajduje się na pozycji podłoża
			self.image = self.player_jump  # wyświetlamy obrazek podskoczenia
		else: # w przeciwnym wypadku wyświetlamy animacje chodzenia
			self.player_index += 0.1 # dodajemy małą liczbę, żeby animacja nie była zbyt szybka 
			if self.player_index >= len(self.player_walk): #gdy index przekroczy długość tablicy obrazków (2) 
				self.player_index = 0 # znowu ustawiamy index na 0
			self.image = self.player_walk[int(self.player_index)]  # ustawiamy jeden z dwóch obrazków z tablicy 

	def update(self):
		self.player_input() 
		self.apply_gravity()
		self.animation_state()

class Opponent(pygame.sprite.Sprite):
	def __init__(self,type):
		super().__init__()
		
		if type == 'bat': #pierwszy przeciwnik jest nietoperzem
			bat_1 = pygame.image.load('graphics/bat/bat1.png').convert_alpha() # wczytujemy pierwszy obrazek poruszania nietoperza 
			bat_2 = pygame.image.load('graphics/bat/bat2.png').convert_alpha() # i drugi
			self.frames = [bat_1,bat_2] # lista dwóch obrazków poruszania  
			y_pos = 210 # pozycja tego przeciwnika jest wyższa niż kolejnego
		else:  # drugi przeciwnik jest pająkiem
			spider_1 = pygame.image.load('graphics/spider/spider1.png').convert_alpha() # wczytujemy pierwszy obrazek poruszania pająka 
			spider_2 = pygame.image.load('graphics/spider/spider2.png').convert_alpha() # i drugi
			self.frames = [spider_1,spider_2] # lista dwóch obrazków poruszania 
			y_pos  = 300 # pozycja tego przeciwnika jest niższa niż poprzedniego

		self.animation_index = 0 # na początku index obrazka do pokazania = 0
		self.image = self.frames[self.animation_index]  # na początku pokazujemy obrazek pierwszy z tablicy
		self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos)) #pozycja Y przeciwnika jest zawsze taka sama, ale pozycja X losowana

	def animation_state(self):
		self.animation_index += 0.1 # dodajemy małą liczbę, żeby animacja nie była zbyt szybka 
		if self.animation_index >= len(self.frames): #gdy index przekroczy długość tablicy obrazków (2)
			self.animation_index = 0  # znowu ustawiamy index na 0
		self.image = self.frames[int(self.animation_index)] # ustawiamy jeden z dwóch obrazków z tablicy 

	def destroy(self):
		if self.rect.x <= -100:  #gdy przeciwnik znika z planszy 
			self.kill() # usuwamy obiekt 

	def update(self):
		self.animation_state()
		self.rect.x -= 6 # przeciwnik będzie przesuwał się z każdą klatką w lewo 
		self.destroy() # tu sprawdzamy czy należy już usunąć przeciwnika

                                                        #  v czyli od momentu w kodzie pygame.init()
def display_score(): #get_ticks() mówi nam ile czasu minęło odkąd cała gra w pygame się rozpoczęła,a nie pojedyncza rozgrywka, 
	current_time = int(pygame.time.get_ticks() / 1000) - start_time  # dlatego musimy odejmować start_time + dzielimy przez 1000 żeby liczby były mniejsze 
	score_surf = text_font.render(f'Score: {current_time}',False,(0,255,68)) #tworzymy surface do wyświetlania wyników 
	score_rect = score_surf.get_rect(center = (400,50))  #tworzymy rectangle dla score_surf i ustawiamy go na środku
	screen.blit(score_surf,score_rect)
	return current_time #zwracamy obecny czas żeby przypisywać go do punktacji 

def collision_sprite():  # funkcja potrzebna do sprawdzania kolizji obiektow klasy Sprite 
	if pygame.sprite.spritecollide(player.sprite,opponent_group,False): # jeśli doszło do kolizji
		opponent_group.empty() # usuwamy wszystkich przeciwników 
		return False # zwróć false (dzięki temu game_active=false  i rozgrywka się kończy)
	else: 
		return True

##########################################################################################################
pygame.init() #musi być wywołany na samym początku, to on rozpoczyna grę 
screen = pygame.display.set_mode((800,400))#okno ma wysokość 400 i szerokość 800
pygame.display.set_caption('SpookyRun') # tytuł okna 
clock = pygame.time.Clock() #clock pomoże nam z utrzymaniem odpowiedniej liczby klatek na sekundę 
text_font = pygame.font.Font('font/MonsterPumpkin.ttf', 50) #wczytujemy czcionkę, z którą można potem napisać tekst metodą render 
game_active = False
start_time = 0  # na początku czas musi wynosić 0 
score = 0 # na początku rozgrywki mamy 0 punktów 
background_Music = pygame.mixer.Sound('audio/music.wav') # importujemy plik z muzyką na tło gry
background_Music.set_volume(0.1)  # zmniejszamy głośność muzyki w tle
background_Music.play(loops = -1) # ustawiamy zapętlenie na nieskończenie wiele razy  

#Grupy klas
player = pygame.sprite.GroupSingle() # w pygame jest Group i GroupSingle() - i najpierw trzeba utworzyć taką grupę
player.add(Player()) # tu dodajemy do single group naszego gracza 

opponent_group = pygame.sprite.Group() # tworzymy grupę przeciwników
												   #convert() przyspiesza grę, sprawia ze obrazek jest 'lepiej załadowany' w pythonie
sky_surface = pygame.image.load('graphics/Sky.png').convert() # obrazek nieba będzie załadowany jako 1 
ground_surface = pygame.image.load('graphics/ground.png').convert() # a nad nim będzie obrazek podłoża dlatego poinżej w screen.blit(ground_surface,(0,300))
																	#dodajemy przesunięcie, żeby podłoże nie zasłaniało nieba
# To będzie na ekranie:
ghost_startPng = pygame.image.load('graphics/player/ghost_start.png').convert_alpha() #importujemy zdjęcie startowe
ghost_startPng = pygame.transform.rotozoom(ghost_startPng,0, 0.35) #skalujemy zdjęcie startowe, żeby było ponad 2 razy mniejsze 
ghost_startPng_rect = ghost_startPng.get_rect(center = (400,200))

game_name = text_font.render('Spooky  run',False,(0,255,68))
game_name_rect = game_name.get_rect(center = (400,80))

game_message = text_font.render('Press space to start',False,(0,255,68))
game_message_rect = game_message.get_rect(center = (400,330))

# Timer do tworzenia przeciwników co pewnien czas
opponent_timer = pygame.USEREVENT + 1 # tworzymy tu customowy event (dodajemy +1 żeby mieć pewność że dany userevent nie był zarezerwowany dla pygame)
pygame.time.set_timer(opponent_timer,1500)  # który ma się wydarzyć co 1500 milisekund 

while True:  # główna pętla gry 
	for event in pygame.event.get():# tu sprawdzamy możliwy input gracza
		if event.type == pygame.QUIT: 
			pygame.quit() #zamknięcie okna gry
			exit() #ten fragment zamknie pętle while=wyłączy całkowicie program 

		if game_active:
			if event.type == opponent_timer: #ustalamy prawdopodobieństwo=2/5 na wylosowanie nietoperza i 3/5 na wylosowanie pająka 
				opponent_group.add(Opponent(choice(['bat','bat','spider','spider','spider']))) # tu tworzymy instancje naszych przeciwników 
		else: # gdy gra nie jest jeszcze aktywna
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: # gdy naciśniemy spację
				game_active = True # gra staje się aktywna 
				start_time = int(pygame.time.get_ticks() / 1000) # zaznaczamy czas kiedy gra się zaczęła, żeby policzyć ile trwała
																# dzielimy przez 1000 żeby liczby były mniejsze
															
	if game_active:
		screen.blit(sky_surface,(0,0)) #blit używamy,żeby umieścić jakąś Surface na innej Surface, tu ustawiamy obrazek nieba na pozycji 0,0
		screen.blit(ground_surface,(0,300)) #ustawiamy obrazek podłoża na pozycji 0,300
		score = display_score() # wywołujemy metodę do wyświetlania wyniku 
		
		player.draw(screen) # tu rysujemy/ wyświetlamy naszego gracza 
		player.update()

		opponent_group.draw(screen) # tu wyświetlamy/rysujemy naszych przeciwników 
		opponent_group.update()

		game_active = collision_sprite() #tu sprawdzamy czy następują kolizje, które mogłyby skończyć grę 
		
	else:# jeśli gra się skończyła albo jeszcze nie zaczęła 
		screen.fill((102,0,204)) #wypełniamy ekran kolorem 
		screen.blit(ghost_startPng,ghost_startPng_rect)

		score_message = text_font.render(f'Your score: {score}',False,(0,255,68))
		score_message_rect = score_message.get_rect(center = (400,330))
		screen.blit(game_name,game_name_rect)

		if score == 0: # kiedy gra się jeszcze nie rozpoczęła mamy 0 pkt i wyświetlamy komunikat startowy game_message
			screen.blit(game_message,game_message_rect) 
		else:  # kiedy gra sie skończyła mamy X punktów i wyświetlamy je na ekranie jako score_message
			screen.blit(score_message,score_message_rect)

	pygame.display.update() # tutaj aktualizujemy wyświetlane na ekranie rzeczy 
	clock.tick(60) #ten fragment mówi pętli while, żeby nie wykonywała się szybciej niż 60 razy na sekundę 
				#dzięki temu nasza gra nie będzie działać szybciej, niż pozwala nasza ustalona max liczba
	#ustalanie minimalnej liczby klatek na sekundę nie jest konieczne przy grze na tyle prostej, jaką tu tworzymy 