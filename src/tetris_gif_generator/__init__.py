import os

import imageio
from PIL import Image, ImageDraw

# 色情報を定義
colors = [
    (  64,  64,  64), # 灰
    (   0, 255, 255), # 水
    (   0,   0, 255), # 青
    ( 255, 165,   0), # 橙
    ( 255, 255,   0), # 黄
    (   0, 255,   0), # 緑
    ( 138,  43, 226), # 紫
    ( 255,   0,   0), # 赤
    ( 192, 192, 192), # 黒
]

output_dir = 'img'

# Tetrisのゲーム盤を生成する関数
def generate_tetris_board(field, turns, height, width):
    # 1マスのサイズ
    cell_size = 20
    # ボードのサイズ
    board_width = (width + 2) * cell_size  # 左右に1ブロック広げる
    board_height = (height + 1) * cell_size  # 下に1ブロック広げる
    # ゲーム盤の画像を生成
    board_img = Image.new('RGB', (board_width, board_height), color='white')
    draw = ImageDraw.Draw(board_img)
    
    # 左右のブロックを黒で塗る
    for y in range(height + 1):
        draw.rectangle([0, y * cell_size, cell_size, (y + 1) * cell_size], fill=colors[8], outline='black')  # 左側
        draw.rectangle([board_width - cell_size, y * cell_size, board_width, (y + 1) * cell_size], fill=colors[8], outline='black')  # 右側
    # 下のブロックを黒で塗る
    for x in range(width + 2):
        draw.rectangle([x * cell_size, board_height - cell_size, (x + 1) * cell_size, board_height], fill=colors[8], outline='black')

    # 盤面を描画
    for turn in range(turns):
        for x in range(width):
            for y in range(height):
                # ターンごとの座標を計算
                pos_x = (x + 1) * cell_size  # 左端から1つ分ずらす
                pos_y = y * cell_size  # 上端から1つ分ずらす
                # ターンごとの色を取得
                field_index = field[turn][y][x]
                color = colors[field_index]
                # 長方形を描画
                draw.rectangle([pos_x, pos_y, pos_x + cell_size, pos_y + cell_size], fill=color, outline='black')

        # 画像を保存
        filename = os.path.join(output_dir, f'turn{turn}.png')
        board_img.save(filename)

    return
          
# 生成した画像からGIFを作成する関数
def create_gif(images, filename, duration=0.5):
    with imageio.get_writer(filename, mode='I', duration=duration) as writer:
        for image in images:
            writer.append_data(image)

def main():
    with open('in.txt', 'r') as file:
        # ターン数、高さ、幅を読み込む
        turns, height, width = map(int, file.readline().split())
        
        # 盤面情報を3次元配列として読み込む
        board_data = []
        for _ in range(turns):
            turn_data = []
            for _ in range(height):
                row = list(map(int, file.readline().split()))
                turn_data.append(row)
            board_data.append(turn_data)

    # Tetrisのゲーム盤画像を生成
    generate_tetris_board(board_data, turns, height, width)

    # GIFを作成する
    # create_gif([tetris_board]*10, 'tetris_animation.gif', duration=0.2)
