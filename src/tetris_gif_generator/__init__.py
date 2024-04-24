import imageio
from PIL import Image, ImageDraw


# Tetrisのゲーム盤を生成する関数
def generate_tetris_board(width, height):
    # 1マスのサイズ
    cell_size = 20
    # ボードのサイズ
    board_width = width * cell_size
    board_height = height * cell_size
    # ゲーム盤の画像を生成
    board_img = Image.new('RGB', (board_width, board_height), color='white')
    draw = ImageDraw.Draw(board_img)
    # 盤面を描画
    for x in range(0, board_width, cell_size):
        for y in range(0, board_height, cell_size):
            draw.rectangle([x, y, x+cell_size, y+cell_size], outline='black')
    return board_img

def main():
    # テスト用の盤面サイズ
    width = 10
    height = 20
    # Tetrisのゲーム盤画像を生成
    tetris_board = generate_tetris_board(width, height)
    # 画像を保存
    tetris_board.save('tetris_board.png')

    # 生成した画像からGIFを作成する関数
    def create_gif(images, filename, duration=0.5):
        with imageio.get_writer(filename, mode='I', duration=duration) as writer:
            for image in images:
                writer.append_data(image)

    # GIFを作成する
    # create_gif([tetris_board]*10, 'tetris_animation.gif', duration=0.2)
