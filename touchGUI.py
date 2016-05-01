# touchGUI.py - A Lightweight OOP Touchscreen GUI System (based on pygame)
# (c) 2016 Chris Burri @ NISTON Engineering Works for Axians Micatel AG
# MIT License applies (http://opensource.org/licenses/MIT)

# Would you like to know more? Visit http://niston.wordpress.com 

# Imports
import os
import pygame
import textrect
import threading
import time
import traceback
import functools

# GUI element base class
class GUIElement:

        def __init__(self, elementName, posX, posY, sizeX, sizeY):
                self.Name = elementName
                self.PosX = posX
                self.PosY = posY
                self.SizeX = sizeX
                self.SizeY = sizeY
                self.Surface = None
		self.Visible = True

        def RenderingSurfaceSet(self, renderingSurface):
                self.Surface = renderingSurface

# Clickable GUI element base class, derives from GUIElement
class GUIClickableElement(GUIElement):

	# constructor
	def __init__(self, elementName, posX, posY, sizeX, sizeY, onClick):
		GUIElement.__init__(self, elementName, posX, posY, sizeX, sizeY)
		self.OnClick = onClick
		self.Clicked = False
		self.Enabled = True

	# (internal use) click method, invokes OnClick handler if element is enabled
	def click(self):
		if self.Enabled == True:
			if self.OnClick != None:
				self.OnClick()


# GUI button class, derives from GUIClickableElement class
class GUIButton(GUIClickableElement):

        # button default colors
        COLORBRDR_INACTIVE = ((0, 255, 0))
        COLORBRDR_ACTIVE = ((0, 255, 0))
        COLORBRDR_CLICK = ((255, 255, 255))
        COLORBODY_INACTIVE = ((0, 0, 0))
        COLORBODY_ACTIVE = ((0, 255, 0))
        COLORBODY_CLICK = ((255, 255, 255))
        COLORTEXT_INACTIVE = ((0, 255, 0))
        COLORTEXT_ACTIVE = ((0, 0, 0))
        COLORTEXT_CLICK = ((0, 0, 0))
	COLORBRDR_DISABLED = ((32, 32, 32))
	COLORBODY_DISABLED = ((0, 0, 0))
	COLORTEXT_DISABLED = ((32, 32, 32))
	COLOR_BKGRND = ((0, 0, 0))

	# font path file
        FONT_REGULAR_PATH = "/usr/share/fonts/truetype/freefont/FreeSans.ttf"

	# default font size
        FONT_REGULAR_SIZE = 30

        # constructor, returns created object
        def __init__(self, elementName, posX, posY, sizeX, sizeY, buttonText, onClick):
		GUIClickableElement.__init__(self, elementName, posX, posY, sizeX, sizeY, onClick)
                self.Text = buttonText
		self.Active = False
                self.Clicked = False
                self.ColorBorderInactive = self.COLORBRDR_INACTIVE
                self.ColorBorderActive = self.COLORBRDR_ACTIVE
                self.ColorBorderClick = self.COLORBRDR_CLICK
		self.ColorBorderDisabled = self.COLORBRDR_DISABLED
                self.ColorBodyInactive = self.COLORBODY_INACTIVE
                self.ColorBodyActive = self.COLORBODY_ACTIVE
                self.ColorBodyClick = self.COLORBODY_CLICK
		self.ColorBodyDisabled = self.COLORBODY_DISABLED
                self.ColorTextInactive = self.COLORTEXT_INACTIVE
                self.ColorTextActive = self.COLORTEXT_ACTIVE
                self.ColorTextClick = self.COLORTEXT_CLICK
		self.ColorTextDisabled = self.COLORTEXT_DISABLED
		self.ColorBackground = self.COLOR_BKGRND
                self.FontPath = self.FONT_REGULAR_PATH
                self.FontSize = self.FONT_REGULAR_SIZE


        # render method draws the button to the display
        def Render(self):

                # determine color scheme according to button status
		if self.Enabled == True:
			if self.Clicked == True:
                                self.bordercolor = self.ColorBorderClick
                                self.bodycolor = self.ColorBodyClick
                                self.textcolor = self.ColorTextClick
			else:
	                	if self.Active == True:
	                                self.bordercolor = self.ColorBorderActive
        	                        self.bodycolor = self.ColorBodyActive
                	                self.textcolor = self.ColorTextActive
				else:
	                        	self.bordercolor = self.ColorBorderInactive
	                        	self.bodycolor = self.ColorBodyInactive
	                        	self.textcolor = self.ColorTextInactive
		else:
			self.bordercolor = self.ColorBorderDisabled
			self.bodycolor = self.ColorBodyDisabled
			self.textcolor = self.ColorTextDisabled

                # draw button
		if self.Visible == True:
			# draw border and body if visible
	                pygame.draw.rect(self.Surface, self.bordercolor,(self.PosX, self.PosY, self.SizeX, self.SizeY))
        	        pygame.draw.rect(self.Surface, self.bodycolor,(self.PosX+1, self.PosY+1, self.SizeX-2, self.SizeY-2))
	                # draw button text
	                self.fontObject = pygame.font.Font(self.FontPath, self.FontSize)
	                if "\n" in self.Text:
	                        # multiline text, use word wrapped drawing method
	                        self.textrectangle = pygame.Rect((self.PosX + 1, self.PosY + 1, self.SizeX - 2, self.SizeY - 2))
				try:
		                        self.textSurface = textrect.render_textrect(self.Text, self.fontObject, self.textrectangle, self.textcolor, self.bodycolor, 1)
				except:
					raise
	                        self.Surface.blit(self.textSurface, self.textrectangle)
	                else:
	                        # single line text, use standard drawing method
	                        self.textSurface = self.fontObject.render(self.Text, True, self.textcolor)
	                        self.textrectangle = self.textSurface.get_rect()
	                        self.textrectangle.center = ((self.PosX + self.SizeX / 2), (self.PosY + self.SizeY / 2))
	                        self.Surface.blit(self.textSurface, self.textrectangle)
		else:
			# draw background color rectangle if invisible
			pygame.draw.rect(self.Surface, self.ColorBackground, (self.PosX, self.PosY, self.SizeX, self.SizeY))



	# flash Button on click and invoke OnClick handler
	def click(self):
		if self.Enabled == True:
			# render button as clicked
			self.Clicked = True
	                self.Render()
			# force screen update
	                pygame.display.update()
			# invoke OnClick handler if applicable
			if self.OnClick != None:
				self.OnClick()
			# setup button appearance reset timer
			threading.Timer(1, self.click_reset())
			# do pygame events
			pygame.event.pump()

	# reset Button appearance after click
	def click_reset(self):
		# hold
		time.sleep(0.1)
		# reset appearance and render
		self.Clicked = False
		self.Render()
		# force screen update
		pygame.display.update()
		# do pygame events
		pygame.event.pump()

# Text Box Element
class GUITextBox(GUIClickableElement):

        # textbox default colors
        COLORBRDR_NORMAL = ((0, 255, 0))
        COLORBRDR_CLICK = ((255, 255, 255))
	COLORBRDR_DISABLED = ((64, 64, 64))
        COLORTEXT_NORMAL = ((0, 255, 0))
        COLORTEXT_CLICK = ((0, 0, 0))
        COLORTEXT_DISABLED = ((32, 32, 32))
        COLOR_BKGRND = ((0, 0, 0))

        # font path file
        FONT_REGULAR_PATH = "/usr/share/fonts/truetype/freefont/FreeSans.ttf"

        # default font size
        FONT_REGULAR_SIZE = 30

	# text alignment constants
	TEXTALIGN_HORIZONTAL_LEFT = 0
	TEXTALIGN_HORIZONTAL_CENTER = 1
	TEXTALIGN_HORIZONTAL_RIGHT = 2


        # constructor, returns created object
        def __init__(self, elementName, posX, posY, sizeX, sizeY, textboxText, onClick):
                GUIClickableElement.__init__(self, elementName, posX, posY, sizeX, sizeY, onClick)
		self.Text = textboxText
		self.Clicked = False
		self.BorderVisible = False
		self.TextAlignHorizontal = self.TEXTALIGN_HORIZONTAL_CENTER
                self.ColorBorderNormal = self.COLORBRDR_NORMAL
                self.ColorBorderClick = self.COLORBRDR_CLICK
                self.ColorBorderDisabled = self.COLORBRDR_DISABLED
                self.ColorTextNormal = self.COLORTEXT_NORMAL
                self.ColorTextClick = self.COLORTEXT_CLICK
                self.ColorTextDisabled = self.COLORTEXT_DISABLED
                self.ColorBackground = self.COLOR_BKGRND
                self.FontPath = self.FONT_REGULAR_PATH
                self.FontSize = self.FONT_REGULAR_SIZE


        # render method draws the text box to the display
        def Render(self):

                # determine color scheme according to textbox status
                if self.Enabled == True:
                        if self.Clicked == True:
                                self.bordercolor = self.ColorBorderClick
                                self.textcolor = self.ColorTextClick
                        else:
				self.bordercolor = self.ColorBorderNormal
				self.textcolor = self.ColorTextNormal
                else:
                        self.bordercolor = self.ColorBorderDisabled
                        self.textcolor = self.ColorTextDisabled

                # draw textbox if visible
                if self.Visible == True:
			# textbox border set to visible?
			if self.BorderVisible == True:
	                        # yes, draw border and background
	                        pygame.draw.rect(self.Surface, self.bordercolor,(self.PosX, self.PosY, self.SizeX, self.SizeY))
	                        pygame.draw.rect(self.Surface, self.ColorBackground,(self.PosX+1, self.PosY+1, self.SizeX-2, self.SizeY-2))
			else:
				# no, draw only background
				pygame.draw.rect(self.Surface, self.ColorBackground,(self.PosX, self.PosY, self.SizeX, self.SizeY))
                        # draw button text
                        self.fontObject = pygame.font.Font(self.FontPath, self.FontSize)
                        # multiline text, use word wrapped drawing method
                        self.textrectangle = pygame.Rect((self.PosX + 1, self.PosY + 1, self.SizeX - 2, self.SizeY - 2))
                        self.textSurface = textrect.render_textrect(self.Text, self.fontObject, self.textrectangle, self.textcolor, self.ColorBackground, self.TextAlignHorizontal)
                        self.Surface.blit(self.textSurface, self.textrectangle)
                else:
                        # draw background color rectangle if invisible
			# TODO: implement background buffering/redrawing
                        pygame.draw.rect(self.Surface, self.ColorBackground, (self.PosX, self.PosY, self.SizeX, self.SizeY))



class GUIRectangle(GUIElement):

	# Rectangle default colors
        COLORBRDR_NORMAL = ((0, 255, 0))
        COLORBRDR_DISABLED = ((32, 32, 32))
	COLOR_BACKGRND = ((0, 0, 0))


	def __init__(self, elementName, posX, posY, sizeX, sizeY):
		GUIElement.__init__(self, elementName, posX, posY, sizeX, sizeY)
		self.ColorBorder = self.COLORBRDR_NORMAL
		self.ColorBorderDisabled = self.COLORBRDR_DISABLED
		self.ColorBackground = self.COLOR_BACKGRND
		self.Enabled = True

	def Render(self):
		# determine color for rectangle
		if self.Visible == True:
			# visible, use foreground color
			if self.Enabled == True:
				self.rectcolor = self.ColorBorder
			else:
				self.rectcolor = self.ColorBorderDisabled
			# draw rectangle in foreground color
		else:
			# invisible, use background color
			self.rectcolor = self.BackgroundColor
		# draw rectangle
		pygame.draw.rect(self.Surface, self.rectcolor, ((self.PosX, self.PosY, self.PosX + self.SizeX, self.PosY + self.SizeY)), 1)


# GUI handling class
class GUI:

	# add a GUI page object to the GUI system
        def AddPage(self, guiPage):
		# give the new page a dummy surface
		guiPage.RenderingSurfaceSet(pygame.Surface((800, 480)))
                self.Pages.append(guiPage)
		guiPage.Initialize()
                return guiPage

	# clear the screen (fill surface with black)
        def ClearScreen(self):
                self.Surface.fill((0,0,0))

        def __init__(self):
                # GUI Pages list and active reference
                self.Pages = []
                self.CurrentPageIndex = None
		self.LockUpdate = False

                # initialize pygame
                os.putenv('SDL_FBDEV', '/dev/fb1')	# framebuffer device
                pygame.init()

                # hide mouse pointer (make it fully transparent, because the obvious set_visible(False) locks the mouse at center screen)
		pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))

                # setup display and obtain rendering surface
                self.Surface = pygame.display.set_mode((800, 480), pygame.FULLSCREEN | pygame.DOUBLEBUF)
                self.ClearScreen()

		# setup and start GUI thread
		self.GuiThread = threading.Thread(target=self.guiLoop, args=(self,))
		#self.GuiThread.daemon = True
		self.IsRunning = True		
		self.GuiThread.start()
		
	# render current page		
        def Render(self):
		# only if we have a current page
                if self.CurrentPageIndex != None:
                        try:
				# try rendering
				self.Pages[self.CurrentPageIndex].Render()
	                	#pygame.display.update()
			except Exception as e:
				# caught exception
                     		print ("Exception: " + str(e))
	                        print (traceback.format_exc())
           		        print ("Shutting down GUI...")
	                        self.IsRunning = False

	# Update the graphical display
	def Update(self):
		pygame.display.update()

	def DoEvents(self):
		pygame.event.pump()

	# Get GUIPage object by Name
        def PageByName(self, pageName):
                for page in self.Pages:
                        if page.Name == pageName:
                                return page

	# Get GUIPage index by Name
        def PageIndexByName(self, pageName):
                self.counter = 0;
                for page in self.Pages:
                        if page.Name == pageName:
                                return self.counter
                        else:
                                self.counter = self.counter + 1

	# Show spcified GUI Page (make active / bring to foreground)
        def Show(self, pageObject):
		try:
			# set current page inactive (if we have a current page)
	                if self.CurrentPageIndex != None:
				# flag as inactive
				self.Pages[self.CurrentPageIndex].IsActive = False
				# substitute display surface with dummy surface
				self.Pages[self.CurrentPageIndex].RenderingSurfaceSet(pygame.Surface((800, 640)))
	
			# clear the screen
			self.ClearScreen()

			# update current page index
	                self.CurrentPageIndex = self.PageIndexByName(pageObject.Name)

			# give the new current page the display surface
			self.Pages[self.CurrentPageIndex].RenderingSurfaceSet(self.Surface)

			# set new current page active
			self.Pages[self.CurrentPageIndex].IsActive = True

			# call OnShow on the new page
			self.Pages[self.CurrentPageIndex].OnShow()

			# render the page
	                self.Render()

		except Exception as e:
	                #exception occured on gui thread. print error and shut down.
            	        print ("Exception: " + str(e))
                        print (traceback.format_exc())
                        print ("Shutting down GUI...")
                        self.IsRunning = False


	# Request GUI shutdown (exit GUI Loop thread)
	def Shutdown(self):
		self.IsRunning = False

	# GUI Loop (GUI thread)
	def guiLoop(self, dummy):
		while self.IsRunning:
                   try:
			# put main loop to sleep (yield processing time)
			time.sleep(0.05)
			# invoke pygame event pump
			pygame.event.pump()
			# see if GUI has a GUIPage on display
			if self.CurrentPageIndex != None:
			  # process mouse events
			  for event in pygame.event.get():
			    # see if mouse was clicked
			    if(event.type is pygame.MOUSEBUTTONDOWN):
				# obtain mouse position on click
				self.clickpos = pygame.mouse.get_pos()
				# iterate through GUI elements on current page
	      		    	for element in self.Pages[self.CurrentPageIndex].Elements:
				  # see if current element is clickable (has click() method)
				  if hasattr(element, 'click'):
  				    # hit test on this particular element
	 			    if (self.clickpos[0] > (element.PosX + 3)) & (self.clickpos[0] < (element.PosX + element.SizeX - 3)):
			              if (self.clickpos[1] > (element.PosY + 2)) & (self.clickpos[1] < (element.PosY + element.SizeY - 2)):
				        # hit test succeeded, invoke click() method
					element.click()				
			    # see if key was pressed
			    if(event.type is pygame.KEYDOWN):
			      # yes, was it the F12 key?
			      if event.key == pygame.K_F12:
				# yes, save screenshot
				pygame.image.save(self.Surface, 'screenshot.tga')
		        # update gui
			if self.LockUpdate == False:
				pygame.display.update()
		   except Exception as e:
		     #exception occured on gui thread. print error and shut down.
		     print ("Exception: " + str(e))
		     print (traceback.format_exc())
		     print ("Shutting down GUI...")
		     self.IsRunning = False
		# gui thread exiting
		print ("GUI thread exiting...")

# GUI Page base class (inherit from this to create your own GUI pages)
class GUIPage:

	# constructor
        def __init__(self, pageName):
                self.Elements = []
                self.Name = pageName
                self.Surface = None
		self.IsActive = False

	# add GUI Element to Page
        def AddElement(self, guiElement):
                guiElement.RenderingSurfaceSet(self.Surface)
                self.Elements.append(guiElement)
                return guiElement

	# initialization is used to set up elements on the page
	def Initialize(self):
		# do nothing in base class
		pass

	# called when page is being shown
	def OnShow(self):
		# do nothing in base class
		pass

	# render all elements on the page
        def Render(self):
		for element in self.Elements:
			try:
				element.Render()
			except:
				raise
			
	# (internal use) set rendering surface
        def RenderingSurfaceSet(self, renderingSurface):
                self.Surface = renderingSurface
		for element in self.Elements:
			element.RenderingSurfaceSet(self.Surface)

	# get page GUI element by name
        def ElementByName(self, elementName):
                for element in self.Elements:
                        if element.Name == elementName:
                                return element





# Numpad Page, can be used to acquire numeric values
class NumPadPage(GUIPage):

	# constructor
	def __init__(self, pageName, title, unitLabel, maxLen, limitLow, limitHigh, onCancel, onAccept):
		GUIPage.__init__(self, pageName)
		self.OnAccept = onAccept		# accept (OK) handler
		self.OnCancel = onCancel		# cancel handler
		self.LimitHigh = limitHigh		# upper Limit
		self.LimitLow = limitLow		# lower Limit
		self.MaxLen = maxLen			# maximum length of input
		self.Text = title			# page title
		self.UnitLabel = unitLabel		# input unit label
		self.userInput = ''		

	# update display according to user input
	def updateUserInput(self):
		# draw filler chars (zeros)
                self.lblUserInput.Text = str('0')*(self.MaxLen-len(self.userInput)) + str(self.userInput)
                self.lblUserInput.Render()
		# do we have user input?
		if self.userInput != '':
			self.btnNum0.Enabled = True
			self.btnNum0.Render()
			self.btnClear.Enabled = True
			self.btnClear.Render()
			self.btnBackspace.Enabled = True
			self.btnBackspace.Render()
			if (int(self.userInput) > self.LimitHigh) or (int(self.userInput) < self.LimitLow) :
				self.btnEnter.Enabled = False
				self.btnEnter.Render()
				self.lblLimit.Visible = True
				self.lblLimit.Render()
			else:
				self.btnEnter.Enabled = True
				self.btnEnter.Render()
				self.lblLimit.Visible = False
				self.lblLimit.Render()	
		else:
			self.btnBackspace.Enabled = False
			self.btnBackspace.Render()
			self.btnClear.Enabled = False
			self.btnClear.Render()
			self.btnNum0.Enabled = False
			self.btnNum0.Render()
			self.btnEnter.Enabled = False
			self.btnEnter.Render()
			self.lblLimit.Visible = True
			self.lblLimit.Render()

	# helper function to append user input
        def UserInputAppend(self, value):
                if self.userInput == None:
                        self.userInput = value
                else:
                        self.userInput = self.userInput + str(value)

	# numeric button pressed
	def btnNum_Click(self, value):
		if (len(self.userInput) < self.MaxLen):
			if value == '0' and self.userInput == '':
				# do not add leading zeros
				pass
			else:
		                self.UserInputAppend(str(value))
				self.updateUserInput()

	# OK button pressed
	def btnEnter_Click(self):
		if self.OnAccept != None:
			self.OnAccept(int(self.userInput))
			self.userInput = ''
			self.updateUserInput()

	# Backspace button press
	def btnBackspace_Click(self):
		if (len(self.userInput) > 0):
			self.userInput = self.userInput[:-1]
			self.updateUserInput()

	# clear button press
	def btnClear_Click(self):
		self.userInput = ''
		self.updateUserInput()

	# cancel button press
	def btnCancel_Click(self):
		self.userInput = ''
		self.updateUserInput()
		if self.OnCancel != None:
			self.OnCancel()

	# page initialization
	def Initialize(self):
		# numeric display rectangle
		self.dispRect = self.AddElement(GUIRectangle('dispRect', 0, 0, 800, 120))
		# MHz label
		self.lblMHz = self.AddElement(GUITextBox('lblMHz', 600, 2, 125, 117, 'MHz', None)) 
		self.lblMHz.TextAlignHorizontal = GUITextBox.TEXTALIGN_HORIZONTAL_RIGHT
		self.lblMHz.FontSize = 60
		self.lblMHz.BorderVisible = False
		# User Input label
		self.lblUserInput = self.AddElement(GUITextBox('lblUserInput', 402, 2, 197, 117, str('0')*self.MaxLen, None))
		self.lblUserInput.TextAlignHorizontal = GUITextBox.TEXTALIGN_HORIZONTAL_RIGHT
		self.lblUserInput.FontSize = 60
		self.lblUserInput.BorderVisible = False
		# Limit warning label
		self.lblLimit = self.AddElement(GUITextBox('lblLimit', 25, 64, 187, 40, 'RANGE: ' + str(self.LimitLow) + '...' + str(self.LimitHigh), None))
		self.lblLimit.TextAlignHorizontal = GUITextBox.TEXTALIGN_HORIZONTAL_LEFT
		self.lblLimit.FontSize = 18
		self.lblLimit.ColorTextNormal = ((255, 0, 0))
		self.lblLimit.ColorBorderNormal = ((255, 0, 0))
		self.lblLimit.BorderVisible = False
		self.lblLimit.Visible = True
		# Text Label
		self.lblText = self.AddElement(GUITextBox('lblText', 25, 15, 382, 47, 'Numerical Input', None))
		self.lblText.TextAlignHorizontal = GUITextBox.TEXTALIGN_HORIZONTAL_LEFT
		self.lblText.BorderVisible = False
		self.lblText.FontSize = 24
		# numeric buttons
		self.btnNum7 = self.AddElement(GUIButton('btnNum7', 0, 120, 200, 90, '7', functools.partial(self.btnNum_Click, '7')))
		self.btnNum8 = self.AddElement(GUIButton('btnNum8', 200, 120, 200, 90, '8', functools.partial(self.btnNum_Click, '8')))
		self.btnNum9 = self.AddElement(GUIButton('btnNum9', 400, 120, 200, 90, '9', functools.partial(self.btnNum_Click, '9')))
		self.btnNum4 = self.AddElement(GUIButton('btnNum4', 0, 210, 200, 90, '4', functools.partial(self.btnNum_Click, '4')))
		self.btnNum5 = self.AddElement(GUIButton('btnNum5', 200, 210, 200, 90, '5', functools.partial(self.btnNum_Click, '5')))
		self.btnNum6 = self.AddElement(GUIButton('btnNum6', 400, 210, 200, 90, '6', functools.partial(self.btnNum_Click, '6')))
		self.btnNum1 = self.AddElement(GUIButton('btnNum1', 0, 300, 200, 90, '1', functools.partial(self.btnNum_Click, '1')))
                self.btnNum2 = self.AddElement(GUIButton('btnNum2', 200, 300, 200, 90, '2', functools.partial(self.btnNum_Click, '2')))
                self.btnNum3 = self.AddElement(GUIButton('btnNum3', 400, 300, 200, 90, '3', functools.partial(self.btnNum_Click, '3')))
		self.btnNum0 = self.AddElement(GUIButton('btnNum0', 200, 390, 200, 90, '0', functools.partial(self.btnNum_Click, '0')))
		self.btnNum0.Enabled = False
		# cancel button (dismiss)
		self.btnCancel = self.AddElement(GUIButton('btnCancel', 600, 120, 200, 90, 'Cancel', self.btnCancel_Click))
		self.btnCancel.ColorTextInactive = ((0, 0, 0))
		self.btnCancel.ColorBorderInactive = ((255, 0, 0))
		self.btnCancel.ColorBodyInactive = ((255, 0, 0))
		# clear button (clear all input)
		self.btnClear = self.AddElement(GUIButton('btnClear', 600, 300, 200, 90, 'Clear', self.btnClear_Click))
		self.btnClear.FontSize = 22
		self.btnClear.ColorTextInactive = ((255, 255, 0))
		self.btnClear.ColorBorderInactive = ((255, 255, 0))
		self.btnClear.Enabled = False
		# backspace (delete last number)
		self.btnBackspace = self.AddElement(GUIButton('btnBackspace', 600, 210, 200, 90, 'Backspace', self.btnBackspace_Click))
		self.btnBackspace.FontSize = 22
		self.btnBackspace.ColorTextInactive = ((255, 255, 0))
		self.btnBackspace.ColorBorderInactive = ((255, 255, 0))
		self.btnBackspace.Enabled = False
		# enter (accept input)
		self.btnEnter = self.AddElement(GUIButton('btnEnter', 600, 390, 200, 90, 'OK', self.btnEnter_Click))
		self.btnEnter.ColorTextInactive = ((0, 0, 0))
		self.btnEnter.ColorBorderInactive = ((0, 255, 0))
		self.btnEnter.ColorBodyInactive = ((0, 255, 0))
		self.btnEnter.Enabled = False

	# override render method to ensure the numpad text is correctly displayed
	def Render(self):
		# update textbox
		self.lblText.Text = self.Text
		# call to base class
		GUIPage.Render(self)
