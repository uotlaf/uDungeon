# -*- coding: utf-8 -*-
"""
    Contém os objetos que serão usados pelo jogo. Atualmente só o player
    está aqui
"""

from os import walk, get_terminal_size
from image_to_list import image_to_text

class obj_player:
    """ Gerencia e desenha o player dentro do cenário"""
    def __init__(self) -> None: 
        """Inicia as variáveis do personagem"""
        # Default
        self.ic_fb_size = (15, 15)

        # Localização em PORCENTAGEM
        self.sprite_x = self.sprite_y = 0 # Porcentagem da tela
        
        # Tamanho
        self.sprite_h = self.sprite_w = 0
        
        # Orientação
        self.orientation = 0

        # Movimento
        self.moveTo_x = self.moveTo_y = 0
        self.walk_step = 3

        # Animação
        self.sprites = []
        self.cur_sprite = 0 # Alterna o sprite atual
        self.cur_orientation = 0 # 0 = pra frente. 1 = pra trás

        # Outros
        self.sprite_folder = ""
        self.bg_size = (0, 0)
    
    def get_sprites(self) -> None:
        ''' Cria os sprites do personagem '''

        # Reinicia as infos dos sprites. Impede que o programa fique adicionando vários sprites
        self.sprites = []
        self.cur_orientation = 0
        self.cur_sprite = 0

        # Adiciona os arquivos na lista self.sprites
        for _, _, arquivos in walk(self.sprite_folder):
            for arquivo in arquivos:
                self.sprites.append(image_to_text(f"{self.sprite_folder}/{arquivo}", self.bg_size))

        # Calcula o tamanho de todos os sprites baseado no primeiro
        self.sprite_w = len(self.sprites[0])
        self.sprite_h = len(self.sprites[0][0])

    def draw_sprite_margin(self) -> list:
        '''
            Desenha o sprite com uma margem dentro de um sprite maior
            O tamanho do sprite maior é igual ao tamanho do background
            Retorna o sprite maior
        '''

        # Calcula onde o sprite vai ficar dentro do bg      
        atual_x = int(self.bg_size[0]*(self.sprite_x/100)) 

        # Pega o sprite atual e o cria um novo
        sprite_atual = self.sprites[self.cur_sprite]
        sprite_novo = []

        # Popula o sprite novo com o tamanho da bg
        sprite_novo = [[" " for _ in range(self.bg_size[0])] for _ in range(self.bg_size[1])]

        # Coloca o sprite atual dentro do novo, depois da margem
        for linha in range(len(sprite_atual)):
            for coluna in range(len(sprite_atual[0])):
                sprite_novo[linha + 1][coluna+atual_x] = sprite_atual[linha][coluna]

        return sprite_novo

    def walk_loop_completed(self) -> bool:
        """ Verifica quando o personagem para de se mover"""
        return True if self.moveTo_x == self.sprite_x else False

    def draw(self) -> list:
        '''
            Devolve uma lista com transparência,
            Para o framebuffer escrever
        '''

        # Troca a orientação do sprite, se necessário
        if self.orientation != self.cur_orientation:
            for sprite in range(len(self.sprites)):
                for linha in range(len(self.sprites[sprite])):
                    self.sprites[sprite][linha].reverse()
            self.cur_orientation = self.orientation
                    

        # Alterna os sprites quando se mover
        if self.moveTo_x > self.sprite_x:
            self.orientation = 0
            self.sprite_x += self.walk_step
            self.cur_sprite += 1
        elif self.moveTo_x < self.sprite_x:
            self.orientation = 1
            self.sprite_x -= 1
            self.cur_sprite += 1

        # Retorna o contador pra 0 se o sprite não existir
        if self.cur_sprite > len(self.sprites) - 1:
            self.cur_sprite = 0

        return self.draw_sprite_margin()

class informacoes:
    # Informações do jogador que são sobrescritas ao decorrer do jogo
    nome = "Padrão"
    idade = 12
    experiente = False
    mortos = []
