import math
import os
import random
import sys
import time
import pygame as pg

WIDTH = 800  # ゲームウィンドウの幅
HEIGHT = 600  # ゲームウィンドウの高さ
SP_COST = 1
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
        pg.K_i: (0, -5),
        pg.K_k: (0, +5),
        pg.K_j: (-5, 0),
        pg.K_l: (+5, 0),
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
        self.frozen = False  # 凍結状態を示すフラグ

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
        if self.frozen:
            screen.blit(self.img, self.rct)  # 凍結中はその場に留まる
            return  # 凍結中は操作を受け付けない

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
        self.frozen = False  # 凍結状態を示すフラグ

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
        if self.frozen:
            screen.blit(self.img, self.rct)  # 凍結中はその場に留まる
            return  # 凍結中は操作を受け付けない

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
    def __init__(self, color: tuple[int, int, int], rad: int, score_value=1):
        """
        引数に基づき爆弾円Surfaceを生成する
        引数1 color：爆弾円の色タプル
        引数2 rad：爆弾円の半径
        引数3 score_value：爆弾のスコア値
        """
        self.img = pg.Surface((2*rad, 2*rad))
        pg.draw.circle(self.img, color, (rad, rad), rad)
        self.img.set_colorkey((0, 0, 0))
        self.rct = self.img.get_rect()
        self.rct.center = (WIDTH/2,HEIGHT/2)
        # self.rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
        self.vx, self.vy = +5, +5
        self.score_value = score_value

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


class Goal:
    """
    ゴールを描画するクラス
    """
    def __init__(self, xy: tuple[int, int], width: int, height: int, color: tuple[int, int, int]):
        """
        引数:
        xy     : ゴールの左上座標 (x, y)
        width  : ゴールの幅
        height : ゴールの高さ
        color  : ゴールの色 (RGBタプル)
        """
        self.base_color = color  # 初期色
        self.color = color  # 現在の色
        self.base_height = height  # 初期幅
        self.width = width  
        self.height = height  # 現在の幅
        self.img = pg.Surface((self.width, self.height))
        self.img.fill(self.color)
        self.rct = self.img.get_rect()
        self.rct.topleft = xy
        self.timer = {"color": 0, "size": 0}  # スキルタイマーの管理

    def skill_effect(self, duration: int, color: tuple[int, int, int] = None, reduce_height: bool = False):
        """
        ゴールの色を変更し、必要に応じて幅を変更する。
        duration: 効果の継続時間
        color: 新しい色
        reduce_width: 幅を変更する場合はTrue
        """
        if color:
            self.timer["color"] = duration
            self.color = color
        if reduce_height:
            self.timer["size"] = duration
            # 中心座標を保持したまま高さを変更
            old_center = self.rct.center
            self.height = self.base_height // 2
            self.img = pg.Surface((self.width, self.height))  # 新しい高さのSurfaceを作成
            self.img.fill(self.color)
            self.rct = self.img.get_rect()  # 新しいRectを取得
            self.rct.center = old_center  # 中心を元の位置に戻す

    def update(self, screen: pg.Surface):
        """
        ゴールを画面に描画する
        タイマー更新
        screen : 画面Surface
        """
        for effect, time_left in self.timer.items():
            if time_left > 0:
                self.timer[effect] -= 1
                if self.timer[effect] == 0:  # 効果終了時に元の状態に戻す
                    if effect == "color":
                        self.color = self.base_color
                    elif effect == "size":
                        # 高さを元に戻し、中心座標を保持する
                        old_center = self.rct.center
                        self.height = self.base_height
                        self.img = pg.Surface((self.width, self.height))  # 元の高さのSurfaceを作成
                        self.img.fill(self.color)
                        self.rct = self.img.get_rect()  # 元のRectを取得
                        self.rct.center = old_center  # 中心を元の位置に戻す
        self.img = pg.Surface((self.width, self.height))
        self.img.fill(self.color)
        self.rct.height = self.height  # ゴール高さの更新
        screen.blit(self.img, self.rct)
        
class GoalState:
    """
    ゲーム全体の状態を管理するクラス
    """
    def __init__(self):
        self.scores = {"player1": 0, "player2": 0}  # プレイヤーごとのスコア
        self.cooldowns = {
            "color_p1": 0, "color_p2": 0,
            "size_p1": 0, "size_p2": 0,
        }  # 各プレイヤーのクールダウン
        self.skill_names = {  # スキル名を定義
            "color_p1": "ゴール無敵",
            "size_p1": "幅縮小",
            "color_p2": "ゴール変更",
            "size_p2": "幅縮小",
        }
    def update(self):
        for key in self.cooldowns:
            if self.cooldowns[key] > 0:
                self.cooldowns[key] -= 1

def check_coll(bomb: Bomb, bird: Bird) -> None:
    """
    爆弾とこうかとんの衝突処理を行う関数

    引数:
        bomb (Bomb): 衝突対象の爆弾オブジェクト
        bird (Bird): 衝突対象のこうかとんオブジェクト

    戻り値:
        None
    """
    hit_margin = 10
    if abs(bomb.rct.bottom - bird.rct.top) < hit_margin and bomb.vy > 0:
        bomb.vy *= -1
    elif abs(bomb.rct.top - bird.rct.bottom) < hit_margin and bomb.vy < 0:
        bomb.vy *= -1
    elif abs(bomb.rct.left -bird.rct.right) < hit_margin and bomb.vx < 0:
        bomb.vx *= -1
    elif abs(bomb.rct.right - bird.rct.left) < hit_margin and bomb.vx > 0:
        bomb.vx *= -1



def main():
    NUM_OF_BOMBS = 1
    pg.display.set_caption("たたかえ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))    
    bg_img = pg.image.load("fig/pg_bg.jpg")
    bird = Bird((WIDTH-100, HEIGHT/2))
    bird2 = Bird2((100, HEIGHT/2))
    bomb = Bomb((255, 0, 0), 10)
    bombs = [Bomb((255, 0, 0), 10) for _ in range(NUM_OF_BOMBS)]
    goal1 = Goal((WIDTH-10, HEIGHT/2-100), 10, 200, (0, 255, 0))  # ゴールを生成
    goal2 = Goal((0, HEIGHT/2-100), 10, 200, (0, 255, 0))  # ゴールを生成
    clock = pg.time.Clock()
    #score = Score()
    goal_state = GoalState()  # ゲーム状態の管理
    expls = []
    tmr = 0
    font = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 15)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
        screen.blit(bg_img, [0, 0])
        goal1.update(screen)
        goal2.update(screen) 
        
        # 爆弾とこうかとん1の衝突判定
        for bomb in bombs:
            if bird.rct.colliderect(bomb.rct):
                check_coll(bomb, bird)

        # 爆弾とこうかとん2の衝突判定
        for bomb in bombs:
            if bird2.rct.colliderect(bomb.rct):
                check_coll(bomb, bird2)
        key_lst = pg.key.get_pressed()
        # プレイヤー1のスキル（0: 色変更、9: 高さ縮小）
        if key_lst[pg.K_7] and goal_state.cooldowns["color_p1"] == 0:
            goal1.skill_effect(10 * 50, (255, 255, 0))
            goal_state.cooldowns["color_p1"] = 20 * 50
        if key_lst[pg.K_8] and goal_state.cooldowns["size_p1"] == 0:
            goal1.skill_effect(10 * 50, reduce_height=True)
            goal_state.cooldowns["size_p1"] = 15 * 50
        # プレイヤー2のスキル（1: 色変更、2: 高さ縮小）
        if key_lst[pg.K_1] and goal_state.cooldowns["color_p2"] == 0:
            goal2.skill_effect(10 * 50, (255, 255, 0))
            goal_state.cooldowns["color_p2"] = 20 * 50
        if key_lst[pg.K_2] and goal_state.cooldowns["size_p2"] == 0:
            goal2.skill_effect(10 * 50, reduce_height=True)
            goal_state.cooldowns["size_p2"] = 15 * 50
        # # スキル状態を描画
        # draw_skill_status(screen, goal_state, font)
        # ボールがゴールに到達した場合の処理
        if bomb.rct.colliderect(goal1.rct) and goal1.timer["color"] == 0:
            bombs.remove(bomb)
            if random.random() > 0.5:
                bombs.append(Bomb((255, 0, 0), 10,))
                goal_state.scores["player2"] += 2
                bomb.rct.center = (WIDTH / 2, HEIGHT / 2)  # ボールを中央に戻す
            else:
                bombs.append(Bomb((255, 215, 0), 10,))
                goal_state.scores["player2"] += 1
                bomb.rct.center = (WIDTH / 2, HEIGHT / 2)  # ボールを中央に戻す

            time.sleep(1)  # 一時停止（動作確認用）
        if bomb.rct.colliderect(goal2.rct) and goal2.timer["color"] == 0:
            bombs.remove(bomb)
            if random.random() > 0.5:
                bombs.append(Bomb((255, 0, 0), 10,))
                goal_state.scores["player1"] += 1
                bomb.rct.center = (WIDTH / 2, HEIGHT / 2)  # ボールを中央に戻す
            else:
                bombs.append(Bomb((255, 215, 0), 10,))
                goal_state.scores["player1"] += 2
                bomb.rct.center = (WIDTH / 2, HEIGHT / 2)  # ボールを中央に戻す
            time.sleep(1)  # 一時停止（動作確認用）
        


        bird.update(key_lst, screen)
        bird2.update(key_lst, screen)
        bombs = [bomb for bomb in bombs if bomb is not None]  # Noneでないもののリスト
        for bomb in bombs:
            bomb.update(screen)
        # スコアの表示更新
        font = pg.font.Font(None, 40)
        p1_score_text = font.render(f"P1 Score: {goal_state.scores['player1']}", True, (0, 0, 255))
        p2_score_text = font.render(f"P2 Score: {goal_state.scores['player2']}", True, (255, 0, 0))
        screen.blit(p1_score_text, (WIDTH - 200, HEIGHT - 50))
        screen.blit(p2_score_text, (10, HEIGHT - 50))
        #score.update(screen)
        expls = [expl for expl in expls if expl.life > 0]
        for expl in expls:
            expl.update(screen)
        # タイマーの更新
        goal_state.update()
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
