import argparse
import os

import imageio
from PIL import Image, ImageDraw, ImageFont

from .config import colors, minos

output_dir = 'img/output'
NEXT_MINO_COLUMN = 4

# Tetrisのゲーム盤を生成する関数
def generate_tetris_board(board, next_minos, hold_minos):
    # 1マスのサイズ
    cell_size = 30

    # フォントの設定
    font_size = cell_size
    font = ImageFont.truetype("font/ARIAL.TTF", font_size)

    # ボードのサイズ
    turns = len(board)
    board_width = len(board[0][0])
    board_height = len(board[0])
    img_width = (board_width + 2 + NEXT_MINO_COLUMN) * cell_size  # 左右に1ブロック広げる
    img_height = (board_height + 1) * cell_size  # 下に1ブロック広げる

    # ゲーム盤の画像を生成
    board_img = Image.new('RGB', (img_width, img_height), color='white')
    draw = ImageDraw.Draw(board_img)

    # 盤面を描画
    for turn in range(turns):
        # 一度全ブロックを 0 と仮定して塗る
        for y in range(board_height + 1):
            for x in range(board_width + 2 + NEXT_MINO_COLUMN):
                draw.rectangle([x * cell_size, y * cell_size, (x + 1) * cell_size, (y + 1) * cell_size], fill=colors[0], outline='black')

        # 左右のブロックを黒で塗る
        for y in range(board_height + 1):
            image = Image.open(f'img/mino_8.png')
            resized_image = image.resize((cell_size, cell_size))
            board_img.paste(resized_image, (0, y * cell_size)) # 左側
            board_img.paste(resized_image, ((board_width + 1) * cell_size, y * cell_size)) # 右側
        # 下のブロックを黒で塗る
        for x in range(board_width + 2):
            image = Image.open(f'img/mino_8.png')
            resized_image = image.resize((cell_size, cell_size))
            board_img.paste(resized_image, (x * cell_size, img_height - cell_size))

        for x in range(board_width):
            for y in range(board_height):
                # ターンごとの座標を計算
                pos_x = (x + 1) * cell_size  # 左端から1つ分ずらす
                pos_y = y * cell_size  # 上端から1つ分ずらす
                # ターンごとの色を取得
                board_index = board[turn][y][x]
                color = colors[board_index]

                # 長方形を描画
                if board_index != 0:
                    image = Image.open(f'img/mino_{board_index}.png')
                    resized_image = image.resize((cell_size, cell_size))
                    board_img.paste(resized_image, (pos_x, pos_y))
                else:
                    draw.rectangle([pos_x, pos_y, pos_x + cell_size, pos_y + cell_size], fill=color, outline='black')

        # ネクストミノを描画
        next_mino_height = 1
        for mino_index in next_minos[turn]:
            mino = minos[mino_index]
            for y in range(len(mino)):
                for x in range(len(mino[0])):
                    cell = mino[y][x]
                    if cell == 0: # 黒で描画
                        color_index = 0
                    else: # ミノの色を取得
                        color_index = mino_index

                    # ミノを描画
                    color = colors[color_index]
                    pos_x = (x + board_width + 2) * cell_size # 盤面の右隣に配置
                    pos_y = (y + next_mino_height) * cell_size # 上端から1つ分ずらす

                    # O ミノだけ例外で右に 1 マスずらす
                    if mino_index == 4:
                        pos_x += cell_size
                    
                    if color_index != 0:
                        image = Image.open(f'img/mino_{color_index}.png')
                        resized_image = image.resize((cell_size, cell_size))
                        board_img.paste(resized_image, (pos_x, pos_y))
                    else:
                        draw.rectangle([pos_x, pos_y, pos_x + cell_size, pos_y + cell_size], fill=color, outline='black')

            next_mino_height += len(mino[0]) + 1

        # ホールドミノを描画
        hold_mino_index = hold_minos[turn]
        hold_mino = minos[hold_mino_index]
        for y in range(len(hold_mino)):
            for x in range(len(hold_mino[0])):
                cell = hold_mino[y][x]
                if cell == 0:
                    color_index = 0
                else:
                    color_index = hold_mino_index
                color = colors[color_index]
                pos_x = (board_width + 2 + x) * cell_size
                pos_y = (board_height - 4 + y) * cell_size

                if hold_mino_index == 4:
                    pos_x += cell_size

                if color_index != 0:
                    image = Image.open(f'img/mino_{color_index}.png')
                    resized_image = image.resize((cell_size, cell_size))
                    board_img.paste(resized_image, (pos_x, pos_y))
                else:
                    draw.rectangle([pos_x, pos_y, pos_x + cell_size, pos_y + cell_size], fill=color, outline='black')

        # 画像を保存
        filename = os.path.join(output_dir, f'turn{turn}.png')
        board_img.save(filename)

    return
          
# 生成した画像からGIFを作成する関数
def create_gif(output_dir, turns, filename, duration=0.5):
    # ターンごとの画像ファイルをリストに追加
    images = []
    for turn in range(turns):
        image_path = os.path.join(output_dir, f"turn{turn}.png")
        images.append(imageio.imread(image_path))
    
    # GIF を生成
    with imageio.get_writer(filename, mode='I', duration=duration, loop=0) as writer:
        for image in images:
            writer.append_data(image)

def main(duration=0.5, loop=0, delay_last_frame=2):
    with open('in.txt', 'r') as file:
        # ターン数、高さ、幅を読み込む
        turns, height, width = map(int, file.readline().split())

        # 盤面情報を3次元配列として読み込む
        board = []
        next_minos = []
        hold_minos = []
        for _ in range(turns):
            turn_data = []
            for _ in range(height):
                row = list(map(int, file.readline().split()))
                turn_data.append(row)
            board.append(turn_data)

            # ネクストミノの番号を読み込んで2次元配列に追加する
            next_mino_turn = list(map(int, file.readline().split()))
            next_minos.append(next_mino_turn)

            # ホールドミノの番号を読み込んで1次元配列に追加する
            hold_minos.append(int(file.readline()))

    # Tetrisのゲーム盤画像を生成
    generate_tetris_board(board, next_minos, hold_minos)

    # GIFを作成する
    parser = argparse.ArgumentParser(description="Generate GIF animation from images")
    parser.add_argument("--duration", type=float, default=duration, help="Duration (in seconds) of each frame")
    parser.add_argument("--loop", type=int, default=loop, help="Number of times the GIF animation should loop (0 for infinite loop)")
    parser.add_argument("--delay_last_frame", type=float, default=delay_last_frame, help="Delay (in seconds) for the last frame to stay visible")
    args = parser.parse_args()
    create_gif(output_dir, turns, "tetris_animation.gif", duration=0.2)
