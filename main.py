import random
import pygame


pygame.init()


class Information:
    # colors
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    BACKGROUND_COLOR = (10, 32, 75)
    BLOCKS_COLORS = [
        (95, 239, 247),
        (32, 83, 232),
        (30, 95, 144)
    ]

    # Padding
    SIDE_PAD = 100
    TOP_PAD = 150
    FIXED_FOR_MIN = 10

    lst = []
    min_val = max_val = block_width = block_height = start_x = 0

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode([width, height])
        pygame.display.set_caption("Sorting Algorithm Visualization")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst) - self.FIXED_FOR_MIN
        self.max_val = max(lst) + self.FIXED_FOR_MIN
        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.block_height = (self.height - self.TOP_PAD) // (self.max_val - self.min_val)
        self.start_x = self.SIDE_PAD // 2


def generate_list(n, min_value, max_value):
    lst = []
    for i in range(n):
        lst.append(random.randint(min_value, max_value))
    return lst


def draw_list(info, re_write=False, lst=None):
    found_greed = True
    if lst is None:
        lst = []

    if re_write:
        clear_rect = (info.SIDE_PAD // 2, info.TOP_PAD,
                      info.width - info.SIDE_PAD, info.height - info.TOP_PAD)
        pygame.draw.rect(info.window, info.BACKGROUND_COLOR, clear_rect)

    for i, val in enumerate(info.lst):
        x = info.start_x + i * info.block_width
        y = info.height - (val - info.min_val) * info.block_height
        color = info.BLOCKS_COLORS[i % 3]
        if i in lst:
            if found_greed:
                color = info.RED
                found_greed = False
            else:
                color = info.GREEN
        pygame.draw.rect(info.window, color, (x, y, info.block_width, info.height))

    if re_write:
        pygame.display.update()


class Button:
    colors = [pygame.Color('lightskyblue3'), (255, 255, 255), (146, 126, 233)]
    base_font = pygame.font.SysFont('comicsans', 22)
    active = 1

    def __init__(self, x, y, txt, button_width, button_height):
        self.text_surface = self.base_font.render(txt, True, (0, 0, 0))
        self.width = button_width
        self.height = button_height
        self.x = x
        self.y = y
        self.input_rect = pygame.Rect(x, y, self.width, self.height)

    def show(self, info):
        pygame.draw.rect(info.window, self.colors[self.active], self.input_rect)
        x = self.x + ((self.width - self.text_surface.get_width()) // 2)
        info.window.blit(self.text_surface, (x, self.y - 6))

    def click(self, mouse):
        return self.x <= mouse[0] <= self.x + self.width and self.y <= mouse[1] <= self.y + self.height

    def update(self, mouse, is_clicked=False):
        if is_clicked:
            self.active = 2
        elif self.x <= mouse[0] <= self.x + self.width and self.y <= mouse[1] <= self.y + self.height:
            self.active = 0
        else:
            self.active = 1

    def set_str(self, txt):
        self.text_surface = self.base_font.render(txt, True, (0, 0, 0))


def draw(info, btn):
    info.window.fill(info.BACKGROUND_COLOR)
    draw_list(info)
    for i in btn:
        i.show(info)
    pygame.display.update()


def insertion_sort(info):
    for i in range(1, len(info.lst)):
        current = info.lst[i]
        while True:
            ascending_sort = i > 0 and info.lst[i - 1] > current
            if not ascending_sort:
                break
            info.lst[i] = info.lst[i - 1]
            i = i - 1
            info.lst[i] = current
            draw_list(info, True, [i - 1, i])
            yield True


def bubble_sort(info):
    for i in range(len(info.lst) - 1):
        for j in range(len(info.lst) - 1 - i):
            num1 = info.lst[j]
            num2 = info.lst[j + 1]

            if num1 > num2:
                info.lst[j], info.lst[j + 1] = info.lst[j + 1], info.lst[j]
                draw_list(info, True, [j, j + 1])
                yield True


def merge_sort(info):
    for i in merge_sort_yield(info.lst):
        info.set_list(i)
        yield True
        draw_list(info, True)


def merge_sort_yield(arr):
    def merge_sort_rec(start, end):
        if end - start > 1:
            middle = (start + end) // 2
            yield from merge_sort_rec(start, middle)
            yield from merge_sort_rec(middle, end)
            left = arr[start:middle]
            right = arr[middle:end]
            a = 0
            b = 0
            c = start
            while a < len(left) and b < len(right):
                if left[a] < right[b]:
                    arr[c] = left[a]
                    a += 1
                else:
                    arr[c] = right[b]
                    b += 1
                c += 1

            while a < len(left):
                arr[c] = left[a]
                a += 1
                c += 1

            while b < len(right):
                arr[c] = right[b]
                b += 1
                c += 1
            yield arr

    yield from merge_sort_rec(0, len(arr))  # call inner function with start/end arguments


def running():
    run = True
    clock = pygame.time.Clock()
    n = 100
    min_val = 10
    max_val = 100
    lst = generate_list(n, min_val, max_val)
    info = Information(800, 600, lst)
    pad_btn_buttons = 25
    button_width = 150
    button_height = 30

    start_button = Button(info.start_x, pad_btn_buttons, "Start", button_width, button_height)

    bubble_sort_button = Button(info.start_x + pad_btn_buttons + button_width, pad_btn_buttons,
                                'Bubble sort', button_width, button_height)

    insertion_sort_button = Button(info.start_x + 2 * pad_btn_buttons + 2 * button_width, pad_btn_buttons,
                                   'Insertion sort', button_width, button_height)

    merge_sort_button = Button(info.start_x + 3 * pad_btn_buttons + 3 * button_width, pad_btn_buttons,
                               'Merge sort', button_width, button_height)

    button_width = 110
    stop_button = Button(info.start_x, pad_btn_buttons + 2 * pad_btn_buttons, 'Stop',
                         button_width, button_height)

    increase_speed = Button(info.start_x + pad_btn_buttons + button_width,
                            pad_btn_buttons + 2 * pad_btn_buttons, '+', button_height, button_height)

    speed_button = Button(info.start_x + pad_btn_buttons + button_width + button_height,
                          pad_btn_buttons + 2 * pad_btn_buttons, 'Speed : 10', 120, button_height)

    decrease_speed = Button(info.start_x + pad_btn_buttons + button_width + button_height + 120,
                            pad_btn_buttons + 2 * pad_btn_buttons, '-', button_height, button_height)

    rest_button = Button(info.start_x + 2 * pad_btn_buttons + button_width + button_height + 120 + button_height,
                         pad_btn_buttons + 2 * pad_btn_buttons, 'Generate', button_width, button_height)

    increase_num = Button(info.start_x + 3 * pad_btn_buttons + 2 * button_width + button_height + 120 + button_height,
                          pad_btn_buttons + 2 * pad_btn_buttons, '+', button_height, button_height)

    num_button = Button(info.start_x + 3 * pad_btn_buttons + 2 * button_width + 2 * button_height + 120 + button_height,
                        pad_btn_buttons + 2 * pad_btn_buttons, '#Nums : 100', 150, button_height)

    decrease_num = Button(
        info.start_x + 3 * pad_btn_buttons + 2 * button_width + 2 * button_height + 270 + button_height,
        pad_btn_buttons + 2 * pad_btn_buttons, '-', button_height, button_height)

    btn = [start_button, stop_button, bubble_sort_button, insertion_sort_button, merge_sort_button,
           increase_speed, speed_button, decrease_speed, rest_button, increase_num, num_button, decrease_num]

    start = False
    sorting_algorithm = bubble_sort
    sorting_algorithm_generator = None
    clicked = 2
    current_speed = 20
    while run:

        clock.tick(5 * current_speed)

        for event in pygame.event.get():
            mouse = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.click(mouse):
                    sorting_algorithm_generator = sorting_algorithm(info)
                    start = True
                elif stop_button.click(mouse):
                    start = False
                elif bubble_sort_button.click(mouse):
                    sorting_algorithm = bubble_sort
                    clicked = 2
                    start = False
                elif insertion_sort_button.click(mouse):
                    sorting_algorithm = insertion_sort
                    clicked = 3
                    start = False
                elif merge_sort_button.click(mouse):
                    sorting_algorithm = merge_sort
                    clicked = 4
                    start = False
                elif increase_speed.click(mouse):
                    start = False
                    if current_speed < 20:
                        current_speed += 2
                        speed_button.set_str('Speed : ' + str(current_speed // 2))
                elif decrease_speed.click(mouse):
                    start = False
                    if current_speed > 2:
                        current_speed -= 2
                        speed_button.set_str('Speed : ' + str(current_speed // 2))
                elif rest_button.click(mouse):
                    info.set_list(generate_list(n, min_val, max_val))
                    start = False
                elif increase_num.click(mouse):
                    start = False
                    if n < 100:
                        n += 10
                        info.set_list(generate_list(n, min_val, max_val))
                        num_button.set_str('#Nums : ' + str(n))
                elif decrease_num.click(mouse):
                    start = False
                    if n > 10:
                        n -= 10
                        info.set_list(generate_list(n, min_val, max_val))
                        num_button.set_str('#Nums : ' + str(n))

        for i in range(len(btn)):
            # avoid speed Label and num label
            if i != 6 and i != 10:
                btn[i].update(pygame.mouse.get_pos(), (i == clicked))

        if start:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                print('DONE')
                start = False
        else:
            draw(info, btn)
    pygame.quit()


if __name__ == "__main__":
    running()