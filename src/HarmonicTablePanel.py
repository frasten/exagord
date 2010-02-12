import gtk
import math
#import cairo  # Boh, funziona anche senza import!!!

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
	cr.set_source_rgb(colore[0] - 0.26, colore[1] - 0.26, colore[2] - 0.26)

	cr.move_to(Points[0][0], Points[0][1])
	for i in range(1, len(Points)):
		cr.line_to(Points[i][0], Points[i][1])
	cr.close_path()
	cr.stroke_preserve()

	cr.set_source_rgb(colore[0], colore[1], colore[2])
	cr.fill()

def esagono(texture, centro, raggio,colore,nota,ottava):
	cr = texture.cairo_create()
	cr.scale(300, 300)#texture.get_width(), texture.get_height())
	punti = getPuntiEsagono(centro, raggio)
	draw_polygon(cr, punti,colore)
	
	#Write note name
	cr.set_source_rgb(0.1, 0.1, 0.1)
	cr.set_font_size(0.05)
	cr.move_to(centro[0] - 0.02 * len(nota), centro[1] + 0.01)
	cr.show_text(nota)
	
	#Write octave number
	cr.set_source_rgb(colore[0] - 0.26, colore[1] - 0.26, colore[2] - 0.26)
	cr.set_font_size(0.04)
	cr.move_to(centro[0] - 0.015, centro[1] + 0.05)
	cr.show_text( int.__str__(ottava))

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
		
		#Array of different colors for octave visualization
		octaveColors = ((0.97, 0.67, 0.56), (0.99, 0.81, 0.62), (1, 0.96, 0.83), (0.85, 0.91, 0.71), (0.67, 0.86, 0.89),
		 (0.76, 0.8, 0.91), (0.78, 0.65, 0.81))
		 
		#Array of note name (NOTE: the index is the semitone distance to C)
		noteArray = ("C","Db","D","Eb","E","F","Gb","G","Ab","A","Bb","B")
		#The C7 on top-left corner differs form C1 by 84 semitones
		startSemitone = 84
		
		#Hexagon parameters
		radius = 0.08 							#hexagon radius
		apotema = (radius / 2) * math.sqrt(3)	#needed for drawing the harmonic table correctly
		dy = apotema							#step length in y direction
		dx = 4 * dy * math.sin(math.pi/3)		#step length in x direction
		
		#Start to generate the harmonic table from top-left corner
		currentSemitone = startSemitone
		
		for i in range(19):						#19 rows...
			if (math.fmod(i,2) == 1):
			#for odd rows...
				cols = 9
				offset = apotema
			else:
			#...and for even rows
				cols = 8
				offset = apotema + (dx / 2)
				
			for j in range(cols):				#the number of cols are 8 or 9
				#Calculate the hexagon center coordinates
				x = j * dx + offset
				y = i * dy
				
				#Calculate the current note using the distance in semitones from C1
				note = float.__int__(math.fmod(currentSemitone,12))
				
				#Calculate the note name
				noteName = noteArray[note]
				
				#Calculate the current octave of the note
				octave = (currentSemitone - note) / 12
				
				#print "nota: ", noteName, " ottava: ", octave, " i:", i, " j: ", j
				#Different colors to differentiate the various octaves
				colore=octaveColors[octave-1]
				
				#Drawing hexagon
				esagono(self.window, (x+radius, y+radius), radius, colore, noteName, octave)
				
				#Along columns, the hexagon differs by one semitone
				currentSemitone = currentSemitone + 1
			#Along rows, -12 semitones from the last note of previous row, to the first of the current row
			#NOTE: change the parameter "-12" to create some freaky harmonic table :)
			currentSemitone = currentSemitone - 12
