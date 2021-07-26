from pathlib import Path
import random

import numpy as np
import cv2
from PIL import Image

MAX_8BIT = 255
BANN_LINE_BRIGHTNESS = 20


class Bann:
    def __init__(self, masu_size, line_size, masu_num=9, masu_color=None):
        if masu_color is None:
            masu_color = [255, 228, 181]

        # Initialize bann.
        self._masu_size = masu_size
        self._line_size = line_size
        self._masu_num = masu_num
        self._masu_color = masu_color

        # Initialize koma.
        self.koma_list = [
            Hira(Path("./images/koma/hira_o.png"), masu_size, (0, 6), 1),
            Hira(Path("./images/koma/hira_o.png"), masu_size, (1, 6), 1),
            Hira(Path("./images/koma/hira_o.png"), masu_size, (2, 6), 1),
            Hira(Path("./images/koma/hira_o.png"), masu_size, (3, 6), 1),
            Hira(Path("./images/koma/hira_o.png"), masu_size, (4, 6), 1),
            Hira(Path("./images/koma/hira_o.png"), masu_size, (5, 6), 1),
            Hira(Path("./images/koma/hira_o.png"), masu_size, (6, 6), 1),
            Hira(Path("./images/koma/hira_o.png"), masu_size, (7, 6), 1),
            Hira(Path("./images/koma/hira_o.png"), masu_size, (8, 6), 1),
            Syuninn(Path("./images/koma/syuninn_o.png"), masu_size, (0, 8), 1),
            Syuninn(Path("./images/koma/syuninn_o.png"), masu_size, (8, 8), 1),
            Kakaricho(Path("./images/koma/kakaricho_o.png"), masu_size, (1, 8), 1),
            Kakaricho(Path("./images/koma/kakaricho_o.png"), masu_size, (7, 8), 1),
            Kacho(Path("./images/koma/kacho_o.png"), masu_size, (2, 8), 1),
            Kacho(Path("./images/koma/kacho_o.png"), masu_size, (6, 8), 1),
            Bucho(Path("./images/koma/bucho_o.png"), masu_size, (3, 8), 1),
            Bucho(Path("./images/koma/bucho_o.png"), masu_size, (5, 8), 1),
            Honnbucho(Path("./images/koma/honbucho_o.png"), masu_size, (1, 7), 1),
            Yakuinn(Path("./images/koma/yakuin_o.png"), masu_size, (7, 7), 1),
            Shacho(Path("./images/koma/syacho_o.png"), masu_size, (4, 8), 1),
            # ----------------------------- #
            Hira(Path("./images/koma/hira_o.png"), masu_size, (0, 2), -1),
            Hira(Path("./images/koma/hira_o.png"), masu_size, (1, 2), -1),
            Hira(Path("./images/koma/hira_o.png"), masu_size, (2, 2), -1),
            Hira(Path("./images/koma/hira_o.png"), masu_size, (3, 2), -1),
            Hira(Path("./images/koma/hira_o.png"), masu_size, (4, 2), -1),
            Hira(Path("./images/koma/hira_o.png"), masu_size, (5, 2), -1),
            Hira(Path("./images/koma/hira_o.png"), masu_size, (6, 2), -1),
            Hira(Path("./images/koma/hira_o.png"), masu_size, (7, 2), -1),
            Hira(Path("./images/koma/hira_o.png"), masu_size, (8, 2), -1),
            Syuninn(Path("./images/koma/syuninn_o.png"), masu_size, (0, 0), -1),
            Syuninn(Path("./images/koma/syuninn_o.png"), masu_size, (8, 0), -1),
            Kakaricho(Path("./images/koma/kakaricho_o.png"), masu_size, (1, 0), -1),
            Kakaricho(Path("./images/koma/kakaricho_o.png"), masu_size, (7, 0), -1),
            Kacho(Path("./images/koma/kacho_o.png"), masu_size, (2, 0), -1),
            Kacho(Path("./images/koma/kacho_o.png"), masu_size, (6, 0), -1),
            Bucho(Path("./images/koma/bucho_o.png"), masu_size, (3, 0), -1),
            Bucho(Path("./images/koma/bucho_o.png"), masu_size, (5, 0), -1),
            Honnbucho(Path("./images/koma/honbucho_o.png"), masu_size, (7, 1), -1),
            Yakuinn(Path("./images/koma/yakuin_o.png"), masu_size, (1, 1), -1),
            Shacho(Path("./images/koma/syacho_o.png"), masu_size, (4, 0), -1)
        ]

        # Initialize match.
        self.activated_koma = None

        players = [-1, 1]
        self.current_player = random.choice(players)
        print("Player {}'s turn!".format(self.current_player))

    def bann_img_generator(self):
        bann_size = self._masu_size * self._masu_num + self._line_size * (self._masu_num + 1)
        bann = np.ones((bann_size, bann_size, 3), dtype=np.uint8) * BANN_LINE_BRIGHTNESS

        for i in range(self._masu_num):
            ini_y = self._line_size * (i + 1) + self._masu_size * i
            for j in range(self._masu_num):
                ini_x = self._line_size * (j + 1) + self._masu_size * j
                bann[ini_y: ini_y + self._masu_size, ini_x: ini_x + self._masu_size] = self._masu_color

        return bann

    def koma_img_generator(self):
        bann_size = self._masu_size * self._masu_num + self._line_size * (self._masu_num + 1)
        dst = np.zeros((bann_size, bann_size, 4), dtype=np.uint8)

        for koma in self.koma_list:
            x, y = koma.getPosition()
            ini_x = self._line_size * (x + 1) + self._masu_size * x
            ini_y = self._line_size * (y + 1) + self._masu_size * y

            img = np.array(koma.getImage())
            if koma.player_id == 1:
                pass
            else:
                img = img[::-1, :, :]

            dst[ini_y: ini_y + self._masu_size, ini_x: ini_x + self._masu_size] = img

        return dst

    def get_current_bann(self):
        bann_img = self.bann_img_generator()
        koma_img = self.koma_img_generator()

        dst = self.alphaCombine(bann_img, koma_img)

        return dst

    def key_event_handler(self, event):
        step = self._masu_size + self._line_size

        if event.x % step <= self._line_size or event.y % step <= self._line_size:  # Event position is on the lines.
            return 0, 0
        else:
            x, y = int(event.x / step), int(event.y / step)
            if self.activated_koma is None:
                new_koma_list = []  # Activated koma will be removed.
                for koma in self.koma_list:
                    koma_x, koma_y = koma.getPosition()
                    if x == koma_x and y == koma_y and self.current_player == koma.getPlayerID():
                        self.activated_koma = koma
                    else:
                        new_koma_list.append(koma)
                self.koma_list = new_koma_list
                return 0, 0
            else:  # Koma is already active, so update the koma's position according to the situation.
                if self.activated_koma.movable(x, y, self.koma_list, self.current_player):
                    # If there is another koma in the destination,
                    # do nothing when the koma is current player's one.
                    # remove the koma when it's next player's one.
                    new_koma_list = []
                    for koma in self.koma_list:
                        koma_x, koma_y = koma.getPosition()
                        if x == koma_x and y == koma_y and self.current_player != koma.getPlayerID():
                            pass
                        else:
                            new_koma_list.append(koma)

                    self.activated_koma.setPosition((x, y))
                    new_koma_list.append(self.activated_koma)
                    self.koma_list = new_koma_list
                    self.activated_koma = None

                    # Change player
                    player_tmp = self.current_player
                    self.current_player = - player_tmp
                    print("Player {}'s turn!".format(self.current_player))

                    updated_bann = self.get_current_bann()
                    return 1, updated_bann

                else:  # Koma cannot move to the event position.
                    self.koma_list.append(self.activated_koma)
                    self.activated_koma = None
                    return 0, 0

    @staticmethod
    def alphaCombine(back_img, front_img):
        back_img = back_img.astype(np.float32)
        front_img = front_img.astype(np.float32)

        alpha = front_img[..., 3]
        alpha = cv2.cvtColor(alpha, cv2.COLOR_GRAY2BGR)
        alpha = alpha / MAX_8BIT

        front_img = front_img[..., :3]

        back_img *= 1 - alpha
        back_img += front_img * alpha

        return back_img.astype(np.uint8)


class Koma:
    def __init__(self, path, size, position, player_id):
        self._img = Image.open(path).resize((size, size))
        self.position = position
        self.player_id = player_id

    def getImage(self):
        return self._img

    def getPosition(self):
        return self.position

    def setPosition(self, position):
        self.position = position

    def getPlayerID(self):
        return self.player_id

    def movable(self, nextpos_x, nextpos_y, koma_list, current_player):
        raise NotImplementedError


class Hira(Koma):
    def __init__(self, path, size, position, player_id):
        super().__init__(path, size, position, player_id)

    def movable(self, nextpos_x, nextpos_y, koma_list, current_player):
        for koma in koma_list:
            koma_x, koma_y = koma.getPosition()
            if koma_x == nextpos_x and koma_y == nextpos_y and current_player == koma.getPlayerID():
                return False

        currentpos_x, currentpos_y = self.getPosition()
        if currentpos_y - nextpos_y == self.player_id and currentpos_x == nextpos_x:
            return True
        else:
            return False


class Syuninn(Koma):
    def __init__(self, path, size, position, player_id):
        super().__init__(path, size, position, player_id)

    def movable(self, nextpos_x, nextpos_y, koma_list, current_player):
        for koma in koma_list:
            koma_x, koma_y = koma.getPosition()
            if koma_x == nextpos_x and koma_y == nextpos_y and current_player == koma.getPlayerID():
                return False

        currentpos_x, currentpos_y = self.getPosition()
        if currentpos_y - nextpos_y == self.player_id and abs(currentpos_x - nextpos_x) <= 1:
            return True
        elif currentpos_y - nextpos_y == - self.player_id and currentpos_x == nextpos_x:
            return True
        else:
            return False


class Kakaricho(Koma):
    def __init__(self, path, size, position, player_id):
        super().__init__(path, size, position, player_id)

    def movable(self, nextpos_x, nextpos_y, koma_list, current_player):
        for koma in koma_list:
            koma_x, koma_y = koma.getPosition()
            if koma_x == nextpos_x and koma_y == nextpos_y and current_player == koma.getPlayerID():
                return False

        currentpos_x, currentpos_y = self.getPosition()
        if currentpos_y - nextpos_y <= self.player_id * 2 and currentpos_x == nextpos_x:
            return True
        elif currentpos_y - nextpos_y == - self.player_id and currentpos_x == nextpos_x:
            return True
        else:
            return False


class Kacho(Koma):
    def __init__(self, path, size, position, player_id):
        super().__init__(path, size, position, player_id)

    def movable(self, nextpos_x, nextpos_y, koma_list, current_player):
        for koma in koma_list:
            koma_x, koma_y = koma.getPosition()
            if koma_x == nextpos_x and koma_y == nextpos_y and current_player == koma.getPlayerID():
                return False

        currentpos_x, currentpos_y = self.getPosition()
        if currentpos_y - nextpos_y == self.player_id and abs(currentpos_x - nextpos_x) <= 1:
            return True
        elif currentpos_y - nextpos_y == - self.player_id and abs(currentpos_x - nextpos_x) == 1:
            return True
        else:
            return False


class Bucho(Koma):
    def __init__(self, path, size, position, player_id):
        super().__init__(path, size, position, player_id)

    def movable(self, nextpos_x, nextpos_y, koma_list, current_player):
        for koma in koma_list:
            koma_x, koma_y = koma.getPosition()
            if koma_x == nextpos_x and koma_y == nextpos_y and current_player == koma.getPlayerID():
                return False

        currentpos_x, currentpos_y = self.getPosition()
        if currentpos_y - nextpos_y == self.player_id and abs(currentpos_x - nextpos_x) <= 1:
            return True
        elif currentpos_y - nextpos_y == 0:
            return True
        elif currentpos_y - nextpos_y == - self.player_id and currentpos_x == nextpos_x:
            return True
        else:
            return False


class Shacho(Koma):
    def __init__(self, path, size, position, player_id):
        super().__init__(path, size, position, player_id)

    def movable(self, nextpos_x, nextpos_y, koma_list, current_player):
        for koma in koma_list:
            koma_x, koma_y = koma.getPosition()
            if koma_x == nextpos_x and koma_y == nextpos_y and current_player == koma.getPlayerID():
                return False

        currentpos_x, currentpos_y = self.getPosition()
        if abs(currentpos_y - nextpos_y) <= 1 and abs(currentpos_x - nextpos_x) <= 1:
            return True
        else:
            return False


class Honnbucho(Koma):
    def __init__(self, path, size, position, player_id):
        super().__init__(path, size, position, player_id)

    def movable(self, nextpos_x, nextpos_y, koma_list, current_player):
        for koma in koma_list:
            koma_x, koma_y = koma.getPosition()
            if koma_x == nextpos_x and koma_y == nextpos_y and current_player == koma.getPlayerID():
                return False

        currentpos_x, currentpos_y = self.getPosition()
        if abs(currentpos_y - nextpos_y) == abs(currentpos_x - nextpos_x):
            return True
        else:
            return False


class Yakuinn(Koma):
    def __init__(self, path, size, position, player_id):
        super().__init__(path, size, position, player_id)

    def movable(self, nextpos_x, nextpos_y, koma_list, current_player):
        currentpos_x, currentpos_y = self.getPosition()
        a_x = currentpos_x - nextpos_x
        a_y = currentpos_y - nextpos_y

        if a_x != 0 and a_y != 0:
            return False
        else:
            for koma in koma_list:
                koma_x, koma_y = koma.getPosition()
                b_x = currentpos_x - koma_x
                b_y = currentpos_y - koma_y
                if a_x == b_x and a_y == b_y and current_player == koma.getPlayerID():
                    return False
                elif a_x == b_x and a_y == b_y and current_player != koma.getPlayerID():
                    return True
                elif b_y != 0 and a_x == b_x and a_y / b_y > 1:
                    return False
                elif b_x != 0 and a_x / b_x > 1 and a_y == b_y:
                    return False

            return True
