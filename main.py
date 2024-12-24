import math
import os
import random
import sys
import time
import pygame as pg


WIDTH = 800  # ゲームウィンドウの幅
HEIGHT = 600  # ゲームウィンドウの高さ
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    """
    オブジェクトが画面内or画面外を判定し，真理値タプルを返す関数
    引数：こうかとんや爆弾，ビームなどのRect
    戻り値：横方向，縦方向のはみ出し判定結果（画面内：True／画面外：False）
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate


class Bird:
    """
    ゲームキャラクター（こうかとん）に関するクラス
    """
    delta = {  # 押下キーと移動量の辞書
        pg.K_UP: (0, -5),
        pg.K_DOWN: (0, +5),
        pg.K_LEFT: (-5, 0),
        pg.K_RIGHT: (+5, 0),
    }
    img0 = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    img = pg.transform.flip(img0, True, False)  # デフォルトのこうかとん（右向き）
    imgs = {  # 0度から反時計回りに定義
        (+5, 0): img,  # 右
        (+5, -5): pg.transform.rotozoom(img, 45, 0.9),  # 右上
        (0, -5): pg.transform.rotozoom(img, 90, 0.9),  # 上
        (-5, -5): pg.transform.rotozoom(img0, -45, 0.9),  # 左上
        (-5, 0): img0,  # 左
        (-5, +5): pg.transform.rotozoom(img0, 45, 0.9),  # 左下
        (0, +5): pg.transform.rotozoom(img, -90, 0.9),  # 下
        (+5, +5): pg.transform.rotozoom(img, -45, 0.9),  # 右下
    }

    def __init__(self, xy: tuple[int, int]):
        """
        こうかとん画像Surfaceを生成する
        引数 xy：こうかとん画像の初期位置座標タプル
        """
        self.img = __class__.imgs[(-5, 0)]
        self.rct: pg.Rect = self.img.get_rect()
        self.rct.center = xy
        self.dire = (+5, 0)

    def change_img(self, num: int, screen: pg.Surface):
        """
        こうかとん画像を切り替え，画面に転送する
        引数1 num：こうかとん画像ファイル名の番号
        引数2 screen：画面Surface
        """
        self.img = pg.transform.rotozoom(pg.image.load(f"fig/{num}.png"), 0, 0.9)
        screen.blit(self.img, self.rct)

    def update(self, key_lst: list[bool], screen: pg.Surface):
        """
        押下キーに応じてこうかとんを移動させる
        引数1 key_lst：押下キーの真理値リスト
        引数2 screen：画面Surface
        """
        sum_mv = [0, 0]
        for k, mv in __class__.delta.items():
            if key_lst[k]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        self.rct.move_ip(sum_mv)
        if check_bound(self.rct) != (True, True):
            self.rct.move_ip(-sum_mv[0], -sum_mv[1])
        if not (sum_mv[0] == 0 and sum_mv[1] == 0):
            self.img = __class__.imgs[tuple(sum_mv)]
        screen.blit(self.img, self.rct)
        if sum_mv != [0, 0]:
            self.dire = (sum_mv[0], sum_mv[1])

class Bird2:
    """
    ゲームキャラクター（こうかとん）に関するクラス
    """
    delta = {  # 押下キーと移動量の辞書
        pg.K_w: (0, -5),
        pg.K_s: (0, +5),
        pg.K_a: (-5, 0),
        pg.K_d: (+5, 0),
    }
    img0 = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    img = pg.transform.flip(img0, True, False)  # デフォルトのこうかとん（右向き）
    imgs = {  # 0度から反時計回りに定義
        (+5, 0): img,  # 右
        (+5, -5): pg.transform.rotozoom(img, 45, 0.9),  # 右上
        (0, -5): pg.transform.rotozoom(img, 90, 0.9),  # 上
        (-5, -5): pg.transform.rotozoom(img0, -45, 0.9),  # 左上
        (-5, 0): img0,  # 左
        (-5, +5): pg.transform.rotozoom(img0, 45, 0.9),  # 左下
        (0, +5): pg.transform.rotozoom(img, -90, 0.9),  # 下
        (+5, +5): pg.transform.rotozoom(img, -45, 0.9),  # 右下
    }

    def __init__(self, xy: tuple[int, int]):
        """
        こうかとん画像Surfaceを生成する
        引数 xy：こうかとん画像の初期位置座標タプル
        """
        self.img = __class__.imgs[(+5, 0)]
        self.rct: pg.Rect = self.img.get_rect()
        self.rct.center = xy
        self.dire = (+5, 0)

    def change_img(self, num: int, screen: pg.Surface):
        """
        こうかとん画像を切り替え，画面に転送する
        引数1 num：こうかとん画像ファイル名の番号
        引数2 screen：画面Surface
        """
        self.img = pg.transform.rotozoom(pg.image.load(f"fig/{num}.png"), 0, 0.9)
        screen.blit(self.img, self.rct)

    def update(self, key_lst: list[bool], screen: pg.Surface):
        """
        押下キーに応じてこうかとんを移動させる
        引数1 key_lst：押下キーの真理値リスト
        引数2 screen：画面Surface
        """
        sum_mv = [0, 0]
        for k, mv in __class__.delta.items():
            if key_lst[k]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        self.rct.move_ip(sum_mv)
        if check_bound(self.rct) != (True, True):
            self.rct.move_ip(-sum_mv[0], -sum_mv[1])
        if not (sum_mv[0] == 0 and sum_mv[1] == 0):
            self.img = __class__.imgs[tuple(sum_mv)]
        screen.blit(self.img, self.rct)
        if sum_mv != [0, 0]:
            self.dire = (sum_mv[0], sum_mv[1])   


class Bomb:
    """
    爆弾に関するクラス
    """
    def __init__(self, color: tuple[int, int, int], rad: int):
        """
        引数に基づき爆弾円Surfaceを生成する
        引数1 color：爆弾円の色タプル
        引数2 rad：爆弾円の半径
        """
        self.img = pg.Surface((2*rad, 2*rad))
        pg.draw.circle(self.img, color, (rad, rad), rad)
        self.img.set_colorkey((0, 0, 0))
        self.rct = self.img.get_rect()
        self.rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
        self.vx, self.vy = +5, +5

    def update(self, screen: pg.Surface):
        """
        爆弾を速度ベクトルself.vx, self.vyに基づき移動させる
        引数 screen：画面Surface
        """
        yoko, tate = check_bound(self.rct)
        if not yoko:
            self.vx *= -1
        if not tate:
            self.vy *= -1
        self.rct.move_ip(self.vx, self.vy)
        screen.blit(self.img, self.rct)


class Score:
    def __init__(self):
        self.fonto = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 30)
        self.score = 0
        self.img = self.fonto.render(f"スコア：{self.score}", 0, (0, 0, 255))
        self.rct = self.img.get_rect()
        self.rct.center = (100, HEIGHT-50)

    def update(self, screen):
        self.img = self.fonto.render(f"スコア：{self.score}", 0, (0, 0, 255))
        screen.blit(self.img, self.rct)


class Explosion:
    def __init__(self, bomb: Bomb):
        self.img1 = pg.image.load(f"fig/explosion.gif")
        self.img2 = pg.transform.flip(self.img1, True, True)
        self.imgs = [self.img1, self.img2]
        self.rct = self.img1.get_rect()
        self.rct.center = bomb.rct.center
        self.life = 50

    def update(self, screen):
        self.life -= 1
        if self.life > 0:
            ind = (self.life // 10) % 2
            screen.blit(self.imgs[ind], self.rct)


class Limit:
    def __init__(self):
        self.fonto = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 30)
        self.time = 1000
        self.img = self.fonto.render(f"制限時間：{self.time}", 0, (255, 0, 0))
        self.rct = self.img.get_rect()
        self.rct.center = (100, 50)

    def update(self, screen):
        self.img = self.fonto.render(f"制限時間：{self.time}", 0, (0, 0, 255))
        screen.blit(self.img, self.rct)


class Fake1: ##
    """
    フェイク爆弾1に関するクラス
    """
    def __init__(self, color: tuple[int, int, int], rad: int):
        """
        引数に基づき爆弾円Surfaceを生成する
        引数1 color：爆弾円の色タプル
        引数2 rad：爆弾円の半径
        """
        self.img = pg.Surface((2*rad, 2*rad))
        pg.draw.circle(self.img, color, (rad, rad), rad)
        self.img.set_colorkey((0, 0, 0))
        self.rct = self.img.get_rect()
        self.rct.center = random.randint(20, WIDTH-20), random.randint(20, HEIGHT-20)
        self.vx, self.vy = +5, +5

    def update(self, screen: pg.Surface):
        """
        爆弾を速度ベクトルself.vx, self.vyに基づき移動させる
        引数 screen：画面Surface
        """
        yoko, tate = check_bound(self.rct)
        if not yoko:
            self.vx *= -1
        if not tate:
            self.vy *= -1
        self.rct.move_ip(self.vx, self.vy)
        screen.blit(self.img, self.rct)


class Fake2: ##
    """
    フェイク爆弾2に関するクラス
    """
    def __init__(self, color: tuple[int, int, int], rad: int):
        """
        引数に基づき爆弾円Surfaceを生成する
        引数1 color：爆弾円の色タプル
        引数2 rad：爆弾円の半径
        """
        self.img = pg.Surface((2*rad, 2*rad))
        pg.draw.circle(self.img, color, (rad, rad), rad)
        self.img.set_colorkey((0, 0, 0))
        self.rct = self.img.get_rect()
        self.rct.center = random.randint(20, WIDTH-20), random.randint(20, HEIGHT-20)
        self.vx, self.vy = +5, +5

    def update(self, screen: pg.Surface):
        """
        爆弾を速度ベクトルself.vx, self.vyに基づき移動させる
        引数 screen：画面Surface
        """
        yoko, tate = check_bound(self.rct)
        if not yoko:
            self.vx *= -1
        if not tate:
            self.vy *= -1
        self.rct.move_ip(self.vx, self.vy)
        screen.blit(self.img, self.rct)


class Next1: ##
    """
    フェイク爆弾1の技を発動できるか出来ないかを判定する
    """
    def __init__(self):
        """
        丸かバツを表示するクラス
        """
        self.fonto = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 30) #フォント
        self.color = (0, 0, 255) #文字色の設定
        self.num = 301 #フェイク爆弾を出すか出さないかを判断する数
        self.img1 = self.fonto.render(f"〇", 0, self.color) #文字列Surface
        self.img2 = self.fonto.render(f"✕", 0, self.color)
        self.ix, self.iy = 50, HEIGHT-100

    def update(self, screen: pg.Surface):
        """
        フェイク爆弾1を発動できるか出来ないかの判定を行い表示する
        引数 screen：画面Surface
        """
        if self.num >= 300 :
            self.img1 = self.fonto.render(f"〇", 0, self.color)
            screen.blit(self.img1, (self.ix, self.iy))
        else:
            self.img2 = self.fonto.render(f"バツ", 0, self.color)
            screen.blit(self.img2, (self.ix, self.iy))


class Next2: ##
    """
    フェイク爆弾2の技を発動できるか出来ないかを判定する
    """
    def __init__(self):
        """
        丸かバツを表示するクラス
        """
        self.fonto = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 30) #フォント
        self.color = (0, 0, 255) #文字色の設定
        self.num = 301 #フェイク爆弾を出すか出さないかを判断する数
        self.img1 = self.fonto.render(f"〇", 0, self.color) #文字列Surface
        self.img2 = self.fonto.render(f"✕", 0, self.color)
        self.ix, self.iy = 650, HEIGHT-100

    def update(self, screen: pg.Surface):
        """
        フェイク爆弾2を発動できるか出来ないかの判定を行い表示する
        引数 screen：画面Surface
        """
        if self.num >= 300 :
            self.img1 = self.fonto.render(f"〇", 0, self.color)
            screen.blit(self.img1, (self.ix, self.iy))
        else:
            self.img2 = self.fonto.render(f"バツ", 0, self.color)
            screen.blit(self.img2, (self.ix, self.iy))


def main():
    NUM_OF_BOMBS = 1
    pg.display.set_caption("たたかえ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))    
    bg_img = pg.image.load("fig/pg_bg.jpg")
    bird = Bird((WIDTH-100, HEIGHT-(HEIGHT/2)))
    bird2 = Bird2((100, HEIGHT/2))
    bomb = Bomb((255, 0, 0), 10)
    bombs = [Bomb((255, 0, 0), 10) for _ in range(NUM_OF_BOMBS)]
    clock = pg.time.Clock()
    fake1 = None
    fake2 = None
    next1 = Next1() ##
    next2 = Next2() ##
    score = Score()
    expls = []
    limit = Limit()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            
            if event.type == pg.KEYDOWN and event.key == pg.K_4 and next1.num >= 300: ##bを押すとfakeボール1が出る
                fake1 = Fake1((255, 255, 0), 20) ##
                next1.num = 0 ##
            
            if event.type == pg.KEYDOWN and event.key == pg.K_0 and next2.num >= 300: ##bを押すとfakeボール2が出る
                fake2 = Fake2((255, 255, 255), 20) ##
                next2.num = 0 ##

        screen.blit(bg_img, [0, 0])
        
        if limit.time == 0:
            fonto = pg.font.Font(None, 80)
            txt = fonto.render("end", True, (255, 0, 0))
            screen.blit(txt, [WIDTH//2-80, HEIGHT//2])
            pg.display.update()
            time.sleep(1)
            return
        

        key_lst = pg.key.get_pressed()
        bird.update(key_lst, screen)
        bird2.update(key_lst, screen)
        bombs = [bomb for bomb in bombs if bomb is not None]  # Noneでないもののリスト
        for bomb in bombs:
            bomb.update(screen)
        score.update(screen)
        expls = [expl for expl in expls if expl.life > 0]
        for expl in expls:
            expl.update(screen)
        if (tmr != 0) and (tmr % 50 == 0):
            limit.time -= 1
        limit.update(screen)

        if fake1 is not None: ##
            if next1.num == 200: #fakeボール1がでて200フレームたったらfakeボール1が消える
                next1.num = 0 ##
                fake1 = None #fake1をNoneに戻す

            if fake1 is not None: ##
                fake1.update(screen) ##
        
        if fake2 is not None: ##
            if next2.num == 200: #fakeボール2がでて200フレームたったらfakeボールが消える
                next2.num = 0 ##
                fake2 = None #fake2をNoneに戻す

            if fake2 is not None: ##
                fake2.update(screen) ##

        next1.update(screen) ##
        next2.update(screen) ##
        pg.display.update()
        tmr += 1
        next1.num += 1 ##
        next2.num += 1 ##
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()