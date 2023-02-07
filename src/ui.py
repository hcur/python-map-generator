import asciimatics
from asciimatics.screen import Screen
from tmap import Tile, Tilemap, Camera

def demo(screen):
    # tilemap in any other circumstance would probably be
    # larger than field of view. camera class is used to
    # limit the area printed to screen at any given time.
    camera = Camera(screen)

    # generate the map
    tilemap = Tilemap(camera.screenWidth, camera.screenHeight)

    # place the camera---in a game, this would be the character (probably)
    camera.updateCameraPlacement(tilemap)

    # update field of view
    camera.updateCameraBounds()

    # generate elevation values
    tilemap.genHeightmap(camera.screenWidth, camera.screenHeight, camera)

    # map landscape
    tilemap.mapTiles()

    while True:
        # iterate over each tile in the range of vision (based on window size)
        # and print the associated character in the associated color
        for row in tilemap.tiles:
            for tile in row:
                if tile.x <= camera.rightXBound and \
                   tile.x >= camera.leftXBound and \
                   tile.y >= camera.upperYBound and \
                   tile.y <= camera.lowerYBound:
                    screen.print_at(tile.char,
                                    tile.x,
                                    tile.y,
                                    colour=tile.color,
                                    bg=0)

        screen.refresh()

        # quit when 'q' is pressed
        ev = screen.get_key()
        if ev in (ord('Q'), ord('q')):
            return


Screen.wrapper(demo)
