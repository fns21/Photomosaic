import os
import sys
from PIL import Image
import numpy as np
import cv2

def average_color(img):
    average_color = np.average(np.average(img, axis=0), axis=0)
    average_color = np.around(average_color, decimals=-1)
    average_color = tuple(int(i) for i in average_color)
    return average_color

def process_images(main_image_path, dir_path, feature_file, repet, scale):
    # Abrir a imagem principal
    main_image = cv2.imread(main_image_path)

    main_image = cv2.cvtColor(main_image, cv2.COLOR_BGR2RGB)

    image_height, image_width, _ = main_image.shape

    tiles_width = image_width // int(scale)
    tiles_height = image_height // int(scale)

    # Listar imagens no diretório especificado
    tiles = os.listdir(dir_path)

    # Lista para armazenar as cores médias de cada imagem
    tiles_colors = []
    for image in tiles:
        image_path = os.path.join(dir_path, image)
        img = cv2.imread(image_path)
        color = average_color(img)
        tiles_colors.append((image, color))

    # Escrever no arquivo de características as cores médias
    with open(feature_file, 'w') as arquivo_txt:
        for tile, cor_media in tiles_colors:
            arquivo_txt.write(f"{tile} = {cor_media}\n")

    section_colors = []
    for y in range(0, image_height, tiles_height):
        for x in range(0, image_width, tiles_width):
            y1 = y
            y2 = y + tiles_height
            x1 = x
            x2 = x + tiles_width

            # Garantir que as regiões não ultrapassem os limites da imagem
            y2 = min(y2, image_height)
            x2 = min(x2, image_width)

            # Recortar a seção da main_image
            section = main_image[y1:y2, x1:x2]
            # Processar a seção
            section_color = average_color(section)
            section_colors.append((section_color, (x, y)))

    # Busca pela imagem da base que combine melhor com a seção
    tile_section_concat = []
    for color_section, (x, y) in section_colors:
        best_match_tile = None
        best_match_diff = float('inf')

        for tile_index, (tile, cor_media) in enumerate(tiles_colors):
            # Calculando a diferença de cor
            diff = abs(color_section[0] - cor_media[0]) + \
                abs(color_section[1] - cor_media[1]) + \
                abs(color_section[2] - cor_media[2])

            if diff < best_match_diff:
                best_match_diff = diff
                best_match_tile = tile
                best_match_index = tile_index

        tile_section_concat.append((best_match_tile, (x, y)))

        if repet == 0:
            # Removendo a melhor correspondência da lista pelo índice
            del tiles_colors[best_match_index]
    
    # Abre imagem como outro tipo de obj e cria quadro em branco
    main_image = Image.open(main_image_path)
    mosaic = Image.new('RGB', main_image.size)

    # Posicionar cada tile na imagem
    for tile, (x, y) in tile_section_concat:
        img = cv2.imread(os.path.join(dir_path, tile))
        tile_image = cv2.resize(img, (tiles_width, tiles_height))
        # Calcular as coordenadas na imagem
        image_x = x
        image_y = y
        # Determinar a caixa delimitadora
        box = (image_x, image_y, image_x + tiles_width, image_y + tiles_height)
        # Colocar o tile na posição correta
        mosaic.paste(Image.fromarray(tile_image), box)

    # Salvar a imagem resultante
    mosaic.save("output_image.png")

def main():
    # Extrair argumentos da linha de comando
    main_image_path = sys.argv[1]
    dir_path = sys.argv[2]
    feature_file = sys.argv[3]
    repet = sys.argv[4]
    scale = sys.argv[5]

    # Processar as imagens
    process_images(main_image_path, dir_path, feature_file, repet, scale)

if __name__ == "__main__":
    main()
