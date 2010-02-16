import gtk
import math
import string

def getHexagonVertices(center, radius):
	'''Returns a list of coordinates of the vertices of an hexagon, given
	the coordinates of the center and the radius.'''
	angle = 0
	vertices = []
	for i in range(6):
		x = center[0] + (radius * math.cos(angle))
		y = center[1] + (radius * math.sin(angle))
		vertices.append({'x': x, 'y': y})
		angle += math.pi / 3
	return vertices


def drawPolygon(cr, points, color):
	'''Draws a generic polygon'''
	# Darker outline
	cr.set_line_width(0.01)
	cr.set_source_rgb(color[0] - 0.26, color[1] - 0.26, color[2] - 0.26)

	cr.move_to(points[0]['x'], points[0]['y'])
	for i in range(1, len(points)):
		cr.line_to(points[i]['x'], points[i]['y'])
	cr.close_path()
	cr.stroke_preserve()

	# Background
	cr.set_source_rgb(color[0], color[1], color[2])
	cr.fill()


def drawHexagon(texture, center, radius, color, note, octave):
	cr = texture.cairo_create()
	cr.scale(300, 300)  # texture.get_width(), texture.get_height())
	vertices = getHexagonVertices(center, radius)
	drawPolygon(cr, vertices, color)

	# Write note name
	cr.set_source_rgb(0.1, 0.1, 0.1)
	cr.set_font_size(0.05)
	cr.move_to(center[0] - 0.02 * len(note), center[1] + 0.01)
	cr.show_text(note)

	# Write octave number
	cr.set_source_rgb(color[0] - 0.26, color[1] - 0.26, color[2] - 0.26)
	cr.set_font_size(0.04)
	cr.move_to(center[0] - 0.015, center[1] + 0.05)
	cr.show_text(str(octave))


class HarmonicTablePanel(gtk.DrawingArea):

	def __init__(self):
		super(HarmonicTablePanel, self).__init__()
		self.connect("expose_event", self.expose)


	def expose(self, widget, event):
		'''Called when the widget is ready'''
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
		
		# Creating color scheme dictionary
		colorSchemeArray = {}
		
		# Read color scheme CSV file
		f = open('./config/colorschemes.svn', 'r')
		for line in f:
			if not (line[0] == "#" or line == ""):
				nome, r1, g1, b1, r2, g2, b2, r3, g3, b3, r4, g4, b4, r5, g5, b5, r6, g6, b6, r7, g7, b7 = line.split(",")
				colorSchemeArray[nome] = ((string._float(r1), string._float(g1), string._float(b1)),
				(string._float(r2), string._float(g2), string._float(b2)),
				(string._float(r3), string._float(g3), string._float(b3)),
				(string._float(r4), string._float(g4), string._float(b4)),
				(string._float(r5), string._float(g5), string._float(b5)),
				(string._float(r6), string._float(g6), string._float(b6)),
				(string._float(r7), string._float(g7), string._float(b7)))
		
		# Array of colors for octave visualization
		# Try: 'rainbow', 'violetmono', 'orangemono'
		octaveColors = colorSchemeArray['violetmono']
		
		# Array of note name (NOTE: the index is the distance in semitones from C)
		noteArray = ("C","Db","D","Eb","E","F","Gb","G","Ab","A","Bb","B")
		# The C7 on top-left corner differs form C1 by 84 semitones
		startSemitone = 84

		# Hexagon parameters
		radius = 0.08  # hexagon radius
		apotema = radius * math.sqrt(3) / 2  # needed for drawing the harmonic table correctly
		dy = apotema  # step length in y direction
		dx = 3 * radius  # step length in x direction

		# Start to generate the harmonic table from top-left corner
		currentSemitone = startSemitone

		for i in range(19):  # 19 rows...
			if (i % 2 == 1):
			# for odd rows...
				cols = 9
				xOffset = apotema
			else:
			# ...and for even rows
				cols = 8
				xOffset = apotema + (dx / 2)

			for j in range(cols):  # the number of cols are 8 or 9
				# Calculate the hexagon center coordinates
				x = j * dx + xOffset
				y = i * dy

				# Calculate the current note using the distance in semitones from C1
				note = currentSemitone % 12

				# Calculate the note name
				noteName = noteArray[note]

				# Calculate the current octave of the note
				octave = (currentSemitone - note) / 12

				# print "nota: ", noteName, " ottava: ", octave, " i:", i, " j: ", j
				# Different colors to differentiate the various octaves
				color = octaveColors[octave - 1]

				# Drawing hexagon
				drawHexagon(self.window, (x + radius, y + radius), radius, color, noteName, octave)

				# Along columns, the hexagon differs by one semitone
				currentSemitone += 1
			'''
			Along rows, -12 semitones from the last note of previous row, to
			the first of the current row.
			NOTE: change the parameter "12" to create some freaky harmonic table :)
			'''
			currentSemitone -= 12
