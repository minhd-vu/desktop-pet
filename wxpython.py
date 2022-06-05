#!/usr/bin/env python

import wx


class PetFrame(wx.Frame):
    def __init__(self, parent, log):
        self.log = log
        wx.Frame.__init__(
            self, parent, -1, "Shaped Window",
            style=wx.FRAME_SHAPED | wx.SIMPLE_BORDER | wx.FRAME_NO_TASKBAR | wx.STAY_ON_TOP
        )

        self.hasShape = False
        self.delta = (0, 0)

        self.Bind(wx.EVT_LEFT_DCLICK, self.OnDoubleClick)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMouseMove)
        self.Bind(wx.EVT_RIGHT_UP, self.OnExit)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

        # Load the image and ensure it has a Mask, (rather than an alpha channel)
        img = wx.Image("./images/idle.gif", wx.BITMAP_TYPE_ANY)
        if img.HasAlpha():
            img.ConvertAlphaToMask()

        # Convert it to a wx.Bitmap, which will be used in SetWindowShape, and
        # in OnPaint below.
        self.bmp = wx.Bitmap(img)

        w, h = self.bmp.GetWidth(), self.bmp.GetHeight()
        self.SetClientSize((w, h))

        self.SetToolTip(
            "Right-click to close the window\n"
            "Double-click the image to set/unset the window shape"
        )

        if wx.Platform == "__WXGTK__":
            # wxGTK requires that the window be created before you can
            # set its shape, so delay the call to SetWindowShape until
            # this event.
            self.Bind(wx.EVT_WINDOW_CREATE, self.SetWindowShape)
        else:
            # On wxMSW and wxMac the window has already been created, so go for it.
            self.SetWindowShape()

        dc = wx.ClientDC(self)
        dc.DrawBitmap(self.bmp, 0, 0, True)

    def SetWindowShape(self, *evt):
        # Use the bitmap's mask to create a wx.Region
        r = wx.Region(self.bmp)

        # NOTE: Starting in 4.1 you can also get a wx.Region directly from
        # a wx.Image, so you can save a step if you don't need it as a wx.Bitmap
        # for anything else.
        # r = self.img.ConvertToRegion()

        # Use the region to set the frame's shape
        self.hasShape = self.SetShape(r)

    def OnDoubleClick(self, evt):
        if self.hasShape:
            self.SetShape(wx.Region())
            self.hasShape = False
        else:
            self.SetWindowShape()

    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
        dc.DrawBitmap(self.bmp, 0, 0, True)

    def OnExit(self, evt):
        self.Close()

    def OnLeftDown(self, evt):
        self.CaptureMouse()
        x, y = self.ClientToScreen(evt.GetPosition())
        originx, originy = self.GetPosition()
        dx = x - originx
        dy = y - originy
        self.delta = ((dx, dy))

    def OnLeftUp(self, evt):
        if self.HasCapture():
            self.ReleaseMouse()

    def OnMouseMove(self, evt):
        if evt.Dragging() and evt.LeftIsDown():
            x, y = self.ClientToScreen(evt.GetPosition())
            fp = (x - self.delta[0], y - self.delta[1])
            self.Move(fp)


if __name__ == "__main__":
    # Create application object.
    app = wx.App()

    # Create the pet borderless and transparent frame.
    frame = PetFrame(None, -1)

    # Display the frame.
    frame.Show()

    # Start the event loop.
    app.MainLoop()
