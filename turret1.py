import sys
import stdio
import math
import stddraw

stddraw.setCanvasSize(800, 600)
stddraw.setXscale(0, 800)
stddraw.setYscale(0, 600)

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
        
        stddraw.setPenColor(stddraw.GREEN)
        stddraw.rectangle(self.x, self.y, self.width, self.height)
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
        self.speed = 15              # Speed of the missile

    def update(self):
        # Update missile position based on angle and speed
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)

    def draw(self):
        # Draw the missile as a small circle
        stddraw.setPenColor(stddraw.RED)
        stddraw.filledCircle(self.x, self.y, 3)

def main():
    # Create a shooter object
    shooter = Shooter(400, 50, 50, 20)  # Centered at the bottom

    # Game loop
    while True:
        # check for input
        if stddraw.hasNextKeyTyped():
            key = stddraw.nextKeyTyped()
            if key == 'a':  # Move left
                shooter.move_left()
            elif key == 'd':  # Move right
                shooter.move_right(800)
            elif key == 'w':  # Rotate turret up
                shooter.rotate_turret(10)
            elif key == 's':  # Rotate turret down
                shooter.rotate_turret(-10)
            elif key == ' ':  # Shoot missile
                shooter.shoot_missile()

        # Update missiles
        for missile in shooter.missiles:
            missile.update()

        
        stddraw.clear()

        shooter.draw()

        stddraw.show(50)  # 50ms delay


if __name__ == "__main__":
    main()


