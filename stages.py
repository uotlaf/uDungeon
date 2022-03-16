# -*- coding: utf-8 -*-
""" Contém os stages usados no jogo """

from image_to_list import image_to_text
from time import sleep
from os import system

def replit_init_screen(jogador, fb, player):
    system('clear')
    print("ATENÇÃO")
    print("Existem alguns problemas ao executar esse programa no replit:")
    print("1 - NÃO MODIFIQUE O TAMANHO DO TERMINAL QUANDO FOR JOGAR")
    print("2 - O replit tem um bug que fica digitando �� no meio dos quadros.")
    print("    Esse não é um problema do código, e sim do replit.")
    print("3 - O replit é extremamente lento para carregar as telas")
    print("4 - Não aumente muito a altura do terminal do replit.")
    print("    Quanto maior, mais lento o programa se comportará.")
    input("Aperte ENTER para continuar")
    print("Carregando...")

    return menu_principal

def menu_principal(jogador, fb, player):
    fb.clear_buffers()

    # Pré-cache das imagens já transformadas em lista. Necessário no replit
    animacao_inicio = []
    for i in range(0, 53, 2):
        animacao_inicio.append(image_to_text(f'resource/abertura/{i}.png', 
                                             fb.ico_buf_size))


    fb.draw_text("Seja bem vindo ao µDungeon")


    # Executa a animação
    for frame in animacao_inicio:
        fb.draw_icon(frame)
        fb.update_screen()
        sleep(0.1)

    input("Digite enter para continuar")

    return perguntas # Retorna a próxima tela

def perguntas(jogador, fb, player):
    fb.clear_buffers()


    # Pergunta o nome. Como não é uma animação, o pré-cache não é necessário
    while True:
        fb.draw_icon(image_to_text(f'resource/selecao/0.png', fb.ico_buf_size))
        fb.draw_text("Primeiro, me diga o nome do aventureiro")
        fb.update_screen()

        fb.enable_cursor()
        nome = input("Digite o nome do aventureiro: ").capitalize()
        fb.disable_cursor()
        if not nome: # Se o nome estiver vazio
            fb.draw_text("JÁ VIU ALGUÉM COM O NOME VAZIO?")
            fb.update_screen()
            sleep(1)
            continue
        if nome in jogador.mortos: # Verifica se o personagem "nome" está morto ou não
            fb.draw_text(f"{nome} morreu. Quem sabe onde está o corpo dele?")
            fb.update_screen()
            sleep(3)
        else:
            jogador.nome = nome
            break


    # Pergunta a idade
    while True:
        fb.draw_icon(image_to_text(f'resource/selecao/1.png', fb.ico_buf_size))
        fb.draw_text(f"Quantos anos {jogador.nome} tem?")
        fb.update_screen()

        fb.enable_cursor()
        idade = input("Digite sua idade: ")
        fb.disable_cursor()

        # Checa se a idade é um número, e se ela está entre 6 e 100
        if not idade.isdecimal() or not idade or int(idade) < 6 or int(idade) > 100:
            fb.draw_text("Tá achando que eu nasci ontem?")
            fb.update_screen()
            sleep(1)
        else:
            jogador.idade = idade
            break


    # Pergunta para propósitos questionáveis
    while True:
        fb.draw_icon(image_to_text(f'resource/selecao/2.png', fb.ico_buf_size))
        fb.draw_text("Já jogou algum outro adventure na vida?" + 
                     " (Só pra saber mesmo, não vai mudar nada no gameplay)")
        fb.update_screen()

        fb.enable_cursor()
        resposta = input("Responda com sim/não: ").lower()
        fb.disable_cursor()

        if not resposta or resposta[0] != "s" and resposta[0] != "n":
            fb.draw_text("Não é porque não vai mudar nada que tu não tem que responder")
            fb.update_screen()
            sleep(1)
        else:
            jogador.experiente = True if resposta[0] == 's' else False
            break


    # Pré-cache da animação do fim da tela
    animacao_fim = []

    for i in range(3, 16):
        animacao_fim.append(image_to_text(f'resource/selecao/{i}.png', 
                                          fb.ico_buf_size))

    # Executa a animacao
    for frame in animacao_fim:
        fb.draw_icon(frame)
        fb.update_screen()
        sleep(0.1)

    return apresentacao_1 # Próxima tela

def apresentacao_1(jogador, fb, player):
    fb.clear_buffers()


    # Pré-cache
    animacao_1 = [] # Cutscene de apresentação
    animacao_jungle = [] # Cutscende da jungle
    animacao_2 = [] # Cutscene do tesouro
    animacao_inicio = [] # Cutscene repetida do início


    for i in range(10): 
        animacao_1.append(image_to_text(f"resource/apresentacao_1/{i}.png", fb.ico_buf_size))
    
    for i in range(7):
        animacao_jungle.append(image_to_text(f"resource/apresentacao_2/{i}.png", fb.ico_buf_size))

    for i in range(29):
        animacao_2.append(image_to_text(f"resource/apresentacao_3/{i}.png", fb.ico_buf_size))

    for i in range(0, 53, 2): # 2 = frameskip
        animacao_inicio.append(image_to_text(f'resource/abertura/{i}.png', fb.ico_buf_size))



    # Inicio da apresentação

    fb.draw_text(f"Você é {jogador.nome}, um explorador de {jogador.idade} anos.")

    for frame in animacao_1: # Mostra as imagens na tela
        fb.draw_icon(frame)
        fb.update_screen()
        sleep(0.3)
    sleep(1)


    fb.draw_text("Ao longo da vida, você explorou várias cavernas e templos escondidos pelo mundo")
    
    for frame in animacao_jungle:
        fb.draw_icon(frame)
        fb.update_screen()
        sleep(0.5)
    sleep(1)

   
    fb.draw_text("Sempre achando tesouros poderosos antes perdidos")

    for frame in animacao_2:
        fb.draw_icon(frame)
        fb.update_screen()
        sleep(0.1)
    sleep(1)

   

    fb.clear_icon_buffer() # Tamanho diferentes das imagens = limpa o buffer antes

    fb.draw_text(f"Um dia {jogador.nome} acha um templo diferente")

    for frame in animacao_inicio:
        fb.draw_icon(frame)
        fb.update_screen()
        sleep(0.1)
    input("Digite enter para continuar")

    return solo

def solo(info, fb, player):
    fb.clear_buffers()


    solo_bg = image_to_text(f"resource/bg/solo.png", 
                            fb.ico_buf_size)


    # Reinicia o player
    player.cur_orientation = 0
    player.sprite_x = 0
    player.bg_size = (len(solo_bg[0]), len(solo_bg))
    player.get_sprites()

    # Desenha os itens da tela
    fb.draw_text(f"{info.nome} entra no primeiro 'andar' do terreno," +
                  "e se depara com um vaso de planta, um quadro e uma porta")
    fb.draw_icon(solo_bg)
    fb.draw_icon(player.draw(), True)
    fb.update_screen()

    fb.draw_text(f"O que {info.nome} deve fazer?")

    while True:
        fb.update_screen()

        # Liga o cursor, pergunta e desabilita logo em seguida
        fb.enable_cursor()
        resposta = input("Digite a próxima ação(Observar/Pegar/Andar até/Ajuda/Lista): ").lower().split()
        fb.disable_cursor()


        if len(resposta) == 0:
            continue

        # Verifica todos os argumentos
        if resposta[0] == "observar":
            if len(resposta) > 1:
                if resposta[1] == "vaso":
                    fb.draw_text("Um vaso de planta estranho")
                elif resposta[1] == "rachadura":
                    fb.draw_text("Uma rachadura na parede")
                elif resposta[1] == "quadro":
                    fb.draw_text("Uma pintura. Não me é estranha")
                elif resposta[1] == "porta":
                    fb.draw_text("Acho que é a próxima sala")
                else:
                    fb.draw_text(f"{resposta[1]}? Nem sei o que é isso")
            else:
                fb.draw_text("É pra observar o quê?. Tá com dificuldade? Digita ajuda")
        elif resposta[0] == "pegar":
            if len(resposta) > 1:
                if resposta[1] == "vaso":
                    return solo_pegar_vaso
                elif resposta[1] == "rachadura":
                    fb.draw_text("Como se pega uma rachadura?")
                elif resposta[1] == "quadro":
                    # Move o player para onde o quadro está
                    player.moveTo_x = 73
                    while not player.walk_loop_completed():
                        fb.draw_icon(solo_bg)
                        fb.draw_icon(player.draw(), True)
                        fb.update_screen()
                        sleep(0.1)
                    fb.draw_text("Parece caro.")
                elif resposta[1] == "porta":
                    fb.draw_text("Como se pega uma porta?")
                else:
                    fb.draw_text("Sei lá o que é isso")
            else:
                fb.draw_text("É pra pegar o que?")
        elif resposta[0] == "andar":
            # Move o player para onde o item está
            if len(resposta) > 2:
                if resposta[2] == "vaso":
                    player.moveTo_x = 28
                    while not player.walk_loop_completed():
                        fb.draw_icon(solo_bg)
                        fb.draw_icon(player.draw(), True)
                        fb.update_screen()
                        sleep(0.1)
                elif resposta[2] == "rachadura":
                    player.moveTo_x = 48
                    while not player.walk_loop_completed():
                        fb.draw_icon(solo_bg)
                        fb.draw_icon(player.draw(), True)
                        fb.update_screen()
                        sleep(0.1)
                elif resposta[2] == "quadro":
                    player.moveTo_x = 73
                    while not player.walk_loop_completed():
                        fb.draw_icon(solo_bg)
                        fb.draw_icon(player.draw(), True)
                        fb.update_screen()
                        sleep(0.1)
                elif resposta[2] == "porta":
                    player.moveTo_x = 90
                    while not player.walk_loop_completed():
                        fb.draw_icon(solo_bg)
                        fb.draw_icon(player.draw(), True)
                        fb.update_screen()
                        sleep(0.1)
                    # Entra na porta
                    return puzzle_portas_1
            else:
                fb.draw_text("Andar até onde?")
        elif resposta[0] == "ajuda":
            fb.draw_text("Digite Observar <local>; Digite Pegar <local>; Digite Andar <local>;")
            fb.update_screen()
            sleep(2)
            fb.draw_text("Digite lista pra ver uma lista de itens que estão na tela")
        elif resposta[0] == "lista":
            fb.draw_text("Vaso | Rachadura | Quadro | Porta")
        else:
            fb.draw_text("Digite alguma coisa")

def solo_pegar_vaso(info, fb, player):

    solo_bg = image_to_text(f"resource/bg/solo.png", fb.ico_buf_size)

    # Pré-cache da animação
    animacao_vaso = []
    for i in range(10):
        animacao_vaso.append(image_to_text(f"resource/animacoes/vaso{i}.png", 
                                            fb.ico_buf_size))

    fb.draw_icon(solo_bg)

    # Anda até onde o vaso está.
    player.moveTo_x = 28
    while not player.walk_loop_completed():
        fb.draw_icon(solo_bg)
        fb.draw_icon(player.draw(), True)
        fb.update_screen()
        sleep(0.1)

    # Executa a animação da cobra
    for frame in animacao_vaso:
        fb.draw_icon(frame)
        fb.draw_icon(player.draw(), True)
        fb.update_screen()
        sleep(0.1)
    
    info.mortos.append(info.nome)
    fb.draw_text( "Não era uma planta, e sim uma cobra! " +
                 f"{info.nome} infelizmente não resistiu.")
    fb.update_screen()
    input("Pressione enter para voltar pro menu principal")

    return menu_principal

def puzzle_portas_1(info, fb, player):
    fb.clear_buffers()

    andar_2_bg = image_to_text("resource/bg/portas_puzzle0.png",
                               fb.ico_buf_size)

    # Reinicia o player
    player.bg_size = (len(andar_2_bg[0]), len(andar_2_bg))
    player.get_sprites()
    player.sprite_x = 0

    # Desenha na tela
    fb.draw_text(f"{info.nome} encontra uma bifurcação")
    fb.draw_icon(andar_2_bg)
    fb.draw_icon(player.draw(), True)

    while True:
        fb.update_screen()
        # Pergunta
        fb.enable_cursor()
        resposta = input(f"Para onde {info.nome} deve ir? [esquerda/direita] ").lower()
        fb.disable_cursor()

        # Verifica os argumentos
        if resposta == "esquerda":
            player.moveTo_x = 30
            while not player.walk_loop_completed():
                fb.draw_icon(andar_2_bg)
                fb.draw_icon(player.draw(), True)
                fb.update_screen()
                sleep(0.1)
            return puzzle_portas_2
        elif resposta == "direita":
            player.moveTo_x = 59
            while not player.walk_loop_completed():
                fb.draw_icon(andar_2_bg)
                fb.draw_icon(player.draw(), True)
                fb.update_screen()
                sleep(0.1)
            # Reinicia o puzzle
            return puzzle_portas_1

def puzzle_portas_2(info, fb, player):
    fb.clear_buffers()

    andar_2_bg = image_to_text("resource/bg/portas_puzzle1.png", fb.ico_buf_size)

    # Reinicia o player
    player.bg_size = (len(andar_2_bg[0]), len(andar_2_bg))
    player.get_sprites()
    player.sprite_x = 0

    fb.draw_text(f"{info.nome} encontra outra bifurcação")

    fb.draw_icon(andar_2_bg)
    fb.draw_icon(player.draw(), True)


    while True:
        fb.update_screen()
        # Pergunta
        fb.enable_cursor()
        resposta = input(f"Para onde {info.nome} deve ir? [esquerda/direita] ").lower()
        fb.disable_cursor()

        # Verifica os argumentos
        if resposta == "esquerda":
            player.moveTo_x = 30
            while not player.walk_loop_completed():
                fb.draw_icon(andar_2_bg)
                fb.draw_icon(player.draw(), True)
                fb.update_screen()
                sleep(0.1)
            # Reinicia o puzzle
            return puzzle_portas_1
        elif resposta == "direita":
            player.moveTo_x = 59
            while not player.walk_loop_completed():
                fb.draw_icon(andar_2_bg)
                fb.draw_icon(player.draw(), True)
                fb.update_screen()
                sleep(0.1)
            # Prossegue
            return puzzle_portas_3

def puzzle_portas_3(info, fb, player):
    fb.clear_buffers()

    andar_2_bg = image_to_text("resource/bg/portas_puzzle2.png", fb.ico_buf_size)

    # Reinicia o player
    player.bg_size = (len(andar_2_bg[0]), len(andar_2_bg))
    player.get_sprites()
    player.sprite_x = 0

    fb.draw_text(f"{info.nome} agora encontra uma trifurcação. Já viu se essas portas matassem?")

    fb.draw_icon(andar_2_bg)
    fb.draw_icon(player.draw(), True)


    while True:
        fb.update_screen()
        # Pergunta
        fb.enable_cursor()
        resposta = input(f"Para onde {info.nome} deve ir? [esquerda/centro/direita] ").lower()
        fb.disable_cursor()

        if resposta == "esquerda":
            player.moveTo_x = 30
            while not player.walk_loop_completed():
                fb.draw_icon(andar_2_bg)
                fb.draw_icon(player.draw(), True)
                fb.update_screen()
                sleep(0.1)
            # Reinicia
            return puzzle_portas_1
        elif resposta == "centro":
            player.moveTo_x = 58
            while not player.walk_loop_completed():
                fb.draw_icon(andar_2_bg)
                fb.draw_icon(player.draw(), True)
                fb.update_screen()
                sleep(0.1)
            # Continua
            return puzzle_tempo_1
        elif resposta == "direita":
            player.moveTo_x = 80
            while not player.walk_loop_completed():
                fb.draw_icon(andar_2_bg)
                fb.draw_icon(player.draw(), True)
                fb.update_screen()
                sleep(0.1)
            # Reinicia
            return puzzle_portas_1

def puzzle_tempo_1(info, fb, player):
    tentativas = 0
    fb.clear_buffers()

    # Duas bg: Uma com a pergunta e uma com a porta
    bg = image_to_text("resource/bg/perguntas.png", fb.ico_buf_size)
    bg_1 = image_to_text("resource/bg/perguntas1.png", fb.ico_buf_size)

    # Pré-cache da animação
    lava_anim = []
    for frame in range(90):
        lava_anim.append(image_to_text(f"resource/animacoes/lava{frame}.png", fb.ico_buf_size))

    # Reinicia o player
    player.bg_size = (len(bg[0]), len(bg))
    player.get_sprites()
    player.sprite_x = 0

    # Escreve
    fb.draw_text(f"{info.nome} encontra uma placa com alguma coisa escrita")
    fb.draw_icon(bg)
    fb.draw_icon(player.draw(), True)
    fb.update_screen()

    while True:
        # Atualiza toda vez que for perguntar
        fb.update_screen()

        # Executa a animação da lava antes de perguntar
        if tentativas > 0: # Animação da lava
            for frame in range(15 * (tentativas - 1), 15 * tentativas):
                fb.draw_icon(lava_anim[frame])
                fb.update_screen()
        
        # Se o jogador morreu
        if tentativas > 5:
            fb.draw_text(f"{info.nome} infelizmente morreu")
            fb.update_screen()
            input("Pressione enter para continuar")
            return menu_principal

        # Pergunta
        fb.enable_cursor()
        resposta = input(f"O que {info.nome} deve fazer?[ler/responder] ").lower()
        fb.disable_cursor()

        # Verifica os argumentos
        if len(resposta) > 0:
            if resposta[0] == "l":
                fb.draw_text("A placa diz:")
                fb.update_screen()
                sleep(2)
                fb.draw_text("Para prosseguir você deverá responder uma pergunta " +
                             "não respondida á séculos pela humanidade. "+ 
                             "Caso não responda, você perecerá")
                fb.update_screen()
                sleep(4)
                fb.draw_text("PORQUE A GALINHA ATRAVESSOU A RUA?")
                fb.update_screen()
                continue # Reinicia o loop

            elif resposta[0] == "r":
                fb.draw_text(f"O que {info.nome} respondeu?")
                fb.update_screen()

                # Pergunta          
                fb.enable_cursor()
                charada_resposta = input("Digite:").lower()
                fb.disable_cursor()
                
                # Verifica se a resposta está certa
                if charada_resposta == "para chegar ao outro lado":
                    break
                else:
                    tentativas += 1
                    continue # Reinicia o loop quando a pessoa errar
        else: # Se a pessoa não digitou nada
            fb.draw_text("Digite alguma coisa")
            tentativas += 1
            fb.update_screen()

    # Caso o jogador acerte, desenha a porta
    fb.draw_icon(bg_1)
    fb.draw_icon(player.draw(), True)
    fb.draw_text("Uma porta apareceu no lugar da placa!")
    fb.draw_icon(lava_anim[15 * tentativas])
    fb.update_screen()

    # Deixa as coisas mais interessantes
    tentativas += 1


    while True:
        if tentativas > 0: # Animação da lava
            for frame in range(15 * (tentativas - 1), 15 * tentativas):
                fb.draw_icon(lava_anim[frame])
                fb.update_screen()

        # Verifica se o jogador morreu
        if tentativas > 5:
            fb.draw_text(f"{info.nome} infelizmente morreu")
            fb.update_screen()
            input("Pressione enter para continuar")
            return menu_principal

        # Pergunta
        fb.enable_cursor()
        resposta = input(f"O que {info.nome} deverá fazer?[entrar/ficar]").lower()
        fb.disable_cursor() 

        # Verifica os argumentos
        if len(resposta) > 0:
            if resposta == "entrar":
                player.moveTo_x = 3
                while not player.walk_loop_completed():
                    fb.draw_icon(bg_1)
                    fb.draw_icon(player.draw(), True)
                    fb.draw_icon(lava_anim[15 * tentativas])
                    fb.update_screen()
                    sleep(0.1)
                return tesouro
            else: # Qualquer outra resposta fará o jogador morrer
                tentativas +=1

def tesouro(info, fb, player):
    fb.clear_buffers()

    bg = image_to_text("resource/bg/tesouro.png", fb.ico_buf_size)
    
    # Reinicia o player
    player.bg_size = (len(bg[0]), len(bg))
    player.get_sprites()
    player.sprite_x = 0
    
    # Desenha na tela
    fb.draw_text(f"{info.nome} finalmente encontra o tesouro! Agora ele tem que " +
                  "descobrir como sair desse lugar")
    fb.draw_icon(bg)
    fb.draw_icon(player.draw(), fb.ico_buf_size)

    while True:
        fb.update_screen()

        # Pergunta
        fb.enable_cursor()
        resposta = input(f"O que {info.nome} deve fazer?[andar/olhar/escavar/lista]").lower().split()
        fb.disable_cursor()
        if len(resposta) == 0:
            continue

        # Verifica os argumentos
        if resposta[0] == "andar":
            if len(resposta) > 2:
                if resposta[2] == "tesouro":
                    player.moveTo_x = 45
                    while not player.walk_loop_completed():
                        fb.draw_icon(bg)
                        fb.draw_icon(player.draw(), True)
                        fb.update_screen()
                        sleep(0.1)
                elif resposta[2] == "rachadura":
                    player.moveTo_x = 90
                    while not player.walk_loop_completed():
                        fb.draw_icon(bg)
                        fb.draw_icon(player.draw(), True)
                        fb.update_screen()
                        sleep(0.1)
                else:
                    fb.draw_text("Sei lá onde é isso")
            else:
                fb.draw_text("Andar até onde?")

        elif resposta[0] == "olhar":
            if len(resposta) > 1:
                if resposta[1] == "tesouro":
                    # Anda até o tesouro
                    player.moveTo_x = 45
                    while not player.walk_loop_completed():
                        fb.draw_icon(bg)
                        fb.draw_icon(player.draw(), True)
                        fb.update_screen()
                        sleep(0.1)
                    fb.draw_text(f"{info.nome}: Puta tesourão! Vou ficar ainda mais rico")

                elif resposta[1] == "rachadura":
                    # Anda até a rachadura
                    player.moveTo_x = 90
                    while not player.walk_loop_completed():
                        fb.draw_icon(bg)
                        fb.draw_icon(player.draw(), True)
                        fb.update_screen()
                        sleep(0.1)
                    fb.draw_text(f"{info.nome} pode tentar escavar aqui!")

        elif resposta[0] == "escavar": # Final do jogo
            if len(resposta) > 1:
                if resposta[1] == "rachadura":
                    # Anda até a rachadura
                    player.moveTo_x = 90
                    while not player.walk_loop_completed():
                        fb.draw_icon(bg)
                        fb.draw_icon(player.draw(), True)
                        fb.update_screen()
                        sleep(0.1)
                    fb.draw_text(f"{info.nome} começa a escavar")
                    fb.update_screen()
                    sleep(2)
                    return fim # Vai pro final do jogo

                elif resposta[1] == "tesouro":
                    fb.draw_text("Como se escava um tesouro?")
            else:
                fb.draw_text("O que é pra escavar?")
        elif resposta[0] == "lista":
            fb.draw_text("tesouro | rachadura")    
     
def fim(info, fb, player):

    fb.clear_buffers()
    
    bg = image_to_text("resource/bg/fim.png", fb.ico_buf_size)

    # Desenha o final do jogo
    fb.draw_icon(bg)
    fb.draw_text(f"{info.nome} conseguiu sobreviver a todos os perigos " +
                  "e ainda conseguiu o tesouro!")
    fb.update_screen()
    input("Pressione enter para continuar")
    
    fb.draw_text("Obrigado por jogar!")
    fb.update_screen()
    input("Pressione enter para voltar ao menu")

    return menu_principal
