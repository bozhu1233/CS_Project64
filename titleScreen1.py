import stddraw
import stdio
import random
import sys
import array

# Screen dimensions
WIDTH, HEIGHT = 800, 600
stddraw.setCanvasSize(WIDTH, HEIGHT)
stddraw.setXscale(0, WIDTH)
stddraw.setYscale(0, HEIGHT)


BLACK = stddraw.BLACK
WHITE = stddraw.WHITE
YELLOW = stddraw.YELLOW

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


stars = [Star() for i in range(100)]


def main():
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
            "A to Move Left, D to Move Right",
            "Q to Quit",
            "R to Rotate Right, E to Rotate Left"
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


if __name__ == "__main__":
    main()
