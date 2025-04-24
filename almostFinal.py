import stddraw
import stdio
import math
import random
import sys
import time
import threading
import stdarray
import stdaudio
from picture import Picture
# Screen dimensions
WIDTH, HEIGHT = 800, 600
stddraw.setCanvasSize(WIDTH, HEIGHT)
stddraw.setXscale(0, WIDTH)
stddraw.setYscale(0, HEIGHT)

# Colours
BLACK = stddraw.BLACK
WHITE = stddraw.WHITE
YELLOW = stddraw.YELLOW
GREEN = stddraw.GREEN
RED = stddraw.RED

# Global variables for aliens
radius = 20
aliens = []
move_y = 40
score = 0

# Images for the elements
alien_pic = Picture("alien.png")
missile_pic = Picture("missile.png")
boom_pic = Picture("boom.png")
shooter_pic = Picture("shooter.png")

# Keys for toggle state
keys_pressed = {
    'a': False,  # Toggle left movement
    'd': False,  # Toggle right movement
    'e': False,  # Toggle rotate up
    'r': False   # Toggle rotate down
}

# Functions for Game Audio
def play_sound_in_thread(samples):
    stdaudio.playSamples(samples)

def shooting_sound():

    sample_rate = 44100
    duration = 0.15
    N = int(sample_rate * duration)
    samples = stdarray.create1D(N, 0.0)

    for i in range(N):
        t = i / sample_rate
        freq = 1200.0 - 1000.0 * (i/N)
        pew = math.sin(2 * math.pi * t * freq)
        noise = (random.random() * 2 - 1) * 0.1
        envelope = 1.0 if i < N/10 else math.exp(-5.0 * (i - N/10)/N)
        samples[i] = envelope * (pew + noise) * 0.5

    sound_thread = threading.Thread(target=play_sound_in_thread, args=(samples,))
    sound_thread.start()

def explosion_sound():

    sample_rate = 22050  
    duration = 0.15  
    N = int(sample_rate * duration)
    samples = stdarray.create1D(N, 0.0)

    for i in range(N):
        t = i / sample_rate

        progress = min(1.0, i/N)  
        freq = max(30.0, 80.0 - 60.0 * progress)  


        boom = math.sin(2 * math.pi * t * freq)
        crackle = math.sin(2 * math.pi * t * 400) * math.exp(-8.0 * progress)
        noise = (random.random() * 2 - 1) * 0.4 * math.exp(-4.0 * progress)


        if i < N//8:  
            envelope = i / (N//8)
        else:  
            envelope = math.exp(-12.0 * (i - N//8)/N)

        samples[i] = envelope * (boom * 0.6 + crackle * 0.3 + noise) * 0.7

    sound_thread = threading.Thread(target=play_sound_in_thread, args=(samples,))
    sound_thread.start()

def gameover_sound():

    sample_rate = 44100
    duration = 3.0  
    N = int(sample_rate * duration)
    samples = stdarray.create1D(N, 0.0)

    for i in range(N):
        t = i / sample_rate

        freq1 = 400.0 - 350.0 * (i/N)
        freq2 = 600.0 - 500.0 * (i/N)
        wave1 = math.sin(2 * math.pi * t * freq1)
        wave2 = 0.5 * math.sin(2 * math.pi * t * freq2)

        envelope = math.exp(-0.8 * i/N)

        wave = wave1 + wave2 + 0.3 * math.sin(2 * math.pi * t * freq1 * 1.5)
        samples[i] = wave * envelope * 0.5

    sound_thread = threading.Thread(target=play_sound_in_thread, args=(samples,))
    sound_thread.start()

def youwin_sound():

    sample_rate = 44100
    duration = 2.5  
    N = int(sample_rate * duration)
    samples = stdarray.create1D(N, 0.0)

    notes = [
        (1046.50, 0.2),  # C6 (high)
        (1318.51, 0.2),   # E6 
        (1567.98, 0.3),   # G6
        (2093.00, 0.5)    # C7 (very high)
    ]
    
    position = 0
    for freq, note_length in notes:
        note_samples = int(note_length * sample_rate)
        end = min(position + note_samples, N)
        
        for i in range(position, end):
            t = (i - position) / sample_rate
            
            wave = (math.sin(2 * math.pi * t * freq) +
                   0.7 * math.sin(2 * math.pi * t * freq * 2.5) +  # Higher harmonic
                   0.4 * math.sin(2 * math.pi * t * freq * 4.2))   # Non-integer harmonic
            
            # Sharp envelope (quick attack, quick decay)
            attack = min(1.0, t/0.01)  #Very quick attack
            decay = math.exp(-t * 10)   #Quick decay
            envelope = attack * decay
            
            samples[i] += wave * envelope * 0.5
        
        position += note_samples
    
    #sparkling high-frequency ending
    sparkle_duration = 0.8
    sparkle_samples = int(sparkle_duration * sample_rate)
    for i in range(position, min(position + sparkle_samples, N)):
        t = (i - position) / sample_rate
        sparkle_freq = 3000 + 2000 * math.sin(t * 20)  # Wavering high frequency
        
        wave = math.sin(2 * math.pi * t * sparkle_freq)
        envelope = math.exp(-t * 4)  # Fade
        samples[i] += wave * envelope * 0.3
  
    sound_thread = threading.Thread(target=play_sound_in_thread, args=(samples,))
    sound_thread.start()

class Alien:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = 1

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def draw_alien(self):
        stddraw.picture(alien_pic, self.x, self.y, radius*2, radius*2)

    def create_grid(rows=3, cols=5):
        grid = []
        for i in range(rows): #creates a grid of aliens of rows x cols
            for j in range(cols):
                x = j * 60 + 40
                y = 576 - i * 48
                grid.append(Alien(x,y)) #adds the aliens positions to an array
        return grid

# Star class for twinkling stars 
class Star:
    def __init__(self):
        self.x = random.uniform(0, WIDTH)
        self.y = random.uniform(0, HEIGHT)
        self.size = random.uniform(1, 3)
        self.twinkle = random.randint(0, 100)

    def draw(self):
        if self.twinkle < 50:
            stddraw.setPenColor(WHITE)
            stddraw.filledCircle(self.x, self.y, self.size)
        self.twinkle = (self.twinkle + 1) % 100

# Shooter class for the turret
class Shooter:
    def __init__(self, x, y, width, height):
        self.x = x   # X position of the shooter
        self.y = y   # Y position of the shooter
        self.width = width   # Width of the shooter
        self.height = height # Height of the shooter
        self.turret_angle = 90   # Angle of the turret 
        self.missiles = []    # List to store active missiles

    def move_left(self):
        self.x -= 10  # Move left by 10
        if self.x < 0:  # Prevent moving off the left edge
            self.x = 0

    def move_right(self, screen_width):
        self.x += 10  # Move right by 10
        if self.x + self.width > screen_width:  # Prevent moving off the right edge
            self.x = screen_width - self.width

    def rotate_turret(self, angle_change):
        self.turret_angle += angle_change
        # Prevent turret from aiming below horizontal
        if self.turret_angle < 0:
            self.turret_angle = 0
        if self.turret_angle > 180:
            self.turret_angle = 180

    def shoot_missile(self):
        # Create a missile at the center of the turret's 'barrel'
        missile_x = self.x + self.width / 2
        missile_y = self.y + self.height
        missile_angle = math.radians(self.turret_angle)  
        self.missiles.append(Missile(missile_x, missile_y, missile_angle))

    def draw(self):
        stddraw.setPenColor(GREEN)
        # Adjusting for scaled image
        stddraw.picture(shooter_pic, self.x + self.width / 2.05, self.y + self.height/2, self.width, self.height)
        turret_length = 30
        turret_end_x = self.x + self.width / 2 + turret_length * math.cos(math.radians(self.turret_angle))
        turret_end_y = self.y + self.height + turret_length * math.sin(math.radians(self.turret_angle))
        stddraw.line(self.x + self.width / 2, self.y + self.height, turret_end_x, turret_end_y)
        # Draw missiles
        for missile in self.missiles:
            missile.draw()

class Missile:
    def __init__(self, x, y, angle):
        self.x = x                  # X position of the missile
        self.y = y                  # Y position of the missile
        self.angle = angle          # Angle of the missile (in radians)
        self.speed = 15             # Speed of the missile

    def update(self):
        # Update missile position based on angle and speed
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)

    def draw(self):
        # Draw the missile
        stddraw.picture(missile_pic, self.x , self.y, 20, 20)
class Game:
    def __init__(self):
        self.level = 1
        self.points = 10
        self.alien_x = 10
        self.over = 0
        self.row = 2
        self.col = 4
    def alien_movex(self):
        #increases the speed of alien by 10% per round
        return self.alien_x * (1 + (self.level - 1) * 0.1)
        #each alien worth more points per level
    def scoring(self):
        return (10 * self.level)

def show_title_screen():
    stars = [Star() for i in range(100)]

    while True:
        stddraw.clear(BLACK)

        # Draw twinkling stars
        for star in stars:
            star.draw()

        # Draw title
        stddraw.setPenColor(YELLOW)
        stddraw.setFontSize(74)  # Set font size for the title
        stddraw.text(WIDTH / 2, HEIGHT * 3 / 4, "COSMIC CONQUESTORS")

        # Draw instructions
        stddraw.setPenColor(WHITE)
        stddraw.setFontSize(36)  # Set font size for the instructions
        instructions = [
                "Press SPACE to Play",
                "A to Move/Stop Left, D to Move/Stop Right",
                "Q to Quit",
                "R to Rotate/Stop Right, E to Rotate/Stop Left",
                "SPACE to SHOOT"
                ]

        for i in range(len(instructions)):
            stddraw.text(WIDTH / 2, HEIGHT / 2 - i * 40, instructions[i])

        # Check for input
        if stddraw.hasNextKeyTyped():
            key = stddraw.nextKeyTyped()
            if key == " ":
                return  # Start the game
            elif key == "q":
                sys.exit()  

        # Display Graphics
        stddraw.show(200) #time delay as argument
def alien_update(move_x):
    edge = False #Boundary Condition: To detect the edge of the screen/canvas
    for alien in aliens:
        if (alien.x >= 760 and alien.direction == 1) or (alien.x <= 40 and alien.direction == -1): #Check if any aliens hit the wall
            edge = True
            break #if the leading alien hits the edge all aliens will hit the edge
    for alien in aliens:
        if edge:               
            alien.move(0, -move_y) #update the x and y position of the aliens
            alien.direction *= -1 #changes the direction
        else: 
            alien.move(alien.direction * move_x, 0)
    for alien in aliens:
        alien.draw_alien() #draws the aliens

def hit(missiles, aliens, points):
    global score
    for missile in missiles:
        for alien in aliens:
            if check_collision(missile,alien):
                explosion_sound()
                missiles.remove(missile)
                aliens.remove(alien)
                score += points
    return score

def game_check(aliens, shooter):
    for alien in aliens:
        closest_x = max(shooter.x, min(alien.x, shooter.x + 50))
        closest_y = max(shooter.y, min(alien.y, shooter.y + 20))
        distance = math.sqrt((closest_x - alien.x) ** 2 + (closest_y - alien.y) ** 2)
        if distance < (radius + 10): #since alien can only collide on the edge of shooter, radius + distance to edge of shooter results in collision
            return True

def check_collision(missile, alien):
    # Calculate the distance between the centers of the missile and alien.
        distance = math.sqrt((missile.x - alien.x) ** 2 + (missile.y - alien.y) ** 2)

        # If the distance is less than the sum of the radii, they are colliding.
        if distance < (3 + radius): 
            stddraw.picture(boom_pic, alien.x , alien.y, 40, 40) # Displays an explosion image
            return True
        else:
            return False

def lose_screen(score):

    stars = [Star() for i in range(100)]
    
    while True:
        stddraw.clear(BLACK)

        for star in stars:
            star.draw()

        stddraw.setPenColor(RED)
        stddraw.setFontSize(40)
        stddraw.text(WIDTH/2, HEIGHT/2, "GAME OVER")
        
        # Score display
        stddraw.setPenColor(WHITE)
        stddraw.setFontSize(20)
        stddraw.text(WIDTH/2, HEIGHT/2 - 30, f"Score: {score}")
        stddraw.text(WIDTH/2, HEIGHT/2 - 60, f"High Score: {find_highscore(load_score_history())}")
        # Instructions
        stddraw.text(WIDTH/2, HEIGHT/2 - 90, "Press 'R' to restart")
        stddraw.text(WIDTH/2, HEIGHT/2 - 120, "Press 'Q' to quit")
        
        stddraw.show(20)

        if stddraw.hasNextKeyTyped():
            key = stddraw.nextKeyTyped().lower()
            if key == 'r':
                return True
            elif key == 'q':
                sys.exit()

def victory_screen(score):

    stars = [Star() for i in range(100)]
    
    while True: 
        stddraw.clear(BLACK)

        for star in stars:
            star.draw()
        
        # Victory text
        stddraw.setPenColor(GREEN)
        stddraw.setFontSize(40)
        stddraw.text(WIDTH/2, HEIGHT/2, "YOU WIN!")
        
        # Score display
        stddraw.setPenColor(WHITE)
        stddraw.setFontSize(20)
        stddraw.text(WIDTH/2, HEIGHT/2 - 30, f"Score: {score}")
        stddraw.text(WIDTH/2, HEIGHT/2 - 60, f"High Score: {find_highscore(load_score_history())}")
        
        # Instructions
        stddraw.text(WIDTH/2, HEIGHT/2 - 90, "Press 'R' to play again")
        stddraw.text(WIDTH/2, HEIGHT/2 - 120, "Press 'Q' to quit")
        
        stddraw.show(20)

        if stddraw.hasNextKeyTyped():
            key = stddraw.nextKeyTyped().lower()
            if key == 'r':
                return True
            elif key == 'q':
                sys.exit()
def load_score_history():
    #Load all the scores from the text file to the list score_history
    score_history = []
    try:
        with open("highscore.txt", "r") as file:
            for line in file:
                try:
                    score = int(line.strip())
                    score_history.append(score)
                except ValueError:
                    print(f"Warning: Invalid score '{line.strip()}' in score history file.")
    # Does fail if file doesn't exist yet
    except FileNotFoundError:
        pass  
    return score_history

def save_score(score):
    #saves the score of the game to a text file
    try:
        with open("highscore.txt", "a") as file:
            file.write(f"{score}\n")  # Write score on a new line
    except IOError:
        print("Error writing to score history file!")

def find_highscore(score_history):
    #Finds the highest score from the score history
    if score_history:  # Check if the list is not empty
        return max(score_history)
    else:
        return 0  # Return 0 if there are no scores yet
game = Game()
def play_game():
    global aliens, score
    #Game state
    game.over = 0
    game.level = 1
    move_x = game.alien_movex()
    # Create stars for the game screen
    stars = [Star() for i in range(100)]
    # Create a shooter object
    shooter = Shooter(400, 50, 100, 50)  # Centered at the bottom
    # Adds the each alien of the list to aliens
    aliens.extend(Alien.create_grid(game.row, game.col))
    # Time dimentions for fire rate
    last_shot_time = 0
    cooldown = 0.4
    # Game loop
    while (not game.over):
        stddraw.clear(BLACK)

        # Draw stars
        for star in stars:
            star.draw()

        current_time = time.time()


        # check for input
        while stddraw.hasNextKeyTyped():
            key = stddraw.nextKeyTyped()
            if key in keys_pressed:
                keys_pressed[key] = not keys_pressed[key]
            elif key == ' ' and (current_time - last_shot_time >= cooldown):  # Shoot missile
                shooting_sound()
                shooter.shoot_missile()
                last_shot_time = current_time # Reset cooldown
            elif key == 'q':  # Quit game
                game.over = 1
                game.level = 1
                game.row = 2
                game.col = 4
                game.points = 10
                score = 0
                aliens.clear()
                return

        if keys_pressed['a']:  
            shooter.move_left() # Toggle left movement
        if keys_pressed['d']:  
            shooter.move_right(WIDTH) # Toggle right movement
        if keys_pressed['e']:  
            shooter.rotate_turret(5) # Toggle Anti-Clockwise rotation
        if keys_pressed['r']:  
            shooter.rotate_turret(-5) # Toggle Clockwise rotation        

        # Update missiles
        for missile in shooter.missiles:
            missile.update()


         # Draw shooter and missiles
        score = hit(shooter.missiles, aliens, game.points)
        stddraw.setFontSize(30)
        stddraw.text(700, 580, f"Score: {score}")
        stddraw.text(100, 60, f"Level: {game.level}")
        alien_update(move_x)
        shooter.draw()
        stddraw.show(50)  # 50ms delay
        if (not aliens):
            game.level += 1
            game.row += 1
            game.col += 1
            game.points = game.scoring()
            # If level 3 is beaten you win
            if (game.level == 4):
                game.over = 1
                game.level = 1
                game.row = 2
                game.col = 4
                game.points = 10
                save_score(score)
                youwin_sound()
                victory_screen(score)
                score = 0
                break
            # Displays Game level for 2 second
            youwin_sound()
            stddraw.setPenColor(YELLOW)
            stddraw.setFontSize(48)
            stddraw.text(WIDTH / 2, HEIGHT / 2, f"Level {game.level}")
            stddraw.show(3000)
            
            aliens.extend(Alien.create_grid(game.row, game.col)) # Create new aliens for the next level
            move_x = game.alien_movex() # Adjusts the movement speed

        elif game_check(aliens, shooter) or any(alien.y < 100 for alien in aliens):
            game.over = 1
            game.level = 1
            game.row = 2
            game.col = 4
            game.points = 10
            gameover_sound()
            save_score(score)
            lose_screen(score)
            score = 0
            aliens.clear()

        
        
            
           

def main():
    while True:
        show_title_screen()
        play_game()

if __name__ == "__main__":
    main()
