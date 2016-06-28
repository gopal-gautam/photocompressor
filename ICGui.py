from Tkinter import Tk, Frame, BOTH, Text, Button, Entry, X, DISABLED, NORMAL, END, PhotoImage
import tkFileDialog, Tkconstants


class Example(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent, background="white")   
         
        self.parent = parent

        w = 390
        h = 120
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
    
        x = (sw - w)/2
        y = (sh - h)/2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))

        self.initUI()
        
    
    def initUI(self):
      
        self.parent.title("BCIPN Image Compressor")
        self.pack(fill=BOTH, expand=1)
        

def main():
  
    root = Tk()
    img = PhotoImage(file='nsetlogo.png')
    root.tk.call('wm', 'iconphoto', root._w, img)    
    # root.geometry("650x450+200+100")
    app = Example(root)

    dirname_textbox = Entry(root, state=DISABLED)
    dirname_textbox.pack(fill=X, padx=5, pady=5)
    #dirname_textbox.configure(state='disabled')

    button_opt = {'fill': Tkconstants.BOTH, 'padx': 5, 'pady':5}
    # dirname = []
    dirname=['']
    def openDirectory():
        dirname1 = tkFileDialog.askdirectory(parent=root, title="Select a directory to proceed")
        dirname[0] = dirname1
        dirname_textbox.configure(state='normal')
        dirname_textbox.delete(0,END)
        dirname_textbox.insert(0,dirname)
        dirname_textbox.configure(state='disabled')
        CompressBtn.configure(state='normal')

    def startCompressor(dirname):
        print dirname
        from ImgCompressorV2 import CompressImage
        ci = CompressImage()
        ci.processdir(dirname)


    def cancelForm():
        dirname = ''
        dirname_textbox.configure(state='normal')
        dirname_textbox.delete(0,END)
        dirname_textbox.insert(0,dirname)
        dirname_textbox.configure(state='disabled')
        CompressBtn.configure(state='disabled')


    Button(root, text="...",fg='black',command=openDirectory).pack(**button_opt)
    CompressBtn = Button(root, text="Compress", fg='black', command=lambda:startCompressor(dirname[0]), state=DISABLED)
    CompressBtn.pack()
    Button(root, text="Cancel",fg='black', command=cancelForm).pack()

    root.mainloop()  


if __name__ == '__main__':
    main()