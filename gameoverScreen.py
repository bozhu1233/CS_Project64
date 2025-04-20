import stdio
import stddraw
import random
import sys

# Screen dimensions
WIDTH = 800
HEIGHT = 600
stddraw.setCanvasSize(WIDTH, HEIGHT)
stddraw.setXscale(0, WIDTH)
stddraw.setYscale(0, HEIGHT)

BLACK = stddraw.BLACK
WHITE = stddraw.WHITE
YELLOW =stddraw.YELLOW
RED = stddraw.RED
GREEN = stddraw.GREEN

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


stars = [Star() for i in range(100)]

def game_over():
    
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
        #stddraw.text(WIDTH/2, HEIGHT/2 - 30, f"Score: {score}")
        
        # Instructions
        stddraw.text(WIDTH/2, HEIGHT/2 - 60, "Press 'R' to restart")
        stddraw.text(WIDTH/2, HEIGHT/2 - 90, "Press 'Q' to quit")
        
        stddraw.show(20)

        if stddraw.hasNextKeyTyped():
            key = stddraw.nextKeyTyped().lower()
            if key == 'r':
                return True
            elif key == 'q':
                sys.exit()

def game_won():
    
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
        #stddraw.text(WIDTH/2, HEIGHT/2 - 30, f"Score: {score}")
        
        # Instructions
        stddraw.text(WIDTH/2, HEIGHT/2 - 60, "Press 'R' to play again")
        stddraw.text(WIDTH/2, HEIGHT/2 - 90, "Press 'Q' to quit")
        
        stddraw.show(20)

        if stddraw.hasNextKeyTyped():
            key = stddraw.nextKeyTyped().lower()
            if key == 'r':
                return True
            elif key == 'q':
                sys.exit()


if __name__ == "__main__":
    
