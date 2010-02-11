import gtk
import math
#import cairo  # Boh, funziona anche senza import!!!

#def getPuntiEsagono(centro, raggio):
#	angolo = 0
#	punti = []
#	for i in range(6):
#		x = centro[0] + (raggio * math.cos(angolo))
#		y = centro[0] + (raggio * math.sin(angolo))
#		punti.append((x, y))
#		angolo += 2 * math.pi / 6
#	return punti

def getPuntiEsagono(centro, raggio):
	angolo = 0
	punti = []
	for i in range(6):
		x = centro[0] + (raggio * math.cos(angolo))
		y = centro[1] + (raggio * math.sin(angolo))
		punti.append((x, y))
		angolo += 2 * math.pi / 6
	return punti

def draw_polygon(cr, Points,colore):
	cr.set_line_width(0.01)
	cr.set_source_rgb(colore[0]/6, colore[1]/1.5, colore[2]/1.5)

	cr.move_to(Points[0][0], Points[0][1])
	for i in range(1, len(Points)):
		cr.line_to(Points[i][0], Points[i][1])
	cr.close_path()
	cr.stroke_preserve()

	cr.set_source_rgb(colore[0], colore[1], colore[2])
	cr.fill()



def esagono(texture, centro, raggio,colore):
	cr = texture.cairo_create()
	cr.scale(300, 300)#texture.get_width(), texture.get_height())
	punti = getPuntiEsagono(centro, raggio)
	draw_polygon(cr, punti,colore)


class HarmonicTablePanel(gtk.DrawingArea):

	def __init__(self):
		super(HarmonicTablePanel, self).__init__()
		self.connect("expose_event", self.expose)


	def expose(self, widget, event):
		context = widget.window.cairo_create()

		# set a clip region for the expose event
		context.rectangle(event.area.x, event.area.y,
		                  event.area.width, event.area.height)
		context.clip()

		self.draw(context)

		return False


	def redraw_canvas(self):
		if self.window:
			alloc = self.get_allocation()
			rect = gdk.Rectangle(alloc.x, alloc.y, alloc.width, alloc.height)
			self.window.invalidate_rect(rect, True)
			self.window.process_updates(True)


	def draw(self, context):
		# White Background
		alloc = self.get_allocation()
		self.window.draw_rectangle(self.get_style().white_gc,
		                           True, 0, 0, alloc.width, alloc.height)
		radius=0.08
		colore=(0.66, 0.86, 0.89)
		offset=0.1
		for i in range(-8,8):
			for j in range(20):
				#trasformo in un sistema di riferimento esagonale (con gli assi non ortogonali ma a pi/3)
				x=(i*2/math.sqrt(3)+j*1/math.sqrt(3))*radius*3
				y=j*radius
				if (0<x<2) and (0<y<1.3):
					esagono(self.window, (x,y), radius, colore)
			
