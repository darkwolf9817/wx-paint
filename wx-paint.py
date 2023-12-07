import wx
import PIL.ImageDraw as ImageDraw
from PIL import Image

class PaintFrame(wx.Frame):
    def __init__(self, parent, title):
        super(PaintFrame, self).__init__(parent, title=title)
        
        self.image = Image.new("RGB", (800, 600), (255, 255, 255))
        self.draw = ImageDraw.Draw(self.image)
        
        self.pen_color = (0, 0, 0)
        self.pen_size = 1
        
        # Create the main panel
        self.panel = wx.Panel(self)
        
        # Bind the events
        self.panel.Bind(wx.EVT_PAINT, self.on_paint)
        self.panel.Bind(wx.EVT_LEFT_DOWN, self.on_mouse_down)
        self.panel.Bind(wx.EVT_LEFT_UP, self.on_mouse_up)
        self.panel.Bind(wx.EVT_MOTION, self.on_mouse_move)
        
        # This creates the menu bar
        menubar = wx.MenuBar()
        file_menu = wx.Menu()
        file_menu.Append(wx.ID_SAVE, "&Save/tCtrl+S")
        file_menu.Bind(wx.EVT_MENU, self.on_save)
        menubar.Append(file_menu, "&File")
        
        # Create a toolbar
        toolbar = wx.ToolBar(self)
        color_button = wx.Button(toolbar, label="Color")
        color_button.Bind(wx.EVT_BUTTON, self.on_color_button)
        size_combo = wx.ComboBox(toolbar, choices=["1", "2", "3", "4", "5"])
        size_combo.Bind(wx.EVT_COMBOBOX, self.on_size_combo)
        toolbar.AddControl(color_button)
        toolbar.AddCOntrol(size_combo)
        toolbar.Realize()
        
        # Set the sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(toolbar, 0, wx.EXPAND)
        sizer.Add(self.panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        
        # Set size and show the frame
        self.SetSize(800, 600)
        self.Show()
        
    # Setting functions for the class
    def on_paint(self, event):
        dc = wx.PaintDC(self.panel)
        bmp = wx.BitMap.FramBuffer(self.image.size, self.image.tobytes())
        dc.DrawBitMap(bmp, 0, 0)
        
    def on_mouse_down(self, event):
        self.is_drawing = True
    
    def on_mouse_up(self, event):
        self.is_drawing = False
        
    def on_mouse_move(self, event):
        if self.is_drawing:
            x, y = event.GetPosition()
            self.draw.ellipse((x - self.pen_size // 2, y - self.pen_size // 2, x + self.pen_size // 2, y + self.pen_size // 2), fill=self.pen_color)
            self.panel.Refresh()
            
    def on_color_button(self, event):
        color_dialog = wx.ColourDialog(self)
        if color_dialog.ShowModal() == wx.ID_OK:
            self.pen_color = color_dialog.GetColourData().GetColour()
            
    def on_size_combo(self, event):
        self.pen_size = int(event.GetSelection())
        
    def on_save(self, event):
        dialog = wx.FileDialog(self, "Save Image", "", "", "*.jpg", wx.FD.SAVE)
        if dialog.ShowModal() == wx.ID_OK:
            self.image.save(dialog.GetPath(), "JPEG")

if __name__ == "__main__":
    app = wx.App()
    frame = PaintFrame(None, "Paint Clone")
    app.MainLoop()