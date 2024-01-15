import customtkinter
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from ToDoDb import ToDoDb
import tkinter.filedialog

class ToDoGuiCtk(customtkinter.CTk):
    def __init__(self, dataBase=ToDoDb()):
        super().__init__()
        self.db = dataBase

        self.title('Task Manager')
        self.geometry('1280x720')
        self.config(bg='#830C4F')
        self.resizable(False, False)

        self.font1 = ('Avenir', 18, 'bold')
        self.font2 = ('Avenir', 12, 'bold')

        self.day_label = self.newCtkLabel('Day')
        self.day_label.place(x=20, y=80)
        self.day_cboxVar = StringVar()
        self.day_cboxOptions = ['Monday','Tuesday','Wednesday','Thursday','Friday','Weekend']
        self.day_cbox = self.newCtkComboBox(options=self.day_cboxOptions, entryVariable=self.day_cboxVar)
        self.day_cbox.place(x=80, y=80)

        self.task_label = self.newCtkLabel('Task')
        self.task_label.place(x=20, y=120)
        self.task_entry = self.newCtkEntry()
        self.task_entry.place(x=80, y=120)

        self.status_label = self.newCtkLabel('Status')
        self.status_label.place(x=20, y=160)
        self.status_cboxVar = StringVar()
        self.status_cboxOptions = ['Not Started', 'In Progress', 'Done']
        self.status_cbox = self.newCtkComboBox(options=self.status_cboxOptions, 
                                    entryVariable=self.status_cboxVar)
        self.status_cbox.place(x=80, y=160)

        self.new_button = self.newCtkButton(text='New Task',
                                onClickHandler=lambda:self.clear_form(True),
                                fgColor='#FFACEC',
                                hoverColor='#C55297',
                                borderColor='#FFACEC')
        self.new_button.place(x=50,y=270)

        self.add_button = self.newCtkButton(text='Add Task',
                                onClickHandler=self.add_entry,
                                fgColor='#FFACEC',
                                hoverColor='#C55297',
                                borderColor='#FFACEC')
        self.add_button.place(x=50,y=320)

        self.update_button = self.newCtkButton(text='Update Task',
                                onClickHandler=self.update_entry,
                                fgColor='#FFACEC',
                                hoverColor='#C55297',
                                borderColor='#FFACEC')
        self.update_button.place(x=50,y=370)

        self.delete_button = self.newCtkButton(text='Delete Task',
                                onClickHandler=self.delete_entry,
                                fgColor='#FFACEC',
                                hoverColor='#C55297',
                                borderColor='#FFACEC')
        self.delete_button.place(x=50,y=420)
        
        self.import_button = self.newCtkButton(text='Import Week from CSV',
                                onClickHandler=self.import_from_csv,
                                fgColor='#C4ACFF',
                                hoverColor='#AB52C5',
                                borderColor='#C4ACFF')
        self.import_button.place(x=50,y=510)

        self.exportCSV_button = self.newCtkButton(text='Export Week to CSV',
                                onClickHandler=self.export_to_csv,
                                fgColor='#C4ACFF',
                                hoverColor='#AB52C5',
                                borderColor='#C4ACFF')
        self.exportCSV_button.place(x=50,y=560)

        self.exportJSON_button = self.newCtkButton(text='Export Week to JSON',
                                onClickHandler=self.export_to_json,
                                fgColor='#C4ACFF',
                                hoverColor='#AB52C5',
                                borderColor='#C4ACFF')
        self.exportJSON_button.place(x=50,y=610)

        self.day_treeviews = {}
        self.newTreeview(day='monday' , i=360, j=60)
        self.newTreeview(day='tuesday', i=655, j=60)
        self.newTreeview(day='wednesday', i=950, j=60, z=88)
        self.newTreeview(day='thursday', i=360, j=400, z=100)
        self.newTreeview(day='friday', i=655, j=400, z=111)
        self.newTreeview(day='weekend', i=950, j=400, z=98)
        self.add_to_treeview()

        self.current_selected_item = None

    def newTreeview(self, day, i, j, z=103):
        self.tree_label = self.newCtkLabel(text=day.capitalize(), widget_BgColor = '#4E2780', widget_padx=z, widget_pady=3)
        self.tree_label.place(x=i, y=j-28)
        
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.style.configure('Treeview', 
                        font=self.font2, 
                        foreground='#000',
                        fieldlbackground='#313837')

        self.tree = ttk.Treeview(self, name=day, height=15, selectmode="browse")
        self.tree['columns'] = ('Task', 'Status')
        self.tree.column('#0', width=0, stretch=tk.NO)
        self.tree.column('Task', anchor=tk.CENTER, width=170)
        self.tree.column('Status', anchor=tk.CENTER, width=80)

        self.tree.heading('Task', text='Task')
        self.tree.heading('Status', text='Status')

        self.tree.tag_configure('Not Started', background='#FFE3DE')
        self.tree.tag_configure('In Progress', background='#C8B3EE')
        self.tree.tag_configure('Done', background='#A16AE8')

        self.tree.place(x=i, y=j, width=275, height=270)
        self.tree.bind('<ButtonRelease-1>', lambda event, day=day: self.after(1, lambda: self.read_display_data(event, day)))

        self.day_treeviews[day] = self.tree
    def newCtkLabel(self, text = 'CTK Label', widget_BgColor='#830C4F', widget_padx=0, widget_pady=0):
        widget_Font=self.font1
        widget_TextColor='#FFF'

        widget = customtkinter.CTkLabel(self, 
                                    text=text,
                                    font=widget_Font, 
                                    text_color=widget_TextColor,
                                    bg_color=widget_BgColor,
                                    padx=widget_padx,
                                    pady=widget_pady)
        return widget
    def newCtkEntry(self, text = 'CTK Label'):
        widget_Font=self.font1
        widget_TextColor='#000'
        widget_FgColor='#FFF'
        widget_BorderColor='#830C4F'
        widget_BorderWidth=0
        widget_Width=250

        widget = customtkinter.CTkEntry(self,
                                    font=widget_Font,
                                    text_color=widget_TextColor,
                                    fg_color=widget_FgColor,
                                    border_color=widget_BorderColor,
                                    border_width=widget_BorderWidth,
                                    width=widget_Width)
        return widget
    def newCtkComboBox(self, options=['DEFAULT', 'OTHER'], entryVariable=None):
        widget_Font=self.font1
        widget_TextColor='#000'
        widget_FgColor='#FFF'
        widget_DropdownHoverColor='#FFACEC'
        widget_BorderColor='#FA89E1'
        widget_ButtonColor='#FFACEC'
        widget_ButtonHoverColor='#FA89E1'
        widget_Width=250
        widget_Options=options

        widget = customtkinter.CTkComboBox(self,
                                        font=widget_Font,
                                        text_color=widget_TextColor,
                                        fg_color=widget_FgColor,
                                        border_color=widget_BorderColor,
                                        width=widget_Width,
                                        variable=entryVariable,
                                        values=options,
                                        state='readonly')
        widget.set(options[0])
        return widget
    def newCtkButton(self, text = 'CTK Button', onClickHandler=None, fgColor='#161C25', hoverColor='#FF5002', bgColor='#830C4F', borderColor='#161C25'):
        widget_Font=self.font1
        widget_TextColor='#FFF'
        widget_FgColor=fgColor
        widget_HoverColor=hoverColor
        widget_BackgroundColor=bgColor
        widget_BorderColor=borderColor
        widget_BorderWidth=2
        widget_Cursor='hand2'
        widget_CornerRadius=15
        widget_Width=260
        widget_Function=onClickHandler

        widget = customtkinter.CTkButton(self,
                                        text=text,
                                        command=widget_Function,
                                        font=widget_Font,
                                        text_color=widget_TextColor,
                                        fg_color=widget_FgColor,
                                        hover_color=widget_HoverColor,
                                        bg_color=widget_BackgroundColor,
                                        border_color=widget_BorderColor,
                                        border_width=widget_BorderWidth,
                                        cursor=widget_Cursor,
                                        corner_radius=widget_CornerRadius,
                                        width=widget_Width)
       
        return widget
    
    def add_to_treeview(self):
        for day_treeview in self.day_treeviews.values():
            day_treeview.selection_remove(day_treeview.selection())
            day_treeview.delete(*day_treeview.get_children())
        
        tasks = self.db.fetch_task()
        for task in tasks:
            day = task[0]
            day_treeview = self.day_treeviews.get(day)
            if day_treeview:
                day_treeview.insert('', END, values=(task[1], task[2]), tag=(task[2],))
    def clear_form(self, *clicked):
        if clicked:
            self.tree.selection_remove(self.tree.focus())
            self.tree.focus('')

        self.day_cboxVar.set('Monday')
        self.task_entry.delete(0, END)
        self.task_entry.configure(state='normal')
        self.status_cboxVar.set('Not Started')
    def add_entry(self):
        day = self.day_cboxVar.get().lower()
        task = self.task_entry.get()
        status = self.status_cboxVar.get()

        if not (day and task and status):
            return messagebox.showerror('Error', 'Enter all fields.')
        elif self.db.task_exists(task, day):
            return messagebox.showerror('Error', 'Task already exists for this day')
        else:
            return self.db.insert_task(day, task, status), messagebox.showinfo('Success', 'Task has been added'), self.clear_form(), self.add_to_treeview() 

    def read_display_data(self, event, day):
        tree_for_day = self.day_treeviews.get(day)
        selected_item = tree_for_day.focus()

        if self.current_selected_item:
            try:
                self.day_treeviews[self.current_selected_item[0]].selection_remove(self.current_selected_item[1])
            except tk.TclError:
                pass
        self.current_selected_item = (day, selected_item)

        if selected_item:
            row = tree_for_day.item(selected_item, 'values')
            self.clear_form()
            self.day_cboxVar.set(day.capitalize())
            self.task_entry.insert(0, row[0])
            self.status_cboxVar.set(row[1])
        else:
            pass
    def delete_entry(self):
        if self.current_selected_item is None:
            return messagebox.showerror('Error', 'Choose a task to delete')
        
        current_day, selected_item = self.current_selected_item
        tree_for_day = self.day_treeviews.get(current_day)
        current_task = tree_for_day.item(selected_item, 'values')[0]

        if self.db.delete_task(current_task, current_day):
            return messagebox.showinfo('Success', 'Task has been deleted'), self.clear_form(), self.add_to_treeview()
        else:
            return messagebox.showerror('Error', 'Task not found or not deleted')   
    def update_entry(self):
        if self.current_selected_item is None:
            return messagebox.showerror('Error', 'Choose a task to update.')
        
        current_day, selected_item = self.current_selected_item
        tree_for_day = self.day_treeviews.get(current_day)
        current_task = tree_for_day.item(selected_item, 'values')[0]
        current_status = tree_for_day.item(selected_item, 'values')[1]

        new_day = self.day_cboxVar.get().lower()
        new_task = self.task_entry.get()
        new_status = self.status_cboxVar.get()

        if not (new_day and new_task and new_status):
            return messagebox.showerror('Error', 'Enter all fields.')
        elif (new_day==current_day and new_task==current_task and new_status==current_status):
            return messagebox.showerror('Error', 'Enter new data.')
        elif current_status==new_status and self.db.task_exists(new_task, new_day):
            return messagebox.showerror('Error', 'Task already exists for this day')
        elif self.db.update_task(current_day, current_task, new_day, new_task, new_status):
            return messagebox.showinfo('Success', 'Task has been updated'), self.clear_form(), self.add_to_treeview()
        else:
            return messagebox.showerror('Error', 'Task not found or not updated')

    def export_to_csv(self):
        try:
            return self.db.export_csv(), messagebox.showinfo('Success', f'Data exported to {self.db.dbName}.csv')
        except:
            return messagebox.showerror('Error', 'Data cannot be exported to .csv.')
    def export_to_json(self):
        try:
            return self.db.export_json(), messagebox.showinfo('Success', f'Data exported to {self.db.dbName}.json')
        except:
            return messagebox.showerror('Error', 'Data cannot be exported to .json.')
    def import_from_csv(self):
        file = tkinter.filedialog.askopenfilename()
        try:
            if not file.lower().endswith('.csv'):
                return messagebox.showerror('Error', 'Data cannot be imported. Choose a .csv file.')
            return self.db.import_csv(file), self.add_to_treeview(), messagebox.showinfo('Success', f'Data imported from {file}.csv')
        except:
            return messagebox.showerror('Error', 'Data cannot be imported.')




