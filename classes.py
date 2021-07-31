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
            Hira(Path("./images/koma/hira_o.png"), masu_size, (0, 6), 1, exist=True),
            Hira(Path("./images/koma/hira_o.png"), masu_size, (1, 6), 1, exist=True),
            Hira(Path("./images/koma/hira_o.png"), masu_size, (2, 6), 1, exist=True),
            Hira(Path("./images/koma/hira_o.png"), masu_size, (3, 6), 1, exist=True),
            Hira(Path("./images/koma/hira_o.png"), masu_size, (4, 6), 1, exist=True),
            Hira(Path("./images/koma/hira_o.png"), masu_size, (5, 6), 1, exist=True),
            Hira(Path("./images/koma/hira_o.png"), masu_size, (6, 6), 1, exist=True),
            Hira(Path("./images/koma/hira_o.png"), masu_size, (7, 6), 1, exist=True),
            Hira(Path("./images/koma/hira_o.png"), masu_size, (8, 6), 1, exist=True),
            Syuninn(Path("./images/koma/syuninn_o.png"), masu_size, (0, 8), 1, exist=True),
            Syuninn(Path("./images/koma/syuninn_o.png"), masu_size, (8, 8), 1, exist=True),
            Kakaricho(Path("./images/koma/kakaricho_o.png"), masu_size, (1, 8), 1, exist=True),
            Kakaricho(Path("./images/koma/kakaricho_o.png"), masu_size, (7, 8), 1, exist=True),
            Kacho(Path("./images/koma/kacho_o.png"), masu_size, (2, 8), 1, exist=True),
            Kacho(Path("./images/koma/kacho_o.png"), masu_size, (6, 8), 1, exist=True),
            Bucho(Path("./images/koma/bucho_o.png"), masu_size, (3, 8), 1, exist=True),
            Bucho(Path("./images/koma/bucho_o.png"), masu_size, (5, 8), 1, exist=True),
            Honnbucho(Path("./images/koma/honbucho_o.png"), masu_size, (1, 7), 1, exist=True),
            Yakuinn(Path("./images/koma/yakuin_o.png"), masu_size, (7, 7), 1, exist=True),
            Shacho(Path("./images/koma/syacho_o.png"), masu_size, (4, 8), 1, exist=True),
            # ----------------------------- #
            Hira(Path("./images/koma/hira_og.png"), masu_size, (0, 2), -1, exist=True),
            Hira(Path("./images/koma/hira_og.png"), masu_size, (1, 2), -1, exist=True),
            Hira(Path("./images/koma/hira_og.png"), masu_size, (2, 2), -1, exist=True),
            Hira(Path("./images/koma/hira_og.png"), masu_size, (3, 2), -1, exist=True),
            Hira(Path("./images/koma/hira_og.png"), masu_size, (4, 2), -1, exist=True),
            Hira(Path("./images/koma/hira_og.png"), masu_size, (5, 2), -1, exist=True),
            Hira(Path("./images/koma/hira_og.png"), masu_size, (6, 2), -1, exist=True),
            Hira(Path("./images/koma/hira_og.png"), masu_size, (7, 2), -1, exist=True),
            Hira(Path("./images/koma/hira_og.png"), masu_size, (8, 2), -1, exist=True),
            Syuninn(Path("./images/koma/syuninn_og.png"), masu_size, (0, 0), -1, exist=True),
            Syuninn(Path("./images/koma/syuninn_og.png"), masu_size, (8, 0), -1, exist=True),
            Kakaricho(Path("./images/koma/kakaricho_og.png"), masu_size, (1, 0), -1, exist=True),
            Kakaricho(Path("./images/koma/kakaricho_og.png"), masu_size, (7, 0), -1, exist=True),
            Kacho(Path("./images/koma/kacho_og.png"), masu_size, (2, 0), -1, exist=True),
            Kacho(Path("./images/koma/kacho_og.png"), masu_size, (6, 0), -1, exist=True),
            Bucho(Path("./images/koma/bucho_og.png"), masu_size, (3, 0), -1, exist=True),
            Bucho(Path("./images/koma/bucho_og.png"), masu_size, (5, 0), -1, exist=True),
            Honnbucho(Path("./images/koma/honbucho_og.png"), masu_size, (7, 1), -1, exist=True),
            Yakuinn(Path("./images/koma/yakuin_og.png"), masu_size, (1, 1), -1, exist=True),
            Shacho(Path("./images/koma/syacho_og.png"), masu_size, (4, 0), -1, exist=True)
        ]

        # Initialize match.
        self.activated_koma = None

        players = [-1, 1]
        self.current_player = random.choice(players)
        print("Player {}'s turn!".format(self.current_player))

    def make_bann_img(self):
        bann_size = self._masu_size * self._masu_num + self._line_size * (self._masu_num + 1)
        bann = np.ones((bann_size, bann_size, 3), dtype=np.uint8) * BANN_LINE_BRIGHTNESS

        for i in range(self._masu_num):
            ini_y = self._line_size * (i + 1) + self._masu_size * i
            for j in range(self._masu_num):
                ini_x = self._line_size * (j + 1) + self._masu_size * j
                bann[ini_y: ini_y + self._masu_size, ini_x: ini_x + self._masu_size] = self._masu_color

        return bann

    def make_koma_img(self):
        bann_size = self._masu_size * self._masu_num + self._line_size * (self._masu_num + 1)
        dst = np.zeros((bann_size, bann_size, 4), dtype=np.uint8)

        for koma in self.koma_list:
            if koma.exist:
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

    def get_current_bann_img(self):
        bann_img = self.make_bann_img()
        koma_img = self.make_koma_img()

        dst = self.alphaCombine(bann_img, koma_img)

        return dst

    def get_koma_by_position(self, x, y):
        for i, koma in enumerate(self.koma_list):
            koma_x, koma_y = koma.getPosition()
            if x == koma_x and y == koma_y and koma.exist:
                return koma
        return None

    def key_event_handler(self, event):
        step = self._masu_size + self._line_size

        if event.x % step <= self._line_size or event.y % step <= self._line_size:  # Event position is on the lines.
            return 0, 0
        else:
            x, y = int(event.x / step), int(event.y / step)
            koma_on_event_position = self.get_koma_by_position(x, y)

            if self.activated_koma is None:
                if koma_on_event_position is not None and koma_on_event_position.getPlayerID() == self.current_player:
                    self.activated_koma = koma_on_event_position
                return 0, 0
            else:
                if self.activated_koma.movable(x, y):
                    if isinstance(self.activated_koma, (Honnbucho, Yakuinn)):
                        # Honnbucho and Yakuinn need to be examined if there's koma or not on the way to
                        # their destinations.
                        current_x, current_y = self.activated_koma.getPosition()
                        vec = [x - current_x, y - current_y]
                        vec = self.normalizeVec(vec)

                        tmp_x, tmp_y = current_x + vec[0], current_y + vec[1]
                        while True:
                            if tmp_x == x and tmp_y == y:
                                break
                            elif self.get_koma_by_position(tmp_x, tmp_y) is not None:
                                self.activated_koma = None
                                return 0, 0
                            tmp_x += vec[0]
                            tmp_y += vec[1]

                    if koma_on_event_position is None:
                        pass
                    elif koma_on_event_position.getPlayerID() == self.current_player:
                        # Current player's koma is occupying the destination.
                        self.activated_koma = None
                        return 0, 0
                    elif koma_on_event_position.getPlayerID() == - self.current_player:
                        # Next player's koma is occupying the destination.
                        self.get_koma_by_position(x, y).exist = False

                    self.activated_koma.setPosition((x, y))
                    self.activated_koma = None

                    # Update player.
                    player_tmp = self.current_player
                    self.current_player = - player_tmp
                    print("Player {}'s turn!".format(self.current_player))
                    # Update bann.
                    updated_bann = self.get_current_bann_img()
                    return 1, updated_bann

                else:
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

    @staticmethod
    def normalizeVec(vec):
        if vec[0] == 0 and vec[1] == 0:
            raise ValueError("vec is 0.")
        elif vec[0] == 0:
            return [vec[0], int(vec[1] / abs(vec[1]))]
        elif vec[1] == 0:
            return [int(vec[0] / abs(vec[0])), vec[1]]
        else:
            return [int(vec[0] / abs(vec[0])), int(vec[1] / abs(vec[1]))]


class Koma:
    def __init__(self, path, size, position, player_id, exist):
        self._img = Image.open(path).resize((size, size))
        self.position = position
        self.player_id = player_id
        self.exist = exist

    def getImage(self):
        return self._img

    def getPosition(self):
        return self.position

    def setPosition(self, position):
        self.position = position

    def getPlayerID(self):
        return self.player_id

    def movable(self, nextpos_x, nextpos_y):
        raise NotImplementedError


class Hira(Koma):
    def __init__(self, path, size, position, player_id, exist):
        super().__init__(path, size, position, player_id, exist)

    def movable(self, nextpos_x, nextpos_y):
        currentpos_x, currentpos_y = self.getPosition()
        if currentpos_y - nextpos_y == self.player_id and currentpos_x == nextpos_x:
            return True
        else:
            return False


class Syuninn(Koma):
    def __init__(self, path, size, position, player_id, exist):
        super().__init__(path, size, position, player_id, exist)

    def movable(self, nextpos_x, nextpos_y):
        currentpos_x, currentpos_y = self.getPosition()
        if currentpos_y - nextpos_y == self.player_id and abs(currentpos_x - nextpos_x) <= 1:
            return True
        elif currentpos_y - nextpos_y == - self.player_id and currentpos_x == nextpos_x:
            return True
        else:
            return False


class Kakaricho(Koma):
    def __init__(self, path, size, position, player_id, exist):
        super().__init__(path, size, position, player_id, exist)

    def movable(self, nextpos_x, nextpos_y):
        currentpos_x, currentpos_y = self.getPosition()
        if currentpos_y - nextpos_y == self.player_id and abs(currentpos_x - nextpos_x) == 1:
            return True
        elif currentpos_y - nextpos_y == self.player_id * 2 and currentpos_x == nextpos_x:
            return True
        elif currentpos_y - nextpos_y == - self.player_id and currentpos_x == nextpos_x:
            return True
        else:
            return False


class Kacho(Koma):
    def __init__(self, path, size, position, player_id, exist):
        super().__init__(path, size, position, player_id, exist)

    def movable(self, nextpos_x, nextpos_y):
        currentpos_x, currentpos_y = self.getPosition()
        if currentpos_y - nextpos_y == self.player_id and abs(currentpos_x - nextpos_x) <= 1:
            return True
        elif currentpos_y - nextpos_y == - self.player_id and abs(currentpos_x - nextpos_x) == 1:
            return True
        else:
            return False


class Bucho(Koma):
    def __init__(self, path, size, position, player_id, exist):
        super().__init__(path, size, position, player_id, exist)

    def movable(self, nextpos_x, nextpos_y):
        currentpos_x, currentpos_y = self.getPosition()
        if currentpos_y - nextpos_y == self.player_id and abs(currentpos_x - nextpos_x) <= 1:
            return True
        elif currentpos_y - nextpos_y == 0 and abs(currentpos_x - nextpos_x) == 1:
            return True
        elif currentpos_y - nextpos_y == - self.player_id and currentpos_x == nextpos_x:
            return True
        else:
            return False


class Shacho(Koma):
    def __init__(self, path, size, position, player_id, exist):
        super().__init__(path, size, position, player_id, exist)

    def movable(self, nextpos_x, nextpos_y):
        currentpos_x, currentpos_y = self.getPosition()
        if currentpos_y - nextpos_y == 0 and currentpos_x - nextpos_x == 0:
            return False
        if abs(currentpos_y - nextpos_y) <= 1 and abs(currentpos_x - nextpos_x) <= 1:
            return True
        else:
            return False


class Honnbucho(Koma):
    def __init__(self, path, size, position, player_id, exist):
        super().__init__(path, size, position, player_id, exist)

    def movable(self, nextpos_x, nextpos_y):
        currentpos_x, currentpos_y = self.getPosition()
        if abs(currentpos_x - nextpos_x) > 0 and abs(currentpos_x - nextpos_x) == abs(currentpos_y - nextpos_y):
            return True
        else:
            return False


class Yakuinn(Koma):
    def __init__(self, path, size, position, player_id, exist):
        super().__init__(path, size, position, player_id, exist)

    def movable(self, nextpos_x, nextpos_y):
        currentpos_x, currentpos_y = self.getPosition()
        if currentpos_y - nextpos_y == 0 and abs(currentpos_x - nextpos_x) > 0:
            return True
        elif currentpos_x - nextpos_x == 0 and abs(currentpos_y - nextpos_y) > 0:
            return True
        else:
            return False
