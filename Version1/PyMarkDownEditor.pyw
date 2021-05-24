from tkinter import *
from tkinter import filedialog,messagebox, font
from TkToolTip import ToolTip
from tkinter.simpledialog import askstring
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk
# pip install tkfontchooser
from tkfontchooser import askfont
from datetime import datetime
from markdown2 import Markdown
from tkhtmlview import HTMLScrolledText

class MarkDown:
    def __init__(self,root):
        self.root = root
        self.myfont = font.Font(family="Helvetica", size=14)
        
        self.cursorPosition = "0.0"
        self.ul = False
        self.ol = False
        self.ol_count = 1       
        
        #--------------------------- Create Menubar ------------------------
        
        my_menu=Menu(self.root)
        file_menu= Menu(my_menu,tearoff=0)
        tools_menu = Menu(my_menu,tearoff=0)
        edit_menu = Menu(my_menu,tearoff=0)
        about_menu = Menu(my_menu,tearoff=0)
        # ---- File Menu ----- #
        my_menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New File", command=self.newFile,accelerator="Ctrl+n")
        file_menu.add_command(label="Open File",command=self.openFile, accelerator="Ctrl+o")
        file_menu.add_command(label="Save File",command=self.saveFile, accelerator="Ctrl+n")
        file_menu.add_separator()
        file_menu.add_command(label="Exit",command=self.closeApp, accelerator="Ctrl+q")
        
        my_menu.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Cut",command=lambda: self.inputeditor.event_generate("<<Cut>>"), accelerator="Ctrl+x")
        edit_menu.add_command(label="Copy",command=lambda: self.inputeditor.event_generate("<<Copy>>"), accelerator="Ctrl+c")
        edit_menu.add_command(label="Paste",command=lambda: self.inputeditor.event_generate("<<Paste>>"), accelerator="Ctrl+p")
        edit_menu.add_command(label="UNDO",command=lambda: self.inputeditor.edit_undo(), accelerator="Ctrl+z")
        edit_menu.add_command(label="REDO",command=lambda: self.inputeditor.edit_redo(), accelerator="Ctrl+y")
        
        my_menu.add_cascade(label="Tools", menu=tools_menu)
        #tools_menu.add_command(label="Change Theme",command=self.changeTheme, accelerator="Ctrl+T")
        tools_menu.add_command(label="Change Font",command=self.changeFont, accelerator="Ctrl+f")
        
        my_menu.add_cascade(label="About", menu=about_menu)
        about_menu.add_command(label="About PyMark",command=self.aboutPyMark)
        
        self.root.config(menu=my_menu)
        
        top_frame = Frame(self.root,bd=1,relief=RAISED)
        top_frame.place(x=5,y=2,width=995,height=35)
        
        self.imageConfig()
        # --------- Top Frame Widgets ---------------#
        
        save_btn = Button(top_frame,image=self.save_img,relief=FLAT,command=self.saveFile)
        save_btn.grid(row=0,column=0,padx=1)
        save_tip = ToolTip(save_btn,"Save File")
        save_btn.image = self.save_img
        
        head_btn = Button(top_frame,image=self.head_img,relief=FLAT,command=self.addHeading)
        head_btn.grid(row=0,column=1,padx=1)
        head_tip = ToolTip(head_btn,"Add Heading")
        head_btn.image = self.head_img
        
        text_btn = Button(top_frame,image=self.text_img,relief=FLAT,command=self.addText)
        text_btn.grid(row=0,column=2,padx=1)
        text_tip = ToolTip(text_btn,"Add Text")
        text_btn.image = self.text_img
             
        bold_btn = Button(top_frame,image=self.bold_img,relief=FLAT,command=self.addBold)
        bold_btn.grid(row=0,column=3,padx=1)
        bold_tip = ToolTip(bold_btn,"Bold")
        bold_btn.image = self.bold_img
        
        italic_btn = Button(top_frame,image=self.itlc_img,relief=FLAT,command=self.addItalic)
        italic_btn.grid(row=0,column=4,padx=1)
        italic_tip = ToolTip(italic_btn,"Italic")
        italic_btn.image = self.itlc_img
                
        line_btn = Button(top_frame,image=self.line_img,relief=FLAT,command=self.addLine)
        line_btn.grid(row=0,column=5,padx=2)
        line_tip = ToolTip(line_btn,"Add Line")
        line_btn.image = self.line_img
        
        code_btn = Button(top_frame,image=self.code_img,relief=FLAT,command=self.addCode)
        code_btn.grid(row=0,column=6,padx=2)
        code_tip = ToolTip(code_btn,"Add Code")
        code_btn.image = self.code_img
        
        ol_btn = Button(top_frame,image=self.ol_img,relief=FLAT,command=self.addOL)
        ol_btn.grid(row=0,column=7,padx=2)
        ol_tip = ToolTip(ol_btn,"Ordered List")
        ol_btn.image = self.ol_img
        
        ul_btn = Button(top_frame,image=self.ul_img,relief=FLAT,command=self.addUL)
        ul_btn.grid(row=0,column=8,padx=2)
        ul_tip = ToolTip(ul_btn,"Unordered List")
        ul_btn.image = self.ul_img
        
        link_btn = Button(top_frame,image=self.link_img,relief=FLAT,command=self.addLink)
        link_btn.grid(row=0,column=9,padx=2)
        link_tip = ToolTip(link_btn,"Add Link")
        link_btn.image = self.link_img
        
        
        time_btn = Button(top_frame,image=self.time_img,relief=FLAT,command=self.addDateTime)
        time_btn.grid(row=0,column=10,padx=2)
        time_tip = ToolTip(time_btn,"Add Time & Date")
        time_btn.image = self.time_img
        
        about_btn = Button(top_frame,image=self.abut_img,relief=FLAT,command=self.aboutPyMark)
        about_btn.grid(row=0,column=11,padx=2)
        about_tip = ToolTip(about_btn,"About PyMark")
        about_btn.image = self.abut_img
        
        
        #----------- Input Box-------------#
        
        self.inputeditor = ScrolledText(self.root,font=self.myfont,bd=2,relief=GROOVE,undo=True,wrap=WORD)
        self.inputeditor.place(x=5,y=40,width=480,height=550)
        self.inputeditor.insert("1.0","## Hello World !")
        self.inputeditor.bindtags(('Text','post-class-bindings', '.', 'all'))
        self.inputeditor.bind_class("post-class-bindings", "<KeyPress>", self.check_pos)
        self.inputeditor.bind_class("post-class-bindings", "<Button-1>", self.check_pos)
        self.inputeditor.bind_class("post-class-bindings", "<Return>", self.nextLine)
        self.inputeditor.bind_class("post-class-bindings","<Control-Key-r>", self.refresh)
        
        self.inputeditor.bind_class("post-class-bindings","(", lambda event: self.autocomplete(event.widget,  ")"))
        self.inputeditor.bind_class("post-class-bindings","[", lambda event: self.autocomplete(event.widget,  "]"))
        self.inputeditor.bind_class("post-class-bindings","*", lambda event: self.autocomplete(event.widget,  "*"))
        self.inputeditor.bind_class("post-class-bindings",'"', lambda event: self.autocomplete(event.widget,  '"'))
        self.inputeditor.bind_class("post-class-bindings","_", lambda event: self.autocomplete(event.widget,  "_"))
        self.inputeditor.bind_class("post-class-bindings","{", lambda event: self.autocomplete(event.widget,  "}"))
 
        self.outputbox = HTMLScrolledText(self.root,bd=2,relief=GROOVE)
        self.outputbox.place(x=490,y=40,width=500,height=550)
        self.outputbox.set_html("<h2>Hello World !</h2>") 
        
        
        #---------Bind Root -------#
        self.root.bind_all('<Control-o>', self.openFile)
        self.root.bind_all('<Control-n>', self.newFile)
        self.root.bind_all('<Control-s>', self.saveFile)
        self.root.bind_all('<Control-q>', self.closeApp)
        self.root.bind_all('<Control-f>', self.changeFont)
        self.root.protocol("WM_DELETE_WINDOW",self.closeApp)
        
        
    def check_pos(self,*args):
        self.onInputChange()
        self.cursorPosition = self.inputeditor.index(INSERT)
        
    def refresh(self,*args):
        self.ul = False
        self.ol = False
        self.ol_count = 1
        
        
        
    def onInputChange(self):
        self.inputeditor.edit_modified(0)
        md2html = Markdown()
        # self.outputbox.set_html(md2html.convert(self.inputeditor.get("1.0" , END)))
        markdownText = self.inputeditor.get("1.0", END)
        html = md2html.convert(markdownText)
        self.outputbox.set_html(html)  
        
        
    def nextLine(self,*args):
        self.check_pos()
        pos = self.cursorPosition
        if self.ul:
            self.inputeditor.insert(pos,"* ")
            
        if self.ol:
            self.ol_count+=1
            self.inputeditor.insert(pos,f"{self.ol_count}. ")
        
        
    def addHeading(self):
        pos = self.cursorPosition
        self.inputeditor.insert(pos,"#")
        #self.inputeditor.mark_set("insert", f"{pos}")
        self.inputeditor.focus_set()
        
    def addText(self):
        pos = self.cursorPosition
        self.inputeditor.insert(pos,"__")
        #self.inputeditor.mark_set("insert", f"{pos}")
        self.inputeditor.focus_set()
        
    def addBold(self):
        pos = self.cursorPosition
        self.inputeditor.insert(pos,"****")
        self.inputeditor.focus_set()
        
    def addItalic(self):
        pos = self.cursorPosition
        self.inputeditor.insert(pos,"**")
        self.inputeditor.focus_set()
        
    def addUL(self):
        pos = self.cursorPosition
        self.ul = True
        self.inputeditor.insert(pos,"* ")
        self.inputeditor.focus_set()
        
    def addOL(self):
        pos = self.cursorPosition
        self.ol = True
        self.inputeditor.insert(pos,f"{self.ol_count}. ")
        self.inputeditor.focus_set()
        
    def addLine(self):
        """Line Will not Display on Right side because Tkhtmlview don't allow it."""
        pos = self.cursorPosition
        self.inputeditor.insert(pos,"\n-------------------\n")
        self.inputeditor.focus_set()

    
    def addLink(self):
        link = askstring("Add Link", "Enter Your Link")
        if link:
            pos = self.cursorPosition
            self.inputeditor.insert(pos,f"\n[enter link description here]({link})\n")
            self.inputeditor.focus_set()
        

    
    
    def addDateTime(self):
        # datetime object containing current date and time
        now = datetime.now()
        # dd/mm/YY H:M:S
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        
        pos = self.cursorPosition
        self.inputeditor.insert(pos,f"\n{dt_string}\n")
        self.inputeditor.focus_set()
        
    
    
    def addCode(self):
        pos = self.cursorPosition
        self.inputeditor.insert(pos,"     enter code here")
        self.inputeditor.focus_set()        
    
        
    def imageConfig(self):
        self.bold_img = PhotoImage(file=r'.\icons\bold.png') #
        self.head_img = PhotoImage(file=r'.\icons\heading.png')#
        self.code_img = PhotoImage(file=r'.\icons\code.png')#
        self.text_img = PhotoImage(file=r'.\icons\captext.png')#
        self.ul_img   = PhotoImage(file=r'.\icons\list.png') #
        self.ol_img   = PhotoImage(file=r'.\icons\ol.png')#
        self.save_img = PhotoImage(file=r'.\icons\save.png')#
        self.line_img = PhotoImage(file=r'.\icons\line.png')#
        self.itlc_img = PhotoImage(file=r'.\icons\italic.png')#
        self.link_img = PhotoImage(file=r'.\icons\link.png')#
        self.abut_img = PhotoImage(file=r'.\icons\question.png')#
        self.time_img = PhotoImage(file=r'.\icons\clock.png')#
        self.img_img  = PhotoImage(file=r'.\icons\image.png')#
        
    def changeFont(self,*args):
        font = askfont(root)
        # font is "" if the user has cancelled
        if font:
            # spaces in the family name need to be escaped
            font['family'] = font['family'].replace(' ', '\ ')
            font_str = "%(family)s %(size)i %(weight)s %(slant)s" % font
            if font['underline']:
                font_str += ' underline'
            if font['overstrike']:
                font_str += ' overstrike'
            
            self.myfont = font_str
            self.inputeditor.configure(font=self.myfont)
    
    def aboutPyMark(self):
        top = Toplevel(self.root)
        top.title("PyMarkDown")
        top.geometry("500x550")
        with open("pymarkdown-info.md",'r') as file:
            data = file.read()
        
        md2html = Markdown()
        html = md2html.convert(data)  
        
        display = HTMLScrolledText(top,bd=2,relief=GROOVE)
        display.set_html(html)
        
        display.pack(expand=True,fill=BOTH)
        top.mainloop()
    
    def closeApp(self,*args):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
            
    def autocomplete(self,widget,last):
        # insert the two characters at the insertion point
        widget.insert("insert", last)
        # move insertion cursor back one character
        widget.mark_set("insert", "insert-1c")
        # prevent the text widget from inserting the character that
        # triggered the event since we've already inserted it.
        return "break"
    
    def newFile(self,*args):
        if messagebox.askyesno("New File","This file is Not saved, \nDo you want to save it"):
            self.saveFile()
            self.inputeditor.delete('all')
            self.outputbox.delete('all')
        else:
            self.inputeditor.delete('1.0',END)
            self.outputbox.delete('1.0',END)
    
    def openFile(self,*args):
        openfilename = filedialog.askopenfilename(filetypes=(("Markdown File", "*.md , *.mdown , *.markdown"),
                                                            ("Text File", "*.txt"),
                                                            ("All Files", "*.*")))
        if openfilename:
            try:
                self.inputeditor.delete(1.0, END)
                self.inputeditor.insert(END, open(openfilename).read())
            except:
                # print("Cannot Open File!")
                messagebox.showerror("Error Opening Selected File" , 
                                     "Oops!, The file you selected : {} can not be opened!".format(openfilename))
    
    def saveFile(self,*args):
        filedata = self.inputeditor.get("1.0" , END)
        savefilename = filedialog.asksaveasfilename(filetypes = (("Markdown File", "*.md"),
                                                                  ("Text File", "*.txt")) , title="Save Markdown File")
        if savefilename:
            try:
                f = open(savefilename , "w")
                f.write(filedata)
            except:
                messagebox.showerror("Error Saving File" , 
                                     "Oops!, The File : {} can not be saved!".format(savefilename))
    
        
        
if __name__ == "__main__":
    root = Tk()
    root.title("MarkDown Editor")
    root.geometry("1000x600")
    root.resizable(0,0)
    MarkDown(root)
    root.mainloop()
