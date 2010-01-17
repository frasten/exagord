import pygtk
pygtk.require('2.0')
import gtk


class MainWindow:
	width, height = 900, 500

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

		# LEFT PANEL
		panelL = gtk.Frame("Left Panel")
		buttonBox = gtk.VButtonBox()
		buttonBox.set_border_width(5)

		buttonBox.set_layout(gtk.BUTTONBOX_START)
		buttonBox.set_spacing(20)

		button1 = gtk.Button(stock=gtk.STOCK_OK)
		buttonBox.add(button1)
		button2 = gtk.Button(stock=gtk.STOCK_OK)
		buttonBox.add(button2)
		button3 = gtk.Button(stock=gtk.STOCK_OK)
		buttonBox.add(button3)
		button4 = gtk.Button(stock=gtk.STOCK_OK)
		buttonBox.add(button4)
		buttonBox.set_size_request(150, -1)  # set the left panel width

		panelL.add(buttonBox)

		self.mainbox.pack_start(panelL, False, False, 0)


		# CENTRAL PANEL
		centralPanel = gtk.Frame("Central Panel")
		self.mainbox.pack_start(centralPanel, True, True, 0)


		# RIGHT PANEL
		panelR = gtk.Frame("Right Panel")
		self.mainbox.pack_start(panelR, False, False, 0)


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
