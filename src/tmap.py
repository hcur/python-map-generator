import numpy as np
import opensimplex
import time


class Tile:

    def __init__(self, x, y, char, color):
        self.x = x
        self.y = y
        self.char = char
        self.color = color


class Tilemap:

    def __init__(self, maxx, maxy):
        # i've got the height/elevation map numbers seperate from the tiles
        # list for performance reasons. it's been a while since i timed things
        # up and i don't have any hard data on hand but i suspect this is
        # faster (because of numpy).
        self.heightmap = np.zeros(shape=(maxy, maxx), dtype=np.single)

    def mapTiles(self):
        self.tiles = []
        append_row = []

        for row in self.heightmap:
            for z in row:
                # TODO: a rules function should be implemented.
                #       this would map each elevation to a terrain
                #       type (i.e: mountains, grass, water, etc)
                #       and assign a character and a color value
                #       to output. assign it to a list and append
                #       each row to `self.tiles.`

                tile = set_chars_EXAMPLE(z, len(append_row), len(self.tiles))
                append_row.append(tile)

            self.tiles.append(append_row)
            append_row = []

    def genHeightmap(self, x, y, camera, seed=time.time_ns()):
        """
        @args:
        x: maximum x coordinate value
        y: maximum y coordinate value
        """

        def noise(nx, ny):
            return opensimplex.noise2(nx, ny) / 2 + 0.5

        def ridgenoise(nx, ny):
            return 2 * (0.5 - abs(0.6 - noise(nx, ny)))

        def n(nx, ny):
            """
            Use opensimplex to generate an elevation level from 0 to 1.0.

            @args:
            nx: X/x - 0.5
            ny: Y/y - 0.5

            See links:
             https://www.redblobgames.com/articles/noise/introduction.html
             https://www.redblobgames.com/maps/terrain-from-noise/
            for reference.
            """

            i0 = 1.00 * ridgenoise(1 * nx + 0.5, 1 * ny - 0.7)
            i1 = 0.50 * ridgenoise(2 * nx + 5.3, 2 * ny + 9.1) * i0
            i2 = 0.25 * ridgenoise(4 * nx + 17.8, 4 * ny + 23.5) * (i0 + i1)

            i = (i0 + i1 + i2) / 1.75

            return i

        opensimplex.seed(seed)

        for Y in range(0, y):
            for X in range(0, x):
                nx = X / x - 0.5
                ny = Y / y - 0.5
                self.heightmap[Y][X] = n(nx - camera.x, ny - camera.y)


class Camera:

    def __init__(self, s):
        (self.screenHeight, self.screenWidth) = s.dimensions

    def updateCameraPlacement(self, tilemap):
        self.x = round(len(tilemap.heightmap[0]) / 2)
        self.y = round(len(tilemap.heightmap) / 2)

    def updateCameraBounds(self):
        #self.rightXBound = self.screenWidth - self.x
        self.rightXBound = round(self.x + self.screenWidth * 1/2)

        #self.leftXBound = self.screenWidth + self.x
        self.leftXBound = round(self.x - self.screenWidth * 1/2)

        #self.upperYBound = self.screenHeight - self.y
        self.upperYBound = round(self.y - self.screenHeight * 1/2)

        #self.lowerYBound = self.screenHeight + self.y
        self.lowerYBound = round(self.y + self.screenHeight * 1/2)




# EXAMPLE CODE ====
sea_level = 0.4


# generic thresholds to determine biome---adjust accordingly.
def set_chars_EXAMPLE(z, x, y):
    char = 'g'
    color = 40

    # mountains
    if z >= 0.9:
        char = 'M'
        color = 255
    elif z >= 0.8:
        char = 'm'
        color = 243
    # dark grass
    elif z >= 0.6:
        color = 22
    # water
    elif z <= sea_level:
        char = 'w'
        color = 19

    return Tile(x, y, char, color)
