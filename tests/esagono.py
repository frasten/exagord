#!/usr/bin/env python
# -*- coding: utf-8 -*-

import clutter
import math
from clutter import CairoTexture
import gobject
import cairo



def getPuntiEsagono(centro, raggio):
	angolo = 0
	punti = []
	for i in range(6):
		x = centro[0] + (raggio * math.cos(angolo))
		y = centro[0] + (raggio * math.sin(angolo))
		punti.append((x, y))
		angolo += 2 * math.pi / 6
	return punti

def draw_polygon(cr, Points):
	cr.set_line_width(0.01)
	cr.set_source_rgb(0.11, 0.72, 0.77)

	cr.move_to(Points[0][0], Points[0][1])
	for i in range(1, len(Points)):
		cr.line_to(Points[i][0], Points[i][1])
	cr.close_path()
	cr.stroke_preserve()
	
	cr.set_source_rgb(0.66, 0.86, 0.89)
	cr.fill()





def esagono(texture, centro, raggio):
	cr = texture.cairo_create()
	cr.scale(300, 300)#texture.get_width(), texture.get_height())
	punti = getPuntiEsagono(centro, raggio)
	draw_polygon(cr, punti)





if __name__ == '__main__':
    stage_color = clutter.Color(0xff, 0xff, 0xff, 0xff)
    
    stage = clutter.Stage()
    stage.connect('button-press-event', clutter.main_quit)
    stage.connect('destroy', clutter.main_quit)
    stage.set_color(stage_color)
    
    texture = CairoTexture(300, 300)
    texture.set_position(
        (stage.get_width() - 300) / 2,
        (stage.get_height() - 300) / 2
    )
    stage.add(texture)
    texture.show()


    esagono(texture, (0.4, 0.4), 0.2)







    stage.show()
    
    clutter.main()
