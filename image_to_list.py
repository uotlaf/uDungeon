#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''Pega uma imagem(pode ser uma .png) e devolve ela no terminal
   Uso: bitmap_to_list.py <imagem>
   Quando usado como módulo, devolve uma lista com as cores em caracteres ANSI
'''

from PIL import Image # Para processamento de imagem
import numpy as np    # Para converter a imagem em uma lista

# Para uso no terminal
from sys import argv  
from os import get_terminal_size

def image_to_text(image: str, 
                 fb_size: tuple, 
                 fix_final : bool = False) -> list:
    '''
        Pega uma imagem e transforma em uma lista de caracteres ANSI
        image: Localização da imagem
        fb_size: Tupla com o tamanho do terminal
        fix_final: Retorna uma lista com as redefinições de cores '\\x1b[0m' 
    '''

    image = Image.open(image)

    # Calcula a proporção da imagem
    image_ratio = image.size[0]/image.size[1]
    

    # Calcula o tamanho novo da imagem respeitando a proporção dela.
    if image_ratio > 1:
        new_size = [ fb_size[0] - 1, int(fb_size[0] // image_ratio )]
    else:
        new_size = [ int( fb_size[0] // image_ratio), fb_size[0] - 1]

    # Corrige quando a imagem é muito quadrada
    if new_size[1] > fb_size[1]:
        new_size = [ int(fb_size[1] * image_ratio ), fb_size[1] - 1]

    # Redimensiona a imagem usando o filtro NEAREST
    image = image.resize(new_size, Image.NEAREST)
    
    # Transforma a imagem em uma lista
    image_rgb = list(np.array(image))

    # Converte pixels em caracteres ANSI
    imagem_final = []
    for linha in image_rgb:
        imagem_final.append([])
        for coluna in linha:
            pixel_atual = list(coluna)

            # Se o pixel atual for transparente
            if pixel_atual[-1] == 0:
                if fix_final:
                    imagem_final[-1].append("\x1b[0m ")
                else: 
                    imagem_final[-1].append(f" ")
            else: # Se não for, escreve o caractere ANSI no lugar do RGB
                r, g, b, *_ = pixel_atual
                imagem_final[-1].append(f"\x1b[48;2;{r};{g};{b}m ")
        if fix_final: # Retorna a cor para a padrão no final de cada linha
            imagem_final[-1].append("\x1b[0m ")

    return imagem_final

if __name__ == '__main__':
    # Para uso direto no terminal
    resultado = image_to_text(str(argv[1]), get_terminal_size(), True)
    for linha in resultado:
        print(*linha, sep="")

