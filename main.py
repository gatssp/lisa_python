import pygame as pg
pg.init()

clock = pg.time.Clock()

pg.display.set_caption("Tiger's game") # задали название приложению

bg_sound = pg.mixer.Sound('sounds/bg.mp3') # загрузили фоновый звук приложения
bg_sound.play() # установили фоновый звук приложения

width = 900
heigt = 600
game_screen = pg.display.set_mode((width, heigt)) # описание игрового дисплея
# комментарий ради комментария
icon_game = pg.image.load('images/icon_tiger.png')
pg.display.set_icon(icon_game) # установили изображение "иконки" приложения

# Описание объектов игры (персонаж, враг, фон)
bg_game = pg.image.load('images/bg_game.jpg')# загрузили фоновое изображение
bg_game_over= pg.image.load('images/game-over-screen.jpg')
enemy = pg.image.load('images/bird.png') # загрузили изображение врага
bullet = pg.image.load('images/paintball.png')

bullets=[]
enemy_list_in_game=[]
walk_right = [pg.image.load('images/player/right_walk/tiger1.png'),
              pg.image.load('images/player/right_walk/tiger2.png'),
              pg.image.load('images/player/right_walk/tiger3.png'),
              pg.image.load('images/player/right_walk/tiger4.png'),
              pg.image.load('images/player/right_walk/tiger5.png')] # создали список из "спрайтсов" основного игрока вправо
walk_left = [pg.image.load('images/player/left_walk/tiger1r.png'),
              pg.image.load('images/player/left_walk/tiger2r.png'),
              pg.image.load('images/player/left_walk/tiger3r.png'),
              pg.image.load('images/player/left_walk/tiger4r.png'),
              pg.image.load('images/player/left_walk/tiger5r.png')] # создали список из "спрайтсов" основного игрока налево

player_speed = 5 # скорость передвижения игрока в пикселях
player_x = 100 # координата изображения игрока по Икс
player_y = 370 # координата изображения игрока по Игрику
bg_x = 0 # координата фонового изображения по Икс

my_font = pg.font.Font("fonts/RobotoCondensed-Bold.ttf", 38)
lose = my_font.render('Game OVER' , False, (186, 34, 44))
restart = my_font.render('RESTART' , False, (34, 168, 186))

restart_rect = restart.get_rect(topleft=(370, 400))

enemy_timer = pg.USEREVENT + 1
pg.time.set_timer(enemy_timer,3500)

bullet_count = 5
player_count = 0 # переменная счетчик для перебора спрайтсов в цикле
jump_count = 8 # высота передвижения игрока в пикселях

game_play = True # переменная-флаг для определения состояния игры (запущена или проигрыш)
is_jump = False # переменная-флаг для определения прыжка
run_game = True # переменная-флаг для основного цикла

while run_game:

    game_screen.blit(bg_game, (bg_x,0)) # отобразили фоновое изображение в 0, 0 координатах
    game_screen.blit(bg_game, (bg_x + 900, 0))  # отобразили фоновое изображение в координатах икс + 900 (900- кол-во пискселей в ширину экрана)

    if game_play == True:

        player_rect = walk_left[0].get_rect(topleft=(player_x,player_y))


        if enemy_list_in_game: # ([x, y] [x1,y2])
            for (i,el) in enumerate (enemy_list_in_game):
                game_screen.blit(enemy, el)
                el.x -= 12

                if el.x < -12:
                    enemy_list_in_game.pop(i)

                if player_rect.colliderect(el):
                    game_play = False

        pressed_keys = pg.key.get_pressed() # переменная pressed_keys проверяет на действие нажатие клавиши

        if pressed_keys[pg.K_LEFT]:
            game_screen.blit(walk_left[player_count], (player_x,player_y)) # отобразили спрайтс игрока с индексом [счетчик] в координатах из "дано"
        else:
            game_screen.blit(walk_right[player_count], (player_x, player_y))

        if player_count == 4: # если счетчик равен 4 (4 потому что спрайтсов в списке 5, а перебор начинается с 0, т е индексы в списке: 0-4)
            player_count = 0 # то обнуляем счетчик для того, чтобы начать перебор спрайтсов заново
        else:
            player_count += 1

        bg_x -= 4 # кол-во пикселей по координате икс на которое смещается фоновая картинка при каждой итерации
        if bg_x == -900: # если фон сместился на 900 пикселей
            bg_x = 0 # cново поставить координату по икс=0

        if pressed_keys[pg.K_w]:
            bullets.append(bullet.get_rect(topleft=(player_x + 100, player_y + 100)))

        if bullets:
            for (i, el ) in enumerate(bullets):
                game_screen.blit(bullet, (el.x, el.y))
                el.x += 4

                if el.x > 910:
                    bullets.pop(i)

                if enemy_list_in_game:
                    for(index, enemy_el) in enumerate(enemy_list_in_game):
                        if el.colliderect(enemy_el):
                            enemy_list_in_game.pop(index)
                            bullets.pop(i)


        if pressed_keys[pg.K_LEFT] and player_x > 50: # если нажата кнопка влево и координата игорка по иксу больше 50
            player_x -= player_speed # смещение координат игорка по иксу на кол-во пикселей указанных как скорость игрока влево
        elif pressed_keys[pg.K_RIGHT] and player_x < 800:
            player_x += player_speed

        if not is_jump:  # проверака на значение, уходим в первую ветку только если is_jump = False
            if pressed_keys[pg.K_SPACE]:
                is_jump = True
        else:  # ветка запускается сразу после замены значения is_jump  на True
            if jump_count >= -8:  # если высота передвижения игрока в пикселях >= -7

                if jump_count > 0:
                    player_y -= ( jump_count ** 2) / 2  # смещение координат игорка по игреку на кол-во пикселей указанных как высотапрыжка (формула для плавности прыжка) вверх
                else:
                    player_y += (jump_count ** 2) / 2  # вниз
                jump_count -= 1

            else:
                is_jump = False
                jump_count = 8

        pg.display.update()
    else:
        game_screen.fill('BLACK')
        game_screen.blit(lose, (350,300))
        game_screen.blit(restart, restart_rect)

        mouse = pg.mouse.get_pos()
        if restart_rect.collidepoint(mouse) and pg.mouse.get_pressed()[0]:
            game_play = True
            player_x = 100
            enemy_list_in_game.clear()
            bullets.clear()



        # Цикл закрытия приложения

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run_game = False
            pg.quit

        if event.type == enemy_timer:
            enemy_list_in_game.append(enemy.get_rect(topleft=(905, 465)))


    clock.tick(14) # 14 - колво фреймов (смен картинок) в секунду
    pg.display.update()
pg.quit()


