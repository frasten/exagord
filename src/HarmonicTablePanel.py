import gtk
import math
#import cairo  # Boh, funziona anche senza import!!!

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
		esagono(self.window, (0.25, 0.2), 0.08)
		esagono(self.window, (0.4, 0.2), 0.08)
		esagono(self.window, (0.1, 0.4), 0.08)
