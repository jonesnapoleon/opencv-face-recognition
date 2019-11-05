import os
import wx
 
from PIL import Image
from wx.lib.pubsub import pub 
 
PhotoMaxSize = 300

class DropTarget(wx.FileDropTarget):
 
    def __init__(self, widget):
        wx.FileDropTarget.__init__(self)
        self.widget = widget
 
    def OnDropFiles(self, x, y, filenames):
        image = Image.open(filenames[0])
        image.thumbnail((PhotoMaxSize, PhotoMaxSize))
        image.save('thumbnail.png')
        pub.sendMessage('dnd', filepath='thumbnail.png')
        return True
 
 
class PhotoCtrl(wx.App):
    def __init__(self, redirect=False, filename=None):
        wx.App.__init__(self, redirect, filename)
        self.frame = wx.Frame(None, title='Feature extractor image', style=wx.DEFAULT_FRAME_STYLE, size=(800, 1000))
        self.panel = wx.Panel(self.frame)
        pub.subscribe(self.update_image_on_dnd, 'dnd')
        self.createWidgets()
        self.frame.Show()
 
    def createWidgets(self):
        instructions = 'Drag and Drop an image of your choice.'
        img = wx.Image(PhotoMaxSize, PhotoMaxSize)
        self.imageCtrl = wx.StaticBitmap(self.panel, wx.ID_ANY, 
                                         wx.Bitmap(img))
        filedroptarget = DropTarget(self)
        self.imageCtrl.SetDropTarget(filedroptarget)
#  
        instructLbl = wx.StaticText(self.panel, label=instructions)
        instructagain = wx.StaticText(self.panel, label='Select an image before clicking these buttons')
        instructagain1 = wx.StaticText(self.panel, label='These buttons will automatically show you five similar results.')
        cosinusBtn = wx.Button(self.panel, label='Cosinus')
        cosinusBtn.Bind(wx.EVT_BUTTON, self.on_cosinus)
        euclideanBtn = wx.Button(self.panel, label='Euclidean')
        euclideanBtn.Bind(wx.EVT_BUTTON, self.on_euclidean)
 
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
 
        self.mainSizer.Add(instructLbl, 0, wx.ALL, 10)
        self.mainSizer.Add(self.imageCtrl, 0, wx.ALL, 10)
        self.mainSizer.Add(instructagain, 0, wx.ALL, 5)
        self.mainSizer.Add(instructagain1, 0, wx.ALL, 5)
        self.mainSizer.Add(wx.StaticLine(self.panel, wx.ID_ANY), 0, wx.ALL|wx.EXPAND, 0)
        self.sizer.Add(euclideanBtn, 0, wx.ALL, 5)
        self.sizer.Add(cosinusBtn, 0, wx.ALL, 5)
        self.mainSizer.Add(self.sizer, 0, wx.ALL, 5)

        self.panel.SetSizer(self.mainSizer)
        self.mainSizer.Fit(self.frame)
        self.panel.Layout()
 
    def on_euclidean(self, event):
        self.panel.SetBackgroundColour('Red')
        img = wx.Image(PhotoMaxSize* 3/4, PhotoMaxSize * 3/4)
 
        # self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        # self.sizer = wx.BoxSizer(wx.HORIZONTAL)

        images = [0, 0, 0, 0, 0]
        for i in range(5):
            images[i] = wx.StaticBitmap(self.panel, 0, wx.Bitmap(img), (i * 225, 400))

        self.mainSizer.Add(wx.StaticLine(self.panel, wx.ID_ANY), 0, wx.ALL|wx.EXPAND, 0)

        for i in range(5):
            self.sizer.Add(images[i], 0, wx.EXPAND, 5)

        self.mainSizer.Add(self.sizer, 0, wx.ALL, 5)

        self.panel.SetSizer(self.mainSizer)
        self.mainSizer.Fit(self.frame)
        self.panel.Layout()
        self.panel.Refresh()

    def on_cosinus(self, event):
        self.panel.SetBackgroundColour('Green')
        img = wx.Image(PhotoMaxSize* 3/4, PhotoMaxSize * 3/4)

        images = [0, 0, 0, 0, 0]
        for i in range(5):
            images[i] = wx.StaticBitmap(self.panel, 0, wx.Bitmap(img), (i * 225, 400))
            
        self.mainSizer.Add(wx.StaticLine(self.panel, wx.ID_ANY), 0, wx.EXPAND)

        for i in range(5):
            self.sizer.Add(images[i], 0, wx.EXPAND, 5)

        self.mainSizer.Add(self.sizer)
        self.panel.SetSizer(self.mainSizer)
        self.mainSizer.Fit(self.frame)
        self.panel.Layout()
        self.panel.Refresh()
 
    def update_image_on_dnd(self, filepath):
        self.on_view(filepath=filepath)
 
    def on_view(self, filepath=None):
        # if not filepath:
        #     filepath = self.photoTxt.GetValue()
 
        img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)
        # scale the image, preserving the aspect ratio
        W = img.GetWidth()
        H = img.GetHeight()
        if W > H:
            NewW = PhotoMaxSize
            NewH = PhotoMaxSize * H / W
        else:
            NewH = PhotoMaxSize
            NewW = PhotoMaxSize * W / H
        img = img.Scale(NewW,NewH)
 
        self.imageCtrl.SetBitmap(wx.Bitmap(img))
        self.panel.Refresh()
 
if __name__ == '__main__':
    app = PhotoCtrl()
    app.MainLoop()