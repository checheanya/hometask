import sys
import argparse

from solid import *
from solid.objects import *
from solid.utils import *

SEGMENTS = 48

"""
Напоминалка: смотрим y - от нас (back-front),
z - вверх (up-down), x - вправо (right-left)
Порядок упоминания - x,y,z

Задаваемые параметры:
1. размер окон;
2. высота замка;
3. высота первой башни;
4. высота второй башни;
5. количество рядов окон;
6. количество окон в ряду.
"""

parser = argparse.ArgumentParser(prog='Castle',
                                 description='''Let's build your own
                                 castle without sms and registration''')
parser.add_argument('-c', '--hight_castle', default=800,
                    type=int, help='Height of castle (default - 800)')
parser.add_argument('-t', '--hight_thin', default=1500,
                    type=int, help='Height of thin tower (default - 1500)')
parser.add_argument('-w', '--hight_wide', default=1200,
                    type=int, help='Height of wide tower (default - 1200)')
parser.add_argument('-s', '--sh_win', default=100,
                    type=int, help='Width of window (default - 100)')
parser.add_argument('-nr', '--nr_win', default=2,
                    type=int, help='Number of rows of windows (default - 2)')
parser.add_argument('-nw', '--nw_win', default=3, type=int,
                    help='Number of windows in one row (default - 3)')
args = parser.parse_args()


def build_castle(hight_castle, hight_thin, hight_wide, sh_win, nr_win, nw_win):
    # Строим основную форму дома
    # ободочек для красоты
    a = hight_castle - 50
    b = hight_castle - 30
    outer0 = color(Red)(cube([1015, 620, b], center=False))
    inner0 = color(Red)(cube([1315, 700, a], center=False))
    ring = translate((-10, -10, 0))(outer0) - translate((-20, -20, 0))(inner0)
    # зубцы сверху
    sh1 = up(hight_castle)(cube([1000, 600, 50], center=False))
    sh2 = color(Red)(translate((50, 50, hight_castle - 10))(
        cube([900, 500, 80], center=False)))
    main = cube([30, 1200, hight_castle + 50], center=False)
    # выше мы задали параллелепипед, теперь вырежем из него зубцы
    dirka1 = 0
    i = 0
    while i < 10:
        i += 1
        m = right(100*i)(main)
        dirka1 += m
    dirka2 = 0
    i = 0
    while i < 6:
        i += 1
        m = translate((1000, 100*i, 0))((rotate(90, [0, 0, 1])(main)))
        dirka2 += m
    teeth = sh1 - sh2 - back(50)(dirka1) - right(50)(dirka2)

    # окошки на основном здании
    # задали форму окна
    main = cube([sh_win, 50, 120], center=False)
    top = rotate(90, [1, 0, 0])(cylinder(r=sh_win/2, h=50))
    full = color(Birch)(main + translate((sh_win/2, 50, 120))(top))
    chislo1 = (hight_castle - 100)/(nr_win + 1)
    # на сколько поднимаем каждый уровень окон
    chislo2 = 800/nw_win
    # на сколько двигаем влево каждое окно в ряду
    # располазаем окна в рядах
    win = 0
    for i in range(0, nr_win):
        row = 0
        for q in range(0, nw_win):
            row += right(chislo2*q)(full)
        win += translate((50, -100, chislo1*i))(row)
    basi = color(Oak)(cube([1000, 600, hight_castle],
                      center=False)) + ring + color(Red)(teeth)
    basis = basi - translate((100, 90, 175))(win) - translate((
        100, 670, 175))(win)
    # Строим универсальную башню (всего их 3, их параметры не меняются)
    tower = cylinder(r=120, h=900, center=False)
    # ободочек для красоты
    outer1 = cylinder(r=130, h=b)
    inner1 = cylinder(r=150, h=a)
    poloska1 = outer1 - inner1
    # зубцы на верху башни
    high_ring = up(900)(cylinder(r=160, h=30))
    relief = color(Red)(up(930)(cylinder(r=160, h=50)))
    # выше мы задали параллелепипед, теперь заданим то, что будем вырезать
    block1 = color(Red)(translate((-200, -25, 900))(
        (cube([500, 50, 100], center=False))
        ))
    s = color(Red)(up(900)(cylinder(r=110, h=90)))
    block2 = back(25)(rotate(90, [0, 0, 1])(block1))
    block3 = back(25)(rotate(50, [0, 0, 1])(block1))
    block4 = back(25)(rotate(130, [0, 0, 1])(block1))
    d = relief - s - block1 - block2 - block3 - block4
    # окошки
    main = cube([30, 50, 120], center=False)
    top = rotate(90, [1, 0, 0])(cylinder(r=15, h=50))
    full1 = color(Birch)(main + translate((15, 50, 120))(top))
    boy = translate((-60, -120, 300))(full1) + translate((
        -60, 100, 300))(full1)
    simple_tower = color(Pine)(tower) + color(Red)(poloska1) + color(
        Red)(high_ring) + d - (boy + up(300)(boy))
# Строим худую башню
    tower_thi = color(Pine)(translate((900, 500, 0))(
        cylinder(r=110, h=hight_thin, center=False)))
    # добавляем зубцы
    tower_thin = tower_thi + color(Red)(translate((
        900, 500, hight_thin - 900))(high_ring + d))
#  Строим толстую башню
    tower_wid = color(Pine)(translate((1100, 650, 0))(
        cylinder(r=150, h=hight_wide, center=False)))
    # добавляем зубцы
    tower_wide = tower_wid + color(Red)(
        translate((1100, 650, hight_wide - 900))(high_ring + d))
    # Красота
    flig = cylinder(r=5, h=1200) + up(1200)(cube([100, 5, 60], center=False)) +
    translate((10, 0, 1225))(color(Green)(rotate(90, [1, 0, 0])(text(
        "The Cat's Empire", font="Liberation Sans:style=Bold Italic"))))
# Ура, наш замок готов!
    castle = union()(basis, simple_tower, right(1000)(
        simple_tower), forward(600)(simple_tower),
                     tower_thin,  tower_wide, flig)

    return castle

if __name__ == '__main__':
    out_dir = sys.argv[1] if len(sys.argv) > 1 else None

    a = build_castle(args.hight_castle, args.hight_thin,
                     args.hight_wide, args.sh_win, args.nr_win, args.nw_win)

    file_out = scad_render_to_file(a, out_dir=out_dir)
    print(f" SCAD file written to: \n{file_out}")
