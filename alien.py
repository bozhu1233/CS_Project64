import stdio, stddraw
radius = .03
aliens = [] #list for the aliens
rows, cols = 3, 5 #number of rows and columns about aliens
move_x = 0.1
move_y = 0.1
class Alien:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def draw_alien(self):
        stddraw.filledCircle(self.x,self.y, radius)

def main():
    direction = 1 #direction for the aliens 1 => right, -1 => left
    for i in range(rows): #creates a grid of aliens of rows x cols
        for j in range(cols):
            x =  j * 0.08 + 0.04
            y = 0.96 - i * 0.08
            aliens.append(Alien(x,y)) #adds the aliens positions to an array
    while True:
        stddraw.clear()
        edge = False
        for alien in aliens:
            if (alien.x >= 0.9 and direction == 1) or (alien.x <= 0.05 and direction == -1):
                edge = True
                break
        for alien in aliens:
            if edge:
                alien.move(0, -move_y)
                direction *= -1
            else: 
                alien.move(direction * move_x, 0)
        for alien in aliens:
            alien.draw_alien()
        stddraw.show(300)
   


if __name__ == '__main__':
    main()



