
from graphics import Canvas
import random
import time

# The size of the canvas
CANVAS_WIDTH = 500
CANVAS_HEIGHT = 1000

SQUARE_SIZE = 25

DELAY = 0.1
SNOWFLAKE_DIAMETER = 10


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
            which_object = random.randint(0, 3)
            if which_object == 0:
                objects = two_times_two(canvas, objects)

            if which_object == 1:
                objects = the_el(canvas, objects)

            if which_object == 2:
                objects = the_i(canvas, objects)

            if which_object == 3:
                objects = pyramid(canvas, objects)

        animate_objects(canvas, objects)

        canvas.update()
        time.sleep(DELAY)

    canvas.mainloop()


def animate_objects(canvas, objects):

    presses = canvas.get_new_key_presses()

    objects_on = False
    counter = 0
    turn_left = False
    turn_right = False
    hit = False
    most_left = 500
    most_right = 0
    left_square = []
    right_square = []

    for elem in objects:
        most_left = min(most_left, canvas.get_left_x(elem))

        most_right = max(most_right, canvas.get_left_x(elem))


    for elem in objects:
        stop = on_the_path(canvas, elem)
        if stop is True:
            objects_on = True
            hit = True
            break
        elif canvas.get_top_y(elem) + canvas.get_height(elem) >= canvas.get_canvas_height():
            objects_on = True
            hit = True
            break
        else:
            counter += 1
            for press in presses:
                turn_left = False
                turn_right = False
                if press.keysym == 'a':

                    canvas.move(elem, -25, 0)
                    stop = on_the_path(canvas, elem)
                    if stop is True:
                        canvas.move(elem, 25, 0)
                elif press.keysym == 'd':
                    canvas.move(elem, 25, 0)
                    stop = on_the_path(canvas, elem)
                    if stop is True:
                        canvas.move(elem, 25, 0)
                        #stop = on_the_path(canvas, elem)
                        #if stop is True:
                        #    canvas.move(elem, -25, 0)
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
                break
            hit = False
            if turn_left is True:
                canvas.move(elem, 25, 0)
            if turn_right is True:
                canvas.move(elem, -25, 0)

            canvas.move(elem, 0, 25)

    fun = 0
    if objects_on is True:
        for elem in objects:
            fun += 1
            canvas.move(elem, 0, -25)
            if fun <= counter:
                canvas.move(elem, 0, -25)
        objects.clear()


    if hit is True:
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
    if stop is True:
        canvas.move(square, 25, 0)
        return True
    if canvas.get_left_x(square) < 1.5:
        canvas.move(square, 25, 0)
        return True
    return False


def is_right_full(canvas, square):
    canvas.move(square, -25, 0)
    stop = on_the_path(canvas, square)
    if stop is True:
        canvas.move(square, 25, 0)
        return True
    if canvas.get_left_x(square) < 1.5:
        canvas.move(square, 25, 0)
        return True
    return False


if __name__ == '__main__':
    main()
