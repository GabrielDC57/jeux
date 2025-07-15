import pygame
import random
import math

# Initialisation de Pygame
pygame.init()

# Constantes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 15
BALL_SIZE = 20
BRICK_WIDTH = 75
BRICK_HEIGHT = 25
BRICK_ROWS = 6
BRICK_COLS = 10
BULLET_WIDTH = 3
BULLET_HEIGHT = 10
POWERUP_SIZE = 20

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
PINK = (255, 192, 203)

class Ball:
    def __init__(self, x, y, dx=5, dy=-5):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.size = BALL_SIZE
        
    def move(self):
        self.x += self.dx
        self.y += self.dy
        
    def bounce_x(self):
        self.dx = -self.dx
        
    def bounce_y(self):
        self.dy = -self.dy
        
    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.size)

class Paddle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.speed = 8
        
    def move_left(self):
        self.x -= self.speed
        if self.x < 0:
            self.x = 0
            
    def move_right(self):
        self.x += self.speed
        if self.x + self.width > SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.width
            
    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height))

class Brick:
    def __init__(self, x, y, color, hits=1):
        self.x = x
        self.y = y
        self.width = BRICK_WIDTH
        self.height = BRICK_HEIGHT
        self.color = color
        self.hits = hits
        self.alive = True
        
    def hit(self):
        self.hits -= 1
        if self.hits <= 0:
            self.alive = False
            return True
        return False
        
    def draw(self, screen):
        if self.alive:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
            pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height), 2)

class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = BULLET_WIDTH
        self.height = BULLET_HEIGHT
        self.speed = 10
        
    def move(self):
        self.y -= self.speed
        
    def draw(self, screen):
        pygame.draw.rect(screen, YELLOW, (self.x, self.y, self.width, self.height))

class PowerUp:
    def __init__(self, x, y, type_):
        self.x = x
        self.y = y
        self.type = type_
        self.size = POWERUP_SIZE
        self.speed = 6
        
    def move(self):
        self.y += self.speed
        
    def draw(self, screen):
        color = GREEN if self.type == 'multiball' else RED if self.type == 'gun' else BLUE
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.size)
        
        # Dessiner le symbole du power-up
        font = pygame.font.Font(None, 24)
        symbol = 'M' if self.type == 'multiball' else 'G' if self.type == 'gun' else 'B'
        text = font.render(symbol, True, WHITE)
        text_rect = text.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(text, text_rect)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Gabrielorid")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        
        self.reset_game()
        
    def reset_game(self):
        self.paddle = Paddle(SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2, SCREEN_HEIGHT - 50)
        self.balls = [Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)]
        self.bullets = []
        self.powerups = []
        self.score = 0
        self.lives = 3
        self.level = 1
        self.gun_timer = 55555555555555555555555555555555555555555555555555555555555555555555555555555555555555555559999999999999999999999999999999999999
        
        self.create_bricks()
        
    def create_bricks(self):
        self.bricks = []
        colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
        
        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLS):
                x = col * (BRICK_WIDTH + 5) + 50
                y = row * (BRICK_HEIGHT + 5) + 50
                color = colors[row % len(colors)]
                hits = 1 if row < 3 else 2  # Les briques du bas sont plus résistantes
                brick = Brick(x, y, color, hits)
                self.bricks.append(brick)
                
    def handle_collisions(self):
        # Collision balle-murs
        for ball in self.balls[:]:
            if ball.x <= ball.size or ball.x >= SCREEN_WIDTH - ball.size:
                ball.bounce_x()
            if ball.y <= ball.size:
                ball.bounce_y()
            elif ball.y >= SCREEN_HEIGHT:
                self.balls.remove(ball)
                
        # Si plus de balles, perdre une vie
        if not self.balls:
            self.lives -= 1
            if self.lives > 0:
                self.balls.append(Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
            
        # Collision balle-paddle
        for ball in self.balls:
            if (ball.y + ball.size >= self.paddle.y and
                ball.y - ball.size <= self.paddle.y + self.paddle.height and
                ball.x >= self.paddle.x and
                ball.x <= self.paddle.x + self.paddle.width):
                
                # Changer l'angle selon où la balle touche la raquette
                hit_pos = (ball.x - self.paddle.x) / self.paddle.width
                angle = (hit_pos - 0.5) * math.pi / 3  # Angle entre -60° et 60°
                speed = math.sqrt(ball.dx**2 + ball.dy**2)
                ball.dx = speed * math.sin(angle)
                ball.dy = -abs(speed * math.cos(angle))
                
        # Collision balle-briques
        for ball in self.balls:
            for brick in self.bricks:
                if (brick.alive and
                    ball.x + ball.size >= brick.x and
                    ball.x - ball.size <= brick.x + brick.width and
                    ball.y + ball.size >= brick.y and
                    ball.y - ball.size <= brick.y + brick.height):
                    
                    # Déterminer le côté de collision
                    if ball.x < brick.x or ball.x > brick.x + brick.width:
                        ball.bounce_x()
                    else:
                        ball.bounce_y()
                    
                    if brick.hit():
                        self.score += 10
                        # Chance d'apparition d'un power-up
                        if random.random() < 0.15:
                            powerup_type = random.choice(['multiball', 'gun', 'big_paddle'])
                            self.powerups.append(PowerUp(brick.x + brick.width // 2, 
                                                       brick.y + brick.height // 2, 
                                                       powerup_type))
                    
        # Collision bullet-briques
        for bullet in self.bullets[:]:
            for brick in self.bricks:
                if (brick.alive and
                    bullet.x + bullet.width >= brick.x and
                    bullet.x <= brick.x + brick.width and
                    bullet.y <= brick.y + brick.height and
                    bullet.y + bullet.height >= brick.y):
                    
                    self.bullets.remove(bullet)
                    if brick.hit():
                        self.score += 10
                    break
                    
        # Collision paddle-powerups
        for powerup in self.powerups[:]:
            if (powerup.y + powerup.size >= self.paddle.y and
                powerup.y - powerup.size <= self.paddle.y + self.paddle.height and
                powerup.x >= self.paddle.x and
                powerup.x <= self.paddle.x + self.paddle.width):
                
                self.powerups.remove(powerup)
                self.activate_powerup(powerup.type)
                
    def activate_powerup(self, powerup_type):
        if powerup_type == 'multiball':
            # Ajouter 2 balles supplémentaires
            for _ in range(2):
                if self.balls:
                    base_ball = self.balls[0]
                    angle = random.uniform(-math.pi/4, math.pi/4)
                    speed = 5
                    dx = speed * math.sin(angle)
                    dy = -speed * math.cos(angle)
                    self.balls.append(Ball(base_ball.x, base_ball.y, dx, dy))
                    
        elif powerup_type == 'gun':
            self.gun_timer = 300  # 5 secondes à 60 FPS
            
        elif powerup_type == 'big_paddle':
            self.paddle.width = min(150, self.paddle.width + 25)
            
    def shoot(self):
        if self.gun_timer > 0:
            bullet = Bullet(self.paddle.x + self.paddle.width // 2 - BULLET_WIDTH // 2,
                          self.paddle.y - BULLET_HEIGHT)
            self.bullets.append(bullet)
            
    def update(self):
        # Mouvement des balles
        for ball in self.balls:
            ball.move()
            
        # Mouvement des bullets
        for bullet in self.bullets[:]:
            bullet.move()
            if bullet.y < 0:
                self.bullets.remove(bullet)
                
        # Mouvement des power-ups
        for powerup in self.powerups[:]:
            powerup.move()
            if powerup.y > SCREEN_HEIGHT:
                self.powerups.remove(powerup)
                
        # Décrémenter le timer du gun
        if self.gun_timer > 0:
            self.gun_timer -= 1
            
        # Vérifier si le niveau est terminé
        if not any(brick.alive for brick in self.bricks):
            self.level += 1
            self.create_bricks()
            # Ajouter une balle bonus
            if self.balls:
                self.balls.append(Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
                
        self.handle_collisions()
        
    def draw(self):
        self.screen.fill(BLACK)
        
        # Dessiner les objets
        self.paddle.draw(self.screen)
        
        for ball in self.balls:
            ball.draw(self.screen)
            
        for brick in self.bricks:
            brick.draw(self.screen)
            
        for bullet in self.bullets:
            bullet.draw(self.screen)
            
        for powerup in self.powerups:
            powerup.draw(self.screen)
            
        # Afficher le score et les vies
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        lives_text = self.font.render(f"Vies: {self.lives}", True, WHITE)
        level_text = self.font.render(f"Niveau: {self.level}", True, WHITE)
        
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(lives_text, (10, 50))
        self.screen.blit(level_text, (10, 90))
        
        # Afficher le timer du gun
        if self.gun_timer > 0:
            gun_text = self.font.render(f"Arme: {self.gun_timer // 60 + 1}s", True, YELLOW)
            self.screen.blit(gun_text, (SCREEN_WIDTH - 150, 10))
            
        pygame.display.flip()
        
    def run(self):
        running = True
        shoot_delay = 0
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.gun_timer > 0 and shoot_delay <= 0:
                        self.shoot()
                        shoot_delay = 10  # Délai entre les tirs
                    elif event.key == pygame.K_r and self.lives <= 0:
                        self.reset_game()
                        
            # Gestion des touches pressées
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.paddle.move_left()
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.paddle.move_right()
                
            if shoot_delay > 0:
                shoot_delay -= 1
                
            if self.lives > 0:
                self.update()
                
            self.draw()
            
            # Game Over
            if self.lives <= 0:
                game_over_text = self.font.render("GAME OVER - Appuyez sur R pour recommencer", True, RED)
                text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
                self.screen.blit(game_over_text, text_rect)
                pygame.display.flip()
                
            self.clock.tick(60)
            
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()