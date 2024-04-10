Fábio Naconeczny da Silva
GRR 20211782
fabio.silva1@ufpr.br


Implementação do Projeto Photomosaic


A execução do programa deve ser feita da seguinte forma:


$ python3 photomosaic.py main_image_path dir_path feature_file repet scale


Através dos argumentos, obtemos o caminho para a imagem que será utilizada como base para criar o mosaico (main_image_path), o diretório que contém as fotos a serem utilizadas no mosaico (dir_path), o arquivo onde serão escritas as características principais (feature_file), uma flag indicando se é permitida ou não a repetição de imagens deste conjunto (repet), e a ordem da matriz que divide a imagem principal em uma grade NxN (scale).
Para a implementação, foi necessário utilizar a biblioteca OpenCV para o tratamento e processamento das imagens, e NumPy para extrair algumas características dessas imagens, como a média de cores.
Após inicializar a imagem original, obtemos suas dimensões e as salvamos nas variáveis image_width e image_height, que utilizamos para calcular o tamanho proporcional dos "tiles" (imagens que comporão o mosaico) baseados no argumento scale, recebido como parâmetro.
Em seguida, para cada imagem do banco de imagens, calculamos sua cor média na função average_color e a guardamos em uma lista tiles_colors, composta por tuplas no formato (nome da imagem, cor média da imagem). Ambas as características são escritas no arquivo de características especificado por feature_file.
Posteriormente, dividimos a imagem original em seções do tamanho dos "tiles", extraímos sua cor média e a salvamos em section_colors, outra lista de tuplas definida por (cor da seção, (posição_x, posição_y)).
Com todas essas informações, o próximo passo é mapear cada seção da imagem original com a imagem correspondente do diretório, calculando a diferença euclidiana entre as médias de cores das imagens do diretório (tiles_colors) e as seções da imagem original (section_colors). Essas melhores combinações são então adicionadas a outra lista de tuplas, tile_section_concat, juntamente com a posição na imagem principal.
Por fim, uma nova imagem em branco é criada e, para cada posição definida em tile_section_concat, um "tile" é colocado sucessivamente até o término. Como não foi implementado um tratamento de contornos, uma das limitações do programa é que se a ordem da matriz passada na execução do programa for muito pequena, a imagem resultante fragmentada pode não se assemelhar muito à original.