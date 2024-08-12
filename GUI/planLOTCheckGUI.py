# This is the main GUI for the program PlanTomoLOTChecker

import wx 
import sys

sys.path.append("C:/AitangResearch/TomoLOTCheck/GUI")

sys.path.append("C:/AitangResearch/TomoLOTCheck")

from  clipBoardLib.clipboard_lib import ClipBoard

from configureFile.configFile import pdf_dir

 
class MainGUI(wx.Frame): 
   def __init__(self, parent, title): 
      
      super(MainGUI, self).__init__(parent, title = title,size=(800,450),style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
		
      panel = wx.Panel(self) 
      
      # boxer for main layout
      vbox = wx.BoxSizer(wx.VERTICAL) 
      
      # patient information box
      nm = wx.StaticBox(panel, -1, 'Patient Information',size=(70,200))
      
      nmSizer = wx.StaticBoxSizer(nm, wx.VERTICAL) 
       
      nmbox = wx.BoxSizer(wx.HORIZONTAL) # horizontal box holding the patient name, MRN
      
      fn = wx.StaticText(panel, -1, "First Name:") 
      ln = wx.StaticText(panel, -1, "Last Name:") 
      ln2=wx.StaticText(panel,-1,"MRN:")
      self.nm1 = wx.TextCtrl(panel, -1, style = wx.ALIGN_LEFT,size=(150,30)) # for first name
      self.nm2 = wx.TextCtrl(panel, -1, style = wx.ALIGN_LEFT,size=(150,30)) # for last name
      self.nm3=wx.TextCtrl(panel, -1, style = wx.ALIGN_LEFT,size=(150,30))   # for MRN
      
    		
      nmbox.Add(fn, 0, wx.ALL|wx.CENTER, 5) 
      nmbox.Add(self.nm1, 0, wx.ALL|wx.CENTER, 5)
      nmbox.Add(ln, 0, wx.ALL|wx.CENTER, 5) 
      nmbox.Add(self.nm2, 0, wx.ALL|wx.CENTER, 5) 
      nmbox.Add(ln2, 0, wx.ALL|wx.CENTER, 5)
      nmbox.Add(self.nm3, 0, wx.ALL|wx.CENTER, 5) 
      nmSizer.Add(nmbox, 0, wx.ALL|wx.CENTER, 10)  
      
      # mean leaf count box
      lc = wx.StaticBox(panel, -1, 'Mean Leaf counts',size=(70,200),style=wx.ALIGN_CENTER) 
      
      lcSizer=wx.StaticBoxSizer(lc, wx.VERTICAL) 
      
      lcBox=wx.BoxSizer(wx.HORIZONTAL)
      leafCountLabel=wx.StaticText(panel,-1,"Mean Leaf Count:")
      leafCountLabel2=wx.StaticText(panel,-1,"       ") # add the space.
      self.leafTextBox=wx.TextCtrl(panel, -1, style = wx.ALIGN_LEFT,size=(560,30))
      
      lcBox.Add(leafCountLabel)
      
      lcBox.Add(leafCountLabel2)
      lcBox.Add(self.leafTextBox)
      
      lcSizer.Add(lcBox)     
      
     # recommendation box
     
      rc = wx.StaticBox(panel, -1, 'Recommendations') 
          
      rcSizer=wx.StaticBoxSizer(rc, wx.VERTICAL) 
      
      
      self.rcTextBox=wx.TextCtrl(panel, -1, style = wx.ALIGN_LEFT|wx.TE_MULTILINE,size=(700,100))
      
           
      rcSizer.Add(self.rcTextBox)           
  
      
      
      # button box
		
      sbox = wx.StaticBox(panel, -1, 'Actions',size=(70,200)) 
      sboxSizer = wx.StaticBoxSizer(sbox, wx.VERTICAL) 
		
      hbox = wx.BoxSizer(wx.HORIZONTAL) 
      self.calButton = wx.Button(panel, -1, 'Calculate') 
		
      hbox.Add(self.calButton, 0, wx.ALL|wx.LEFT, 10) 
      
      self.saveButton = wx.Button(panel, -1, 'Save') 
		
      hbox.Add(self.saveButton, 0, wx.ALL|wx.LEFT, 10) 
      
      self.exitButton=wx.Button(panel,-1,'Exit')
      
      hbox.Add(self.exitButton,0, wx.ALL|wx.LEFT, 10)
      
      
      sboxSizer.Add(hbox, 0, wx.ALL|wx.LEFT, 10) 
      
      # main vbox
      vbox.Add(nmSizer,0, wx.ALL|wx.CENTER, 5) 
      vbox.Add(lcSizer,0, wx.ALL|wx.CENTER, 5) 
      vbox.Add(rcSizer,0, wx.ALL|wx.CENTER, 5) 
      
      
      
      vbox.Add(sboxSizer,0, wx.ALL|wx.CENTER, 5)
      
      self.statusBar=self.CreateStatusBar()
      
      
      
      panel.SetSizer(vbox) 
      self.Centre() 
         
      panel.Fit() 
      self.Show()  
      
      
      
      # add clipporad object
      
      self.clipBoardObj=ClipBoard()
      
      # bind all the evemnt
      
      self.Bind(wx.EVT_BUTTON,self.OnCalculate,self.calButton)
      
      self.Bind(wx.EVT_BUTTON,self.OnExit,self.exitButton)
      
      self.Bind(wx.EVT_BUTTON,self.OnSave,self.saveButton)
      
      
   def OnCalculate(self,event):
      '''
      Call back function for calculate button.
      
      '''
      
      # set the font size
      
      font1 = wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')
      
      # get mean leaf count
      
      meanLeafCount=self.clipBoardObj.get100msLeaves() 
      
      # set the leaf count box.
      
      self.leafTextBox.SetLabel(str(meanLeafCount))
      
      self.leafTextBox.SetFont(font1)
      
      if meanLeafCount>1.7: # set the color.
         
         self.leafTextBox.SetForegroundColour(wx.GREEN)
         
      if meanLeafCount<=1.7:
         
         self.leafTextBox.SetForegroundColour(wx.RED)
         
     
      # fill the recommendation box and set the color.
      
      font1 = wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')
      
      if meanLeafCount>1.7: # set the color.
               
               self.rcTextBox.SetForegroundColour(wx.GREEN)
               
               green_recomendation=" This Tomo plan satifies the requirements that the mean leaf accout is less than 1.7 for open time less 100ms"
               
               self.rcTextBox.SetLabel(green_recomendation)
               self.rcTextBox.SetFont(font1)
               
      if meanLeafCount<=1.7:
               
               red_recomendation=" Please adjust the pitch to make sure the mean leaf count is less than 1.7 for the open time less than 100ms."
                        
               self.rcTextBox.SetLabel(red_recomendation)               
               
               self.rcTextBox.SetForegroundColour(wx.RED) 
               
               self.rcTextBox.SetFont(font1)
   def OnSave(self,event):
      
      '''
      call back for save button.
            
      '''
      # to get patient details
      
      firstName=self.nm1.GetValue()
      lastName=self.nm2.GetValue()
      MRN=self.nm3.GetValue()
      
      patientName=firstName+','+lastName
      
      # to see if the RT type in patient infomation.
      
      if not (firstName and lastName and MRN):
         
         self.statusBar.SetStatusText("Please fill the patient infomation before save the report.")
         
              
             
      if  (firstName and lastName and MRN):
        
            pdf_file_name=self.clipBoardObj.writeToPDFFile(pdf_dir,MRN,patientName)
                
            self.statusBar.SetStatusText('PDF report was saved as: '+pdf_file_name)          

   def OnExit(self,event):
      
      '''
      callback to exit the system.
      
      '''
      
      self.Destroy()
      
if __name__=="__main__":
   
   app = wx.App() 
   MainGUI(None,  'Tomo Plan MLC LOT Checker') 
   app.MainLoop()
