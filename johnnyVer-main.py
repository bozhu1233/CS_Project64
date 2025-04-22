import stddraw
import stdio
import math
import random
import sys

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

# Global variables for aliens & score
radius = 20
aliens = []
move_x = 10
move_y = 50
score = 0

# Alien Class
class Alien:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = 1

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def draw_alien(self):
        stddraw.setPenColor(WHITE)
        stddraw.filledCircle(self.x, self.y, radius)
    
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
        stddraw.rectangle(self.x, self.y, self.width, self.height)
        turret_length = 30
        turret_end_x = self.x + self.width / 2 + turret_length * math.cos(math.radians(self.turret_angle))
        turret_end_y = self.y + self.height + turret_length * math.sin(math.radians(self.turret_angle))
        stddraw.line(self.x + self.width / 2, self.y + self.height, turret_end_x, turret_end_y)
        # Draw missiles
        for missile in self.missiles:
            missile.draw()
# Missile Class
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
        # Draw the missile as a small circle
        stddraw.setPenColor(RED)
        stddraw.filledCircle(self.x, self.y, 3)

def show_title_screen():
    stars = [Star() for i in range(100)]

    while True:
        stddraw.clear(BLACK)

        # Draw twinkling stars
        for star in stars:
            star.draw()

        # Draw title
        stddraw.setPenColor(YELLOW)
        stddraw.setFontSize(70)  # Set font size for the title
        stddraw.text(WIDTH / 2, HEIGHT * 3 / 4, "COSMIC CONQUESTORS")

        # Draw instructions
        stddraw.setPenColor(WHITE)
        stddraw.setFontSize(36)  # Set font size for the instructions
        instructions = [
                "Press SPACE to Play",
                "A to Move Left, D to Move Right",
                "Q to Quit",
                "R to Rotate Right, E to Rotate Left",
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
def update_draw():
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

def check_collision(missile, alien): 
        
        distance = math.sqrt((missile.x - alien.x) ** 2 + (missile.y - alien.y) ** 2) # Calculate the distance between the centers of the missile and alien

        if distance < (3 + radius):  # If the distance is less than the missile radius + alien radius = colliding
            return True

def hit(missiles, aliens): 
    global score
    for missile in missiles: 
            for alien in aliens:
                if check_collision(missile,alien): 
                    missiles.remove(missile)
                    aliens.remove(alien)
                    score += 10
    return score

def game_check(aliens, shooter):
    for alien in aliens:
        closest_x = max(shooter.x, min(alien.x, shooter.x + 50))
        closest_y = max(shooter.y, min(alien.y, shooter.y + 20))
        distance = math.sqrt((closest_x - alien.x) ** 2 + (closest_y - alien.y) ** 2)
        if distance < (radius + 10): #since alien can only collide on the edge of shooter, radius + distance to edge of shooter results in collision
            return True

def play_game():
    global aliens, score 
    score = 0
    # Create stars for the game screen
    stars = [Star() for i in range(100)]
    # Create a shooter object
    shooter = Shooter(400, 50, 50, 20)  # Centered at the bottom
    # 0 for running game, 1 for game over
    game_over = 0 
    # Adds the each alien of the list to aliens
    aliens.extend(Alien.create_grid())
    # Game loop
    while (not game_over):
        stddraw.clear(BLACK)

        # Draw stars
        for star in stars:
            star.draw()

        # check for input
        if stddraw.hasNextKeyTyped():
            key = stddraw.nextKeyTyped()
            if key == 'a':  # Move left
                shooter.move_left()
            elif key == 'd':  # Move right
                shooter.move_right(WIDTH)
            elif key == 'e':  # Rotate turret up
                shooter.rotate_turret(10)
            elif key == 'r':  # Rotate turret down 
                shooter.rotate_turret(-10)
            elif key == ' ':  # Shoot missile
                shooter.shoot_missile()
            elif key == 'q':  # Quit game
                return

        # Update missiles
        for missile in shooter.missiles:
            missile.update()

        # Draw shooter and missiles
        score = hit(shooter.missiles, aliens)
        stddraw.text(700, 580, f"Score: {score}")
        print(score)
        update_draw()
        shooter.draw()
        stddraw.show(10)  # 50ms delay
        if score == 150 or game_check(aliens, shooter):
            game_over = 1
            aliens.clear()

def main():
    while True:
        show_title_screen()
        play_game()
        print("game over")

if __name__ == "__main__":
    main()
