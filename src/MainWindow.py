import pygtk
pygtk.require('2.0')
import gtk


class MainWindow:
	width, height = 800, 600

	def delete_event(self, widget, event, data=None):
		print "delete event occurred"
		return False

	def __init__(self):
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.connect("destroy", self.destroy)
		self.window.set_default_size(self.width, self.height)
		self.window.set_title("Exagord")
		
		# Sets the border width of the window.
		self.window.set_border_width(10)

		self.window.move((gtk.gdk.screen_width() - self.width) / 2,
		  (gtk.gdk.screen_height() - self.height) / 2)

		# Main Container
		self.mainbox = gtk.HBox()
		button = gtk.Button("PanelL")
		self.mainbox.pack_start(button, False, False, 0)
		button2 = gtk.Button("HarmonicTable")
		self.mainbox.pack_start(button2, True, False, 0)
		button3 = gtk.Button("PanelR")
		self.mainbox.pack_start(button3, False, False, 0)


		self.window.add(self.mainbox)
		self.mainbox.show_all()

		# show the main window
		self.window.show()





	def destroy(self, widget, data=None):
		print "destroy signal occurred"
		gtk.main_quit()

	def main(self):
		# All PyGTK applications must have a gtk.main(). Control ends here
		# and waits for an event to occur (like a key press or mouse event).
		gtk.main()
