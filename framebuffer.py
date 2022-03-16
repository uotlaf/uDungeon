# -*- coding: utf-8 -*-
""" Controla e escreve na tela do terminal """

from os import system

class framebuffer:
    '''
        Escreve todos os items na tela no seu devido lugar.
    '''
    def __init__(self, term_size: tuple) -> None:
        '''
            Cria e popula os buffers da tela
        '''
        self.create_buffers(term_size)
        self.size = (term_size)

    def create_buffers(self, term_size: tuple) -> None:

        width, height = term_size
    
        # txt_buf tem sempre tamanho 5, já que desenhar a caixa tira 2 linhas
        txt_buf_h = 5 
        ico_buf_h  = height - txt_buf_h - 1 # O resto da tela

        # Cria e expande os buffers
        self.txt_buf = [[" " for _ in range(width)] for _ in range(txt_buf_h)]
        self.ico_buf = [[" " for _ in range(width)] for _ in range(ico_buf_h)]

        # Variável com o tamanho do buffer
        self.ico_buf_size = (width, len(self.ico_buf))

    def clear_buffers(self) -> None:
        '''Limpa os buffers para escrita nova e redesenha a caixa de texto'''
        self.clear_icon_buffer()
        self.clear_text_buffer()

    def disable_cursor(self) -> None:
        system('tput civis')

    def enable_cursor(self) -> None:
        system('tput cnorm')

    def clear_icon_buffer(self) -> None:
        '''Limpa só o buffer de ícones'''
        for i in self.ico_buf:
            for j in range(len(i)):
                i[j] = " "
            i[0] = "\x1b[0m " # Impede que as cores pulem de linha
    
    def clear_text_buffer(self) -> None:
        '''Limpa só o buffer de texto e redesenha a caixa'''
        for i in self.txt_buf:
            for j in range(len(i)):
                i[j] = " "

        # Desenha a caixa de texto
        self.txt_buf[0][0] = "\x1b[0m╔"
        self.txt_buf[0][-1] = "╗"
        self.txt_buf[0][1:-1] = "═" * len(self.txt_buf[0][1:-1])
        for i in self.txt_buf[1:-1]:
            i[0] = "║"
        for i in self.txt_buf[1:-1]:
            i[-1] = "║"
        self.txt_buf[-1][0]="╚"
        self.txt_buf[-1][1:-1] = "═" * len(self.txt_buf[-1][1:-1])
        self.txt_buf[-1][-1]="╝"

    def quebra_string(self, string: str,
                      limite: int) -> list:
        '''Quebra a string em x linhas, baseado no limite de caracteres'''
        lista = []
        restante = len(string)
        counter = 0

        # Quebra a string em X linhas
        while restante > 0:
            str_quebrada = string[(limite * counter):(limite * (counter + 1))]
            restante -= len(str_quebrada)
            counter += 1
            lista.append(str_quebrada)

        return lista

    def draw_text(self, string: str) -> None:
        """ Desenha uma string no buffer de texto"""

        # Limpa o buffer de texto
        self.clear_text_buffer()

        # Pega o tamanho do buffer de texto pra quebrar as linhas
        tamanho_buffer = len(self.txt_buf[1][1:-1]) 

        # Divide a string em X linhas
        string_quebrada = self.quebra_string(string, tamanho_buffer)

        # Escreve as x primeiras linhas da string no buffer.
        # -2 = caracteres de desenho de caixa
        if len(string_quebrada) > 1:
            for i in range(len(string_quebrada)):
                self.txt_buf[i+1][1:len(string_quebrada[i]) + 1] = string_quebrada[i] 
        else:
            self.txt_buf[1][1:len(string_quebrada[0]) + 1] = string_quebrada[0] 
    
    def draw_icon(self, icon: list, sprite : bool = False) -> None:
        ''' 
            Desenha um ícone no buffer de ícone
            icon = lista com os pixels do ícone
            sprite = Não retorna a cor para o padrão no final do sprite, 
            para não bagunçar o bg
        '''

        altura_icon  = len(icon)
        largura_icon = len(icon[0]) 
        altura_fb = len(self.ico_buf)
        largura_fb= len(self.ico_buf[0]) 

        # Margem para desenho
        margem_y = (altura_fb//2) - (altura_icon//2)
        margem_x = (largura_fb//2) - (largura_icon//2)

        # Desenha o ícone no meio da tela com transparência
        for linha in range(altura_icon):
            for coluna in range(largura_icon):
                if icon[linha][coluna] != " ": # Pula se o icon for transparente
                    self.ico_buf[margem_y + linha][margem_x + coluna] = icon[linha][coluna]
            # Corrige o final do bg            
            if sprite == False and (margem_x + coluna + 1) < largura_fb:
                self.ico_buf[margem_y + linha][margem_x + coluna + 1] = "\x1b[0m "

    def update_screen(self) -> None:
        ''' Imprime os buffers na tela '''
        temp_buf = ""

        # Retorna o cursor para o início da tela
        temp_buf += "\x1b[0;0f"

        # Buffer de ícones
        for col in self.ico_buf:
            for linha in col:
                temp_buf += linha

        # Buffer de texto
        for col in self.txt_buf:
            for linha in col:
                temp_buf += linha


        # Popula a última linha da tela com " ", para entrada de respostas
        largura_fb = len(self.txt_buf[0])
        temp_buf += " " * largura_fb + f"\x1b[{largura_fb}D"

        # Imprime o buffer na tela
        print(temp_buf, end="", flush=True)

