
from graphics import Canvas
import random
import time

# The size of the canvas
CANVAS_WIDTH = 500
CANVAS_HEIGHT = 1000

SQUARE_SIZE = 25

DELAY = 0.1
SNOWFLAKE_DIAMETER = 10

all_squares = []


def main():
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    canvas.set_canvas_title("Snow")

    canvas.set_canvas_background_color("black")

    for line in range(100):
        line = canvas.create_line(0, line * SQUARE_SIZE, canvas.get_canvas_width(), line * SQUARE_SIZE)
        canvas.set_fill_color(line, "white")

    for line in range(20):
        line = canvas.create_line(line * SQUARE_SIZE, 0, line * SQUARE_SIZE, canvas.get_canvas_height())
        canvas.set_fill_color(line, "white")

    #set up

    objects = []


    #Animation Loop
    while True:
        #move all snowflakes
        #make new snow
        if len(objects) < 1:
            is_line_full(canvas)
            random_object = random.randint(0, 6)
            print(random_object)
            if random_object == 0:
                objects = two_times_two(canvas, objects)

            if random_object == 1:
                objects = the_el(canvas, objects)

            if random_object == 2:
                objects = the_i(canvas, objects)

            if random_object == 3:
                objects = the_j(canvas, objects)

            if random_object == 4:
                objects = the_z(canvas, objects)

            if random_object == 5:
                objects = the_s(canvas, objects)

            if random_object == 6:
                objects = pyramid(canvas, objects)

        animate_objects(canvas, objects)

        canvas.update()
        time.sleep(DELAY)

    canvas.mainloop()


def animate_objects(canvas, objects):

    global all_squares

    #lets all the objects get back at the right position after it´s supposed to stop.
    correct_objects = False
    counter = 0
    equal_to_counter = 0

    #clears the list after the object doesn´t move
    remove = False

    #discovers the left and right most squares, helps you move to the left and right
    most_left = 500
    most_right = 0
    left_square = []
    right_square = []
    full_left = False
    full_right = False

    clicked_a = False
    clicked_d = False

    for elem in objects:
        most_left = min(most_left, canvas.get_left_x(elem))
        if canvas.get_left_x(elem) == most_left:
            left_square.clear()
            left_square.append(elem)

        most_right = max(most_right, canvas.get_left_x(elem))
        if canvas.get_left_x(elem) == most_right:
            right_square.clear()
            right_square.append(elem)
        all_squares.append(elem)

    presses = canvas.get_new_key_presses()

    for press in presses:

        if press.keysym == 'a':
            full_left = is_left_full(canvas, left_square[0])
            clicked_a = True

        elif press.keysym == 'd':
            full_right = is_right_full(canvas, right_square[0])
            clicked_d = True

        if press.keysym == 'space':
            pause = canvas.create_text(canvas.get_canvas_width() / 2,
                                       canvas.get_canvas_height() / 2,
                                       "Pause")
            canvas.set_fill_color(pause, "green")
            canvas.set_font(pause, "Times", 50)
            canvas.wait_for_click()
            canvas.delete(pause)
            presses = canvas.get_new_key_presses()
            break

    for elem in objects:
        stop = on_the_path(canvas, elem)
        if stop is True:
            correct_objects = True
            remove = True
            break
        elif canvas.get_top_y(elem) + canvas.get_height(elem) >= canvas.get_canvas_height():
            correct_objects = True
            remove = True
            break
        else:
            counter += 1
            if clicked_a is True:
                if full_left is False:
                    canvas.move(elem, -25, 0)
            if clicked_d is True:
                if full_right is False:
                    canvas.move(elem, 25, 0)

            remove = False

            canvas.move(elem, 0, 25)

    if correct_objects is True:
        for elem in objects:
            equal_to_counter += 1
            canvas.move(elem, 0, -25)
            if equal_to_counter <= counter:
                canvas.move(elem, 0, -25)
        objects.clear()

    if remove is True:
        objects.clear()


def on_the_path(canvas, objects):

    object_coords = canvas.coords(objects)

    x1 = object_coords[0]
    y1 = object_coords[1]
    x2 = object_coords[2]
    y2 = object_coords[3]

    overlapping_objects_bot = canvas.find_overlapping(x1, y2, x2, y2)
    overlapping_objects_left = canvas.find_overlapping(x1, y1, x1, y2)
    overlapping_objects_right = canvas.find_overlapping(x2, y1, x2, y2)

    if len(overlapping_objects_bot) >= 2:
        return True
    if len(overlapping_objects_left) >= 2:
        return True
    if len(overlapping_objects_right) >= 2:
        return True
    return False


def create_square(canvas, x, y, color):

    global SQUARE_SIZE

    square = canvas.create_rectangle(x - int(SQUARE_SIZE / 2) + 1, y - 1, x + int(SQUARE_SIZE / 2) - 1, y - SQUARE_SIZE + 1)

    canvas.set_fill_color(square, color)
    canvas.set_outline_color(square, "grey")
    return square


def two_times_two(canvas, objects):

    y = 0 - SQUARE_SIZE
    ran_col = random.randint(0, 8)

    color = ran_color(ran_col)


    for k in range(2):
        x = (canvas.get_canvas_width() - SQUARE_SIZE) / 2
        for i in range(2):
            square = create_square(canvas, x, y, color)
            objects.append(square)
            x += SQUARE_SIZE
        y -= SQUARE_SIZE

    return objects


def the_el(canvas, objects):

    y = 0 - SQUARE_SIZE
    ran_col = random.randint(0, 8)

    color = ran_color(ran_col)

    x = (canvas.get_canvas_width() - SQUARE_SIZE) / 2
    square = create_square(canvas, x, y, color)
    y -= SQUARE_SIZE
    objects.append(square)
    for i in range(3):
        square = create_square(canvas, x, y, color)
        objects.append(square)
        x += SQUARE_SIZE

    return objects


def the_j(canvas, objects):

    y = 0 - 2 * SQUARE_SIZE
    ran_col = random.randint(0, 8)

    color = ran_color(ran_col)

    x = (canvas.get_canvas_width() - SQUARE_SIZE) / 2
    square = create_square(canvas, x, y, color)
    y += SQUARE_SIZE
    objects.append(square)
    for i in range(3):
        square = create_square(canvas, x, y, color)
        objects.append(square)
        x += SQUARE_SIZE

    return objects


def the_z(canvas, objects):

    y = 0 - 2 * SQUARE_SIZE
    x = (canvas.get_canvas_width() - SQUARE_SIZE) / 2 - 2 * SQUARE_SIZE
    ran_col = random.randint(0, 8)

    color = ran_color(ran_col)
    for i in range(2):
        x += SQUARE_SIZE
        square = create_square(canvas, x, y, color)
        objects.append(square)
    y += SQUARE_SIZE
    for i in range(2):
        square = create_square(canvas, x, y, color)
        objects.append(square)
        x += SQUARE_SIZE

    return objects


def the_s(canvas, objects):

    y = 0 - SQUARE_SIZE
    x = (canvas.get_canvas_width() - SQUARE_SIZE) / 2 - 2 * SQUARE_SIZE
    ran_col = random.randint(0, 8)

    color = ran_color(ran_col)
    for i in range(2):
        x += SQUARE_SIZE
        square = create_square(canvas, x, y, color)
        objects.append(square)
    y -= SQUARE_SIZE
    for i in range(2):
        square = create_square(canvas, x, y, color)
        objects.append(square)
        x += SQUARE_SIZE

    return objects


def the_i(canvas, objects):

    y = 0 - 2 * SQUARE_SIZE
    ran_col = random.randint(0, 8)

    color = ran_color(ran_col)

    x = (canvas.get_canvas_width() - SQUARE_SIZE) / 2
    for i in range(4):
        square = create_square(canvas, x, y, color)
        objects.append(square)
        y -= SQUARE_SIZE

    return objects

def pyramid(canvas, objects):

    y = 0
    ran_col = random.randint(0, 8)

    color = ran_color(ran_col)

    x = (canvas.get_canvas_width() - SQUARE_SIZE) / 2 - SQUARE_SIZE

    for i in range(3):
        square = create_square(canvas, x, y, color)
        objects.append(square)
        x += SQUARE_SIZE

    y -= SQUARE_SIZE
    x -= 2 * SQUARE_SIZE

    square = create_square(canvas, x, y, color)
    objects.append(square)

    return objects



def ran_color(i):
    switcher = {
        0: 'red',
        1: 'blue',
        2: 'green',
        3: 'cyan',
        4: 'lime',
        5: 'yellow',
        6: 'turquoise',
        7: 'orange',
        8: 'purple'
    }
    return switcher.get(i)


def is_left_full(canvas, square):
    canvas.move(square, -25, 0)
    stop = on_the_path(canvas, square)
    canvas.move(square, 25, 0)
    if stop is True:
        return True
    if canvas.get_left_x(square) <= 1.5:
        return True
    return False


def is_right_full(canvas, square):
    canvas.move(square, 25, 0)
    stop = on_the_path(canvas, square)
    canvas.move(square, -25, 0)
    if stop is True:
        return True
    if canvas.get_left_x(square) >= 475:
        return True
    return False


def is_line_full(canvas):

    all_squares = []

    square_coords_y = canvas.get_canvas_height() + SQUARE_SIZE / 2

    empty = False

    for k in range(44):
        square_coords_x = 0 + SQUARE_SIZE / 2
        square_coords_y -= SQUARE_SIZE
        for i in range(20):
            square_coords = canvas.find_overlapping(square_coords_x, square_coords_y, square_coords_x, square_coords_y)
            if len(square_coords) > 0:
                all_squares.append(square_coords[0])
                if empty is True:
                    for elem in all_squares:
                        canvas.move(elem, 0, 25)
                        square_coords_y -= SQUARE_SIZE
                    empty = False
                if len(all_squares) == 0 and i == 19:
                    empty = True
                if len(all_squares) == 20:
                    for elem in all_squares:
                        canvas.delete(elem)
            square_coords_x += SQUARE_SIZE
        all_squares.clear()


if __name__ == '__main__':
    main()
