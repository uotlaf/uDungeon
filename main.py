#!/usr/bin/env python3
# -*- coding: utf-8 -*-

print("Carregando...")

from os import get_terminal_size, environ, system
from time import sleep
from framebuffer import framebuffer
import stages
from objects import obj_player, informacoes

# Identifica se está rodando no replit
replit = True if 'REPL_ID' in environ else False

# Tamanho atual do terminal
act_term_size = get_terminal_size()

# Inicia os buffers
fb = framebuffer(get_terminal_size())

# Inicia o player
player = obj_player()  # Classe do player
player.sprite_folder = "resource/personagem/"  # Pasta com os sprites
player.ic_fb_size = fb.ico_buf_size  # Tamanho dos sprites

# Primeira parte
tela_atual = stages.menu_principal if not replit else stages.replit_init_screen

if __name__ == '__main__':
    # Loop principal
    try:
        while True:
            # Se o terminal mudar de tamanho, refaz os buffers
            new_term_size = get_terminal_size()
            if act_term_size != new_term_size:
                fb.create_buffers(new_term_size)
                fb.size = (new_term_size)
                player.ic_fb_size = (new_term_size)

            # Se o terminal for muito pequeno:
            if new_term_size[0] < 80 or new_term_size[1] < 13:
                system('clear')
                print("\x1b[0;0fAUMENTE UM POUQUINHO O TAMANHO DO TERMINAL")
                sleep(1)
                continue

            # Chama as telas
            fb.disable_cursor()
            # A tela atual vai retornar a próxima tela a ser apresentada
            # Previne um possível stack overflow
            tela_atual = tela_atual(informacoes, fb, player)

    except KeyboardInterrupt:  # Corrige o cursor ao sair jogo com ctrl+c
        print("Limpando...")
        fb.enable_cursor()
