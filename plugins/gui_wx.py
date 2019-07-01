import sys
import argparse
import wx
from plugins.ui_base import UIBase

class LogOut(object):
    
    def __init__(self, btn_text, std, err):
        self.btn_text = btn_text
        self.std = std
        self.err = err

class GUI(wx.Frame):
    
    def __init__(self, config, args):

        self._config = config
        self._args = args
        
        self.log_out_index = 0
        self.log_out = []

        super(GUI, self).__init__(None, title=self._config.get_app())
        
        pnl = wx.Panel(self)
        
        sz_frame = wx.BoxSizer(wx.VERTICAL)
        
        sz_top = wx.BoxSizer(wx.VERTICAL)
                
        for key, value in args.items():
            cb = wx.CheckBox(pnl, label=str(key))
            cb.SetValue(value)
            sz_top.Add(cb, 0, wx.ALL , 5)
            self.Bind(wx.EVT_CHECKBOX,self.OnChecked)             
        
        self.txt_log = wx.TextCtrl(pnl, size = (560,400), style = wx.TE_MULTILINE | wx.TE_READONLY )
        sz_top.Add(self.txt_log, 1, wx.ALL , 5)

        # log_out list holds parameters for 
        #    (re)setting sys.stdout and sys.stderr to standard
        #    redirecting sys.stdout and sys.stderr to text control txt_log
        # and the appropriate text for the toggle botton
        # these paramters are holt by instances of LogOut class, implemented for this particular purpose
        self.log_out.append(
            LogOut(
                'log to window',
                sys.__stdout__,
                sys.__stderr__,
                )
            )
        self.log_out.append(
            LogOut(
                'log to console',
                TextRedirector(self.txt_log, "stdout"),
                TextRedirector(self.txt_log, "stderr"),
                )
            )

        sz_frame.Add(sz_top, 1, wx.ALL , 5)

        sz_botton = wx.BoxSizer(wx.HORIZONTAL)
        
        self.btn_log_out = wx.ToggleButton(pnl , -1, self.log_out[self.log_out_index].btn_text)
        sz_botton.Add(self.btn_log_out, 0, wx.ALL , 5)
        self.btn_log_out.Bind(wx.EVT_TOGGLEBUTTON,self.OnToggle)
        self.OnToggle(None)             # initialzes log output to txt_log
        
        btn_print = wx.Button(pnl , -1, 'print')
        sz_botton.Add(btn_print, 0, wx.ALL , 5)
        btn_print.Bind(wx.EVT_BUTTON,self.OnPrint)

        btn_start = wx.Button(pnl , -1, 'start')
        sz_botton.Add(btn_start, 0, wx.ALL , 5)
        btn_start.Bind(wx.EVT_BUTTON,self.OnExit)
        
        sz_frame.Add(sz_botton, 0, wx.ALIGN_RIGHT | wx.ALL , 5)
         
        pnl.SetSizer(sz_frame)
        sz_frame.Fit(self)
        
        self.Show(True)
    
    def OnToggle(self, event):          # without reference to event, the function can be called without actual event context
        
        self.log_out_index ^= 1         # toggles index between 0 and 1
#         event.GetEventObject().SetLabel(self.log_out[self.log_out_index].btn_text)
        self.btn_log_out.SetLabel(self.log_out[self.log_out_index].btn_text)
        sys.stdout = self.log_out[self.log_out_index].std
        sys.stderr = self.log_out[self.log_out_index].err
            
    def OnChecked(self, event): 
        cb = event.GetEventObject()
        self._args[cb.GetLabel()] = cb.GetValue()
        print(cb.GetLabel() + ' changed to ' + str(cb.GetValue()))

    def OnAbout(self, event):
        # A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.
        dlg = wx.MessageDialog( self, "Graphical user interface of "  + self._config.get_app(), "About " + self._config.get_app(), wx.OK)
        dlg.ShowModal()
        dlg.Destroy()
        
    def OnPrint(self, event):
        s = ''
        for i, (key, value) in enumerate(self._args.items()):
            if i > 0: s = s + ', '
            s = s + key + ': ' + str(value)
        print(s)
        
    def OnExit(self,event):
        self.Close(True)                # Close the frame.
        
    def get_args(self):
        return self._args

class TextRedirector(object):

    def __init__(self, cntrl, tag="stdout"):
        self.out = cntrl
        self.tag = tag

    def write(self, s):
        # TODO: implement different output/text tagging  for stdout and stderr
        self.out.WriteText(s)

class UI(UIBase):
    
    def execute(self):
        
        parser = argparse.ArgumentParser()
        parser.add_argument('-e', '--e_option', help='considers option e', action='store_true')
        parser.add_argument('-f', '--f_option', help='considers option f', action='store_true')
        args = vars(parser.parse_args())            # converts argparse.Namespace object to dictionary
        
        app = wx.App(False)
        gui = GUI(self.get_config(), args)
        app.MainLoop()
        
        return argparse.Namespace(**gui.get_args())  # converts dictionary to argparse.Namespace 
