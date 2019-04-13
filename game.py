import arcade
import os

SPRITE_SCALING = 0.4
SPRITE_NATIVE_SIZE = 128
SPRITE_SIZE = int(SPRITE_NATIVE_SIZE * SPRITE_SCALING)

SCREEN_WIDTH = SPRITE_SIZE * 16
SCREEN_HEIGHT = SPRITE_SIZE * 14
SCREEN_TITLE = "Ice Sliding Puzzle"

MOVEMENT_SPEED = 13


class Room:
    def __init__(self):
        self.wall_list = None

        self.background = None


def setup_room_1():
    room = Room()

    room.wall_list = arcade.SpriteList()

    for y in (0, 0):
        for x in range(0, SCREEN_WIDTH, SPRITE_SIZE):
            if (x != SPRITE_SIZE * 14) or x == 0:
                wall = arcade.Sprite("images/ice_block.png", SPRITE_SCALING)
                wall.left = x
                wall.bottom = y
                room.wall_list.append(wall)

    for y in (SCREEN_HEIGHT - SPRITE_SIZE, SCREEN_HEIGHT - SPRITE_SIZE):
        for x in range(0, SCREEN_WIDTH, SPRITE_SIZE):
                wall = arcade.Sprite("images/ice_block.png", SPRITE_SCALING)
                wall.left = x
                wall.bottom = y
                room.wall_list.append(wall)

    for x in (0, SCREEN_WIDTH - SPRITE_SIZE):
        for y in range(SPRITE_SIZE, SCREEN_HEIGHT - SPRITE_SIZE, SPRITE_SIZE):
            if (y != SPRITE_SIZE * 5 and y != SPRITE_SIZE * 6) or x == 0:
                wall = arcade.Sprite("images/ice_block.png", SPRITE_SCALING)
                wall.left = x
                wall.bottom = y
                room.wall_list.append(wall)

    coordinate_list = [[14 * SPRITE_SIZE, 4 * SPRITE_SIZE],
                       [5 * SPRITE_SIZE, 3 * SPRITE_SIZE],
                       [6 * SPRITE_SIZE, 7 * SPRITE_SIZE]]

    for coordinate in coordinate_list:
        wall = arcade.Sprite("images/ice_block.png", SPRITE_SCALING)
        wall.left = coordinate[0]
        wall.bottom = coordinate[1]
        room.wall_list.append(wall)

    room.background = arcade.load_texture("images/background_ice.jpg")

    return room


def setup_room_2():
    room = Room()

    room.wall_list = arcade.SpriteList()

    for y in (0, SCREEN_HEIGHT - SPRITE_SIZE):
        for x in range(0, SCREEN_WIDTH, SPRITE_SIZE):
            wall = arcade.Sprite("images/boxCrate_double.png", SPRITE_SCALING)
            wall.left = x
            wall.bottom = y
            room.wall_list.append(wall)

    for x in (0, SCREEN_WIDTH - SPRITE_SIZE):
        for y in range(SPRITE_SIZE, SCREEN_HEIGHT - SPRITE_SIZE, SPRITE_SIZE):
            if (y != SPRITE_SIZE * 4 and y != SPRITE_SIZE * 5 and y != SPRITE_SIZE * 6) or x != 0:
                wall = arcade.Sprite("images/boxCrate_double.png", SPRITE_SCALING)
                wall.left = x
                wall.bottom = y
                room.wall_list.append(wall)

    wall = arcade.Sprite("images/boxCrate_double.png", SPRITE_SCALING)
    wall.left = 5 * SPRITE_SIZE
    wall.bottom = 6 * SPRITE_SIZE
    room.wall_list.append(wall)
    room.background = arcade.load_texture("images/background_2.jpg")

    return room


class MyGame(arcade.Window):
    def __init__(self, width, height, title):

        super().__init__(width, height, title)

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.current_room = 0

        self.rooms = None
        self.player_sprite = None
        self.player_list = None
        self.physics_engine = None

    def setup(self):
        self.player_sprite = arcade.Sprite("images/character.png", SPRITE_SCALING)
        self.player_sprite.center_x = SCREEN_WIDTH - 75
        self.player_sprite.center_y = 30
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player_sprite)

        self.rooms = []

        room = setup_room_1()
        self.rooms.append(room)

        room = setup_room_2()
        self.rooms.append(room)

        self.current_room = 0

        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.rooms[self.current_room].wall_list)

    def on_draw(self):
        arcade.start_render()

        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.rooms[self.current_room].background)

        self.rooms[self.current_room].wall_list.draw()

        self.player_list.draw()

    def on_key_press(self, key, modifiers):
        if self.player_sprite.change_y == 0 and self.player_sprite.change_x == 0:
            if key == arcade.key.UP:
                self.player_sprite.change_y = MOVEMENT_SPEED
            elif key == arcade.key.DOWN:
                self.player_sprite.change_y = -MOVEMENT_SPEED
            elif key == arcade.key.LEFT:
                self.player_sprite.change_x = -MOVEMENT_SPEED
            elif key == arcade.key.RIGHT:
                self.player_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def update(self, delta_time):
        self.physics_engine.update()

        if self.player_sprite.center_x > SCREEN_WIDTH and self.current_room == 0:
            self.current_room = 1
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                             self.rooms[self.current_room].wall_list)
            self.player_sprite.center_x = 0
        elif self.player_sprite.center_x < 0 and self.current_room == 1:
            self.current_room = 0
            self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                             self.rooms[self.current_room].wall_list)
            self.player_sprite.center_x = SCREEN_WIDTH


def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()