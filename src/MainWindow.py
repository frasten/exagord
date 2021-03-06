import pygtk
pygtk.require('2.0')
import gtk

from HarmonicTablePanel import HarmonicTablePanel


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

		# Elements buttons
		buttonBox = gtk.VButtonBox()
		buttonBox.set_border_width(5)

		buttonBox.set_layout(gtk.BUTTONBOX_START)
		buttonBox.set_spacing(20)

		button1 = gtk.Button()
		# Queste n istruzioni serviranno quando mostreremo solo l'immaginetta
		button1.set_relief(gtk.RELIEF_NONE)  # Elimino il bordo di default
		button1.set_focus_on_click(False)
		button1.set_tooltip_text("First Element")
		icon = gtk.image_new_from_stock(gtk.STOCK_CLOSE, gtk.ICON_SIZE_MENU)
		button1.add(icon)  # Metto un'immagine al button
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

		# Split into two:
		centralSplitBox = gtk.VBox()


		# TopBar
		centralTopbar = gtk.HBox()
		centralTopbar.set_border_width(5)
		
		# **** TPM **** 
		# value, min, max, increment, pageIncrement, boh?
		tpmContainer = gtk.HBox()  # Container for TPM stuff
		tpmContainer.pack_start(gtk.Label("TPM:"), False, False, 0)
		tpmAdj = gtk.Adjustment(60, 1, 300, 1, 10, 0.0)
		tpm = gtk.SpinButton(tpmAdj, 0, 0)
		tpmContainer.pack_start(tpm, False, False, 5)
		centralTopbar.pack_start(tpmContainer, False, False, 10)

		# **** Octave ****
		octaveContainer = gtk.HBox()  # Container for Octave stuff
		octaveContainer.pack_start(gtk.Label("Octave:"), False, False, 3)
		octaveAdj = gtk.Adjustment(0, -8, 8, 1, 2, 0.0)
		octave = gtk.SpinButton(octaveAdj, 0, 0)
		octaveContainer.pack_start(octave, False, False, 5)
		centralTopbar.pack_start(octaveContainer, False, False, 10)

		# **** Midi Ch. ****
		midiChContainer = gtk.HBox()  # Container for MIDI Channel stuff
		midiChContainer.pack_start(gtk.Label("Midi Ch:"), False, False, 3)
		midiChAdj = gtk.Adjustment(1, 1, 16, 1, 2, 0.0)
		midiCh = gtk.SpinButton(midiChAdj, 0, 0)
		midiChContainer.pack_start(midiCh, False, False, 5)
		centralTopbar.pack_start(midiChContainer, False, False, 10)


		# Aggiungo la topbar al pannello centrale
		centralSplitBox.pack_start(centralTopbar, False, False, 0)

		# Harmonic Table
		self.htPanel = HarmonicTablePanel()
		centralSplitBox.pack_start(self.htPanel, True, True, 0)

		centralPanel.add(centralSplitBox)



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


if __name__ == '__main__':
	win = MainWindow()
	win.main()
