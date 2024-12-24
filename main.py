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
        self.fonto = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 30)
        self.color = color  
        self.rad = rad  
        self.img = pg.Surface((2*rad, 2*rad))
        pg.draw.circle(self.img, color, (rad, rad), rad)
        self.img.set_colorkey((0, 0, 0))
        self.rct = self.img.get_rect()
        self.rct.center = (WIDTH/2,HEIGHT/2)
        # self.rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
        self.vx, self.vy = +5, +5
        self.score_value = score_value

        # 爆弾大きさスキル
        self.count_large_1 = 0  # 1P 爆弾の大きさ変更スキル発動用 frameカウント
        self.count_large_2 = 0  # 2P 爆弾の大きさ変更スキル発動用 frameカウント
        self.large_frame = 400  # 発動に必要なframeカウント数 (爆弾の大きさ変更スキル用)

        if self.count_large_1 >= self.large_frame:  # 1P
            self.img_mozi_1 = self.fonto.render("9", 0, (255, 0, 0))
            self.rct_mozi_1 = self.img_mozi_1.get_rect()
            self.rct_mozi_1.center = (WIDTH-200, 100)
        else:
            self.img_mozi_1 = self.fonto.render("9", 0, (255, 0, 0))
            self.rct_mozi_1 = self.img_mozi_1.get_rect()
            self.rct_mozi_1.center = (WIDTH-200, 100)

        if self.count_large_2 >= self.large_frame:  # 2P
            self.img_mozi_2 = self.fonto.render("3", 0, (255, 0, 0))
            self.rct_mozi_2 = self.img_mozi_2.get_rect()
            self.rct_mozi_2.center = (200, 100)    
        else:
            self.img_mozi_2 = self.fonto.render("3", 0, (255, 0, 0))
            self.rct_mozi_2 = self.img_mozi_2.get_rect()
            self.rct_mozi_2.center = (200, 100)

    def resize(self, factor: float):
        """
        爆弾の大きさを変更する
        引数 factor: 爆弾の半径（変更後の）
        """
        self.rad = factor
        self.img = pg.Surface((2 * self.rad, 2 * self.rad))
        pg.draw.circle(self.img, self.color, (self.rad, self.rad), self.rad)
        self.img.set_colorkey((0, 0, 0))
        self.rct = self.img.get_rect(center=self.rct.center)

        # 大きさ変更後の爆弾 画面外との当たり判定
        if self.rct.left < 0:
            self.rct.left = 0
        if self.rct.right > WIDTH:
            self.rct.right = WIDTH
        if self.rct.top < 0:
            self.rct.top = 0
        if self.rct.bottom > HEIGHT:
            self.rct.bottom = HEIGHT

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

        # 爆弾大きさスキル
        if self.count_large_1 >= self.large_frame:  # 1P
            self.img_mozi_1 = self.fonto.render("9", 0, (255, 0, 0))
            screen.blit(self.img_mozi_1, self.rct_mozi_1)
        else:
            self.img_mozi_1 = self.fonto.render("9", 0, (0, 0, 0))
            screen.blit(self.img_mozi_1, self.rct_mozi_1)
        if self.count_large_2 >= self.large_frame:  # 2P
            self.img_mozi_2 = self.fonto.render("3", 0, (255, 0, 0))
            screen.blit(self.img_mozi_2, self.rct_mozi_2)
        else:
            self.img_mozi_2 = self.fonto.render("3", 0, (0, 0, 0))
            screen.blit(self.img_mozi_2, self.rct_mozi_2)


# class Score:
#     def __init__(self, position: tuple[int, int]):
#         self.fonto = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 30)
#         self.score = 0
#         self.position = position

#     def update(self, screen):
#         img = self.fonto.render(f"スコア：{self.score}", 0, (0, 0, 255))
#         rct = img.get_rect()
#         rct.center = self.position
#         screen.blit(img, rct)


# class SP:
#     """SPに関するクラス"""
#     def __init__(self, position: tuple[int, int]):
#         """
#         fontoで表示するためのフォントを設定
#         spはスキルポイント。初期値は0
#         positionはspの表示位置"""
#         # self.fonto = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 30)
#         self.sp = 5
#         # self.position = position

    # def update(self, screen):
    #     # img = self.fonto.render(f"SP：{self.sp}", 0, (0, 255, 0))
    #     # rct = img.get_rect()
    #     # rct.center = self.position
    #     # screen.blit(img, rct)


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
        self.time = 60
        self.img = self.fonto.render(f"制限時間：{self.time}", 0, (255, 0, 0))
        self.rct = self.img.get_rect()
        self.rct.center = (100, 50)

    def update(self, screen):
        self.img = self.fonto.render(f"制限時間：{self.time}", 0, (0, 0, 255))
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
#スキル状態の表示は推奨機ではスペックが足りない可能性
# def draw_skill_status(screen, goal_state: GoalState, font):
#     """
#     スキルの状態を描画する
#     screen: 描画する画面Surface
#     goal_state: GoalStateオブジェクト
#     font: フォントオブジェクト
#     """
#     # プレイヤー1のスキル表示位置
#     p1_base_x, p1_base_y = WIDTH - 300, 100
#     # プレイヤー2のスキル表示位置
#     p2_base_x, p2_base_y = 10, 100
#     for player, (base_x, base_y, suffix) in zip(["player1", "player2"], [(p1_base_x, p1_base_y, "p1"), (p2_base_x, p2_base_y, "p2")]):
#         for skill in ["color", "size"]:
#             key = f"{skill}_{suffix}"  # スキルキー（例: color_p1, size_p2）
#             skill_name = goal_state.skill_names[key]
#             cooldown = goal_state.cooldowns[key]
#             # 状態テキストの生成
#             if cooldown == 0:
#                 status_text = f"{skill_name}: スキル使用可能"
#                 color = (0, 255, 0)  # 使用可能の色: 緑
#             else:
#                 status_text = f"{skill_name}: クールダウン中()"  #{cooldown // 50:.1f}s)"
#                 color = (255, 0, 0)  # クールダウン中の色: 赤
#             # 描画
#             font = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 15)
#             skill_text = font.render(status_text, True, color)
#             screen.blit(skill_text, (base_x, base_y))
#             base_y += 30  # 次のスキル用に行を下げる

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


class Freeze:
    """停止スキルに関するクラス"""
    def __init__(self, duration: int):
        """
        durationは凍結の持続時間を指定する
        timerは停止時間のカウント。初期値は0
        """
        self.duration = duration
        self.timer = 0

    def update(self):
        """
        timerの数字を1づつ減らしていく
        """
        if self.timer > 0:
            self.timer -= 1

    def activate(self):
        """
        停止状態を開始する
        """
        self.timer = self.duration

    def is_active(self):
        """
        停止状態かのチェック
        """
        return self.timer > 0


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
        self.num = 501 #フェイク爆弾を出すか出さないかを判断する数
        self.img1 = self.fonto.render(f"4", 0, (255, 0, 0)) #文字列Surface
        self.rct1 = self.img1.get_rect()
        self.rct1.center = (250, 100)
        self.img2 = self.fonto.render(f"4", 0, (0, 0, 0))
        self.rct2 = self.img2.get_rect()
        self.rct2.center = (250, 100)
        # self.ix, self.iy = 300, 100

    def update(self, screen: pg.Surface):
        """
        フェイク爆弾1を発動できるか出来ないかの判定を行い表示する
        引数 screen：画面Surface
        """
        if self.num >= 500 :
            self.img1 = self.fonto.render(f"4", 0, (255, 0, 0))
            screen.blit(self.img1, self.rct1)
        else:
            self.img2 = self.fonto.render(f"4", 0, (0, 0, 0))
            screen.blit(self.img2, self.rct2)


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
        self.num = 501 #フェイク爆弾を出すか出さないかを判断する数
        self.img1 = self.fonto.render(f"0", 0, (255, 0, 0)) #文字列Surface
        self.rct1 = self.img1.get_rect()
        self.rct1.center = (WIDTH-150, 100)
        self.img2 = self.fonto.render(f"0", 0, (0, 0, 0))
        self.rct2 = self.img2.get_rect()
        self.rct2.center = (WIDTH-150, 100)
        self.ix, self.iy = 650, 80

    def update(self, screen: pg.Surface):
        """
        フェイク爆弾2を発動できるか出来ないかの判定を行い表示する
        引数 screen：画面Surface
        """
        if self.num >= 500 :
            self.img1 = self.fonto.render(f"0", 0, (255, 0, 0))
            screen.blit(self.img1, self.rct1)
        else:
            self.img2 = self.fonto.render(f"0", 0, (0, 0, 0))
            screen.blit(self.img2, self.rct2)


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
    fake1 = None
    fake2 = None
    next1 = Next1() ##
    next2 = Next2() ##
    #score = Score()
    goal_state = GoalState()  # ゲーム状態の管理
    expls = []
    limit = Limit()
    freeze_bird = Freeze(120)  # 5秒間凍結
    freeze_bird2 = Freeze(120)  # 5秒間凍結
    tmr = 0
    # # フォント設定（日本語対応フォントを指定）
    # font_path = "C:/Windows/Fonts/msgothic.ttc"  # 日本語対応フォント
    # font = pg.font.Font(font_path, 30)  # フォントサイズ30
    font = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 15)

    right_sp = 1
    left_sp = 1

    # ゴールの設定
    # left_goal = pg.Rect(0, (HEIGHT - GOAL_HEIGHT) // 2, GOAL_WIDTH, GOAL_HEIGHT)
    # right_goal = pg.Rect(WIDTH - GOAL_WIDTH, (HEIGHT - GOAL_HEIGHT) // 2, GOAL_WIDTH, GOAL_HEIGHT)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pg.KEYDOWN and event.key == pg.K_9 and bomb.count_large_1 >= bomb.large_frame:  # 1P キー（9）を押したときに
                # 2つのモード
                # bomb.resize(bomb.rad * 2)  # 倍率の場合（押すたびに変化）
                bomb.resize(50)  # 固定の大きさの場合
                bomb.count_large_1 = 0
            if event.type == pg.KEYDOWN and event.key == pg.K_3 and bomb.count_large_2 >= bomb.large_frame:  # 2P キー（3）を押したときに
                # 2つのモード
                # bomb.resize(bomb.rad * 2)  # 倍率の場合（押すたびに変化）
                bomb.resize(50)  # 固定の大きさの場合
                bomb.count_large_2 = 0
            
            if event.type == pg.KEYDOWN and event.key == pg.K_4 and next1.num >= 500: ##bを押すとfakeボール1が出る
                fake1 = Fake1((255, 0, 0), 10) ##
                next1.num = 0 ##
            
            if event.type == pg.KEYDOWN and event.key == pg.K_0 and next2.num >= 500: ##bを押すとfakeボール2が出る
                fake2 = Fake2((255, 0, 0), 10) ##
                next2.num = 0 ##

        if bomb.count_large_1 == 200:  # 4秒(200frame)でボールが元に戻る
            bomb.resize(10)
        if bomb.count_large_2 == 200:  # 4秒(200frame)でボールが元に戻る
            bomb.resize(10)

        screen.blit(bg_img, [0, 0])
        goal1.update(screen)
        goal2.update(screen) 
        #ゴール実装初期
        # # ゴールに到達したか判定
        # if bomb.rct.colliderect(goal.rct):
        #     score.score += 1  # 1点アップ
        #     bomb.rct.center = (WIDTH/2,HEIGHT/2)  # 爆弾を中心位置に再配置
        #     # fonto = pg.font.Font(None, 80)
        #     # txt = fonto.render("ゴール達成！", True, (0, 255, 0))
        #     # screen.blit(txt, [WIDTH//2-150, HEIGHT//2])
        #     # pg.display.update()
        #     time.sleep(2)
        #     # return
        # if bomb.rct.colliderect(goal2.rct):
        #     score.score += 1  # 1点アップ
        #     bomb.rct.center = (WIDTH/2,HEIGHT/2)  # 爆弾を中心位置に再配置
        #     # fonto = pg.font.Font(None, 80)
        #     # txt = fonto.render("ゴール達成！", True, (0, 255, 0))
        #     # screen.blit(txt, [WIDTH//2-150, HEIGHT//2])
        #     # pg.display.update()
        #     time.sleep(2)
        #     # return
        if limit.time == 0:
            fonto = pg.font.Font(None, 80)
            txt = fonto.render("end", True, (255, 0, 0))
            screen.blit(txt, [WIDTH//2-80, HEIGHT//2])
            pg.display.update()
            time.sleep(1)
            return
        
        # 爆弾とこうかとん1の衝突判定
        for bomb in bombs:
            if bird.rct.colliderect(bomb.rct):
                check_coll(bomb, bird)

        # 爆弾とこうかとん2の衝突判定
        for bomb in bombs:
            if bird2.rct.colliderect(bomb.rct):
                check_coll(bomb, bird2)
        key_lst = pg.key.get_pressed()
        # プレイヤー1のスキル（7: 色変更、8: 高さ縮小）
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

        fonto = pg.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 30) #フォント

        if goal_state.cooldowns["color_p2"] == 0:
            img1 = fonto.render(f"1", 0, (255, 0, 0)) #文字列Surface
            rct1 = img1.get_rect()
            rct1.center = (100, 100)
            screen.blit(img1, rct1)
        else:
            img1 = fonto.render(f"1", 0, (0, 0, 0)) #文字列Surface
            rct1 = img1.get_rect()
            rct1.center = (100, 100)
            screen.blit(img1, rct1)
        if goal_state.cooldowns["color_p1"] == 0:
            img1 = fonto.render(f"7", 0, (255, 0, 0)) #文字列Surface
            rct1 = img1.get_rect()
            rct1.center = (WIDTH-300, 100)
            screen.blit(img1, rct1)
        else:
            img1 = fonto.render(f"7", 0, (0, 0, 0)) #文字列Surface
            rct1 = img1.get_rect()
            rct1.center = (WIDTH-300, 100)
            screen.blit(img1, rct1)

        if goal_state.cooldowns["size_p2"] == 0:
            img2 = fonto.render(f"2", 0, (255, 0, 0)) #文字列Surface
            rct2 = img2.get_rect()
            rct2.center = (150, 100)
            screen.blit(img2, rct2)
        else:
            img2 = fonto.render(f"2", 0, (0, 0, 0)) #文字列Surface
            rct2 = img2.get_rect()
            rct2.center = (150, 100)
            screen.blit(img2, rct2)
        if goal_state.cooldowns["size_p1"] == 0:
            img2 = fonto.render(f"8", 0, (255, 0, 0)) #文字列Surface
            rct2 = img2.get_rect()
            rct2.center = (WIDTH-250, 100)
            screen.blit(img2, rct2)
        else:
            img2 = fonto.render(f"8", 0, (0, 0, 0)) #文字列Surface
            rct2 = img2.get_rect()
            rct2.center = (WIDTH-250, 100)
            screen.blit(img2, rct2)

        # # スキル状態を描画
        # draw_skill_status(screen, goal_state, font)
        # ボールがゴールに到達した場合の処理
        if bomb.rct.colliderect(goal1.rct) and goal1.timer["color"] == 0:
            goal_state.scores["player1"] += 1
            bomb.rct.center = (WIDTH / 2, HEIGHT / 2)  # ボールを中央に戻す
            time.sleep(1)  # 一時停止（動作確認用）
        if bomb.rct.colliderect(goal2.rct) and goal2.timer["color"] == 0:
            goal_state.scores["player2"] += 1
            bomb.rct.center = (WIDTH / 2, HEIGHT / 2)  # ボールを中央に戻す
            time.sleep(1)  # 一時停止（動作確認用）
        if key_lst[pg.K_LSHIFT] and left_sp >= SP_COST:
            freeze_bird.activate()
            left_sp -= SP_COST #コストを消費
        if key_lst[pg.K_RSHIFT] and right_sp >= SP_COST:
            freeze_bird2.activate()
            right_sp -= SP_COST#コストを消費

        freeze_bird.update()
        freeze_bird2.update()


        if left_sp >= SP_COST:
            img3 = fonto.render(f"LSHIFT", 0, (255, 0, 0)) #文字列Surface
            rct3 = img3.get_rect()
            rct3.center = (350, 100)
            screen.blit(img3, rct3)
        else:
            img3 = fonto.render(f"LSHIFT", 0, (0, 0, 0)) #文字列Surface
            rct3 = img3.get_rect()
            rct3.center = (350, 100)
            screen.blit(img3, rct3)
        if right_sp >= SP_COST:
            img3 = fonto.render(f"RSHIFT", 0, (255, 0, 0)) #文字列Surface
            rct3 = img3.get_rect()
            rct3.center = (WIDTH-50, 100)
            screen.blit(img3, rct3)
        else:
            img3 = fonto.render(f"RSHIFT", 0, (0, 0, 0)) #文字列Surface
            rct3 = img3.get_rect()
            rct3.center = (WIDTH-50, 100)
            screen.blit(img3, rct3)

        bird.frozen = freeze_bird.is_active()
        bird2.frozen = freeze_bird2.is_active()

        bird.update(key_lst, screen)
        bird2.update(key_lst, screen)
        bombs = [bomb for bomb in bombs if bomb is not None]  # Noneでないもののリスト
        for bomb in bombs:
            bomb.update(screen)
        # スコアの表示更新
        font = pg.font.Font(None, 40)
        p1_score_text = font.render(f"P1 Score: {goal_state.scores['player2']}", True, (0, 0, 255))
        p2_score_text = font.render(f"P2 Score: {goal_state.scores['player1']}", True, (255, 0, 0))
        screen.blit(p1_score_text, (WIDTH - 200, HEIGHT - 50))
        screen.blit(p2_score_text, (10, HEIGHT - 50))
        #score.update(screen)
        expls = [expl for expl in expls if expl.life > 0]
        for expl in expls:
            expl.update(screen)
        # タイマーの更新
        goal_state.update()
        if (tmr != 0) and (tmr % 50 == 0):
            limit.time -= 1
        # if (tmr != 0) and (tmr % 150 == 0):  # 3秒ごとにSPを増やす
        #     sp_left.sp += 1
        #     sp_right.sp += 1
        limit.update(screen)

        if fake1 is not None: ##
            if next1.num == 500: #fakeボール1がでて200フレームたったらfakeボール1が消える
                next1.num = 0 ##
                fake1 = None #fake1をNoneに戻す

            if fake1 is not None: ##
                fake1.update(screen) ##
        
        if fake2 is not None: ##
            if next2.num == 500: #fakeボール2がでて200フレームたったらfakeボールが消える
                next2.num = 0 ##
                fake2 = None #fake2をNoneに戻す

            if fake2 is not None: ##
                fake2.update(screen) ##

        next1.update(screen) ##
        next2.update(screen) ##
        pg.display.update()
        tmr += 1
        bomb.count_large_1 += 1  # 1P frameカウント_爆弾大きさスキル用
        bomb.count_large_2 += 1  # 2P frameカウント_爆弾大きさスキル用
        next1.num += 1 ##
        next2.num += 1 ##
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
