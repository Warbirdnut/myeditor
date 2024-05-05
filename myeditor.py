import tkinter as tk
from tkinter import simpledialog
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import askyesno, showinfo, askokcancel, askquestion
from tkinter.simpledialog import askstring, askinteger
from tkinter import messagebox

# Globals

start_x, start_y = None, None

# Mouse functions

def on_mouse_down(event):
  global start_x, start_y
  start_x = event.x
  start_y = event.y

def on_mouse_move(event):
  if event.num == 1:
    end_x = event.x
    end_y = event.y
    text_area.tag_remove("sel", "1.0", tk.END)
    text_area.tag_add("sel", f"{start_x},{start_y}", f"{end_x},{end_y}")

# Key function

def tab_pressed(event: tk.Event) -> str:
  text_area.insert("insert", " " * 4)
  return "break"


def open_file():
   # Check if there are unsaved changes
    if text_area.get(1.0, tk.END).strip():
        response = askyesno("Save Changes", "Do you want to save changes before opening a new file?")
        if response:
            save_file()

    # Clear the text widget
    text_area.delete(1.0, tk.END)

    # Open the selected file (allowing multiple file types)
    file_path = askopenfilename(filetypes=[("All Files", "*.*"),("Python Files", "*.py"), ("Perl Files", "*.pl *.plx"), ("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "r") as file:
            text_area.insert(tk.END, file.read())



def save_file():
  files = [('All Files',"*.*"),('Python Files', '*.py'), ('Perl Files', '*.pl *.plx'), ('Text Files', '*.txt'), ('All Files', '*.*')]
  file_path = asksaveasfilename(filetypes=files, defaultextension='.py')
  if file_path:
    with open(file_path, 'w') as file:
        file.write(text_area.get(1.0, tk.END))



def new_file():
    # Prompt user to save current contents (if any)
    if text_area.get(1.0, tk.END).strip():
        response = askyesno("Save Changes", "Do you want to save changes before creating a new file?")
        if response:
            save_file()
	# Clear the text widget
    text_area.delete(1.0, tk.END)	
	
def select_all_text():

    text_area.tag_add("sel", "1.0", "end")

def select_text():
  pass

def copy_text():
  selected_text = text_area.selection_get()
  if selected_text:
    text_area.clipboard_clear()
    text_area.clipboard_append(selected_text)

def cut():
  selected_text = text_area.selection_get()
  if not selected_text:
    return
  # Cut the selected text (remove from the widget)
  text_area.delete("sel.first", "sel.last")

  # Add the selected text to the clipboard
  text_area.clipboard_clear()
  text_area.clipboard_append(selected_text)
def paste_text():
   text_area.insert("insert", text_area.clipboard_get())

def find():
    # Get the search term from a dialog box
    search_term = tk.simpledialog.askstring("Find", "Enter search term:")
    if search_term is None:
        return

    # Remove any previous highlighting
    text_area.tag_remove("highlight", "1.0", tk.END)

    # Start search from the beginning
    start_pos = "1.0"
    while True:
        # Search for the term
        match_pos = text_area.search(search_term, start_pos, tk.END)
        if not match_pos:
            break
        # Get the end position of the match
        end_pos = f"{match_pos}+{len(search_term)}c"

        # Highlight the match
        text_area.tag_add("highlight", match_pos, end_pos)
        text_area.tag_config("highlight", background="yellow")

        # Update start position for next search
        start_pos = end_pos		
		
def replace():
    original_string = askstring("Replace", "Enter the original string:")
    replacement_string = askstring("Replace", "Enter the replacement string:")

    if original_string and replacement_string:
        # Find the first occurrence
        start_idx = text_area.search(original_string, "1.0", stopindex=tk.END)
        while start_idx:
            end_idx = f"{start_idx}+{len(original_string)}c"
            # Highlight the match (customize the background color or font style)
            text_area.tag_add("highlight", start_idx, end_idx)
            text_area.tag_config("highlight", background="yellow")  # Customize the highlight color
            # Prompt the user for replacement
            response = askquestion("Replace", f"Replace this occurrence of '{original_string}'?")
            if response == "yes":
                # Delete the original string and insert the replacement string
                text_area.delete(start_idx, end_idx)
                text_area.insert(start_idx, replacement_string)
            # Move to the next occurrence
            start_idx = text_area.search(original_string, end_idx, stopindex=tk.END)
            if not start_idx:
                # No more occurrences found, break out of the loop
                break
            # Ask if the user wants to replace all instances
            response_all = askquestion("Replace All", f"Replace all remaining occurrences of '{original_string}'?")
            if response_all == "no":
                # Remove the highlight for this match
                text_area.tag_remove("highlight", start_idx, end_idx)
                # Move to the next occurrence
                start_idx = text_area.search(original_string, end_idx, stopindex=tk.END)
        # Remove all highlights after a brief delay (optional)
        text_area.after(2000, lambda: text_area.tag_remove("highlight", "1.0", tk.END))  
		
def show_about_dialog():
  version = ".01"  # Replace with your actual version
  showinfo("About", f"Application Version: {version}")

def show_edit_menu(event):
  # Get the coordinates of the right click
  x = root.winfo_x() + event.x
  y = root.winfo_y() + event.y

  # Pop up the edit menu at the clicked coordinates
  edit_menu.tk_popup(x, y)


def exit_app():
  response = askyesno("Really Exit?", "Do you really want to exit?")
  if response:
      if text_area.get(1.0, tk.END).strip():
          response = askyesno("Save Changes", "Do you want to save changes before exiting?")
          if response:
              save_file()
  root.destroy()

def on_scroll(event):
  # Identify the location of the mouse click
  if event.delta > 0:
    # Scroll down if mouse wheel is scrolled down (positive delta)
    text_area.yview_scroll(1, 'units')
  else:
    # Scroll up if mouse wheel is scrolled up (negative delta)
    text_area.yview_scroll(-1, 'units')

root = tk.Tk()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Get the desired width and height
desired_width = screen_width // 2
desired_height = screen_height

root.geometry(f"{desired_width}x{desired_height}")
root.title("My Editor")
root.iconbitmap('./icon.ico')

# Text Widget
text_area = tk.Text(root, wrap=tk.WORD, font=('Arial',14))

# Scrollbar
scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL)

# Create scrollbar-text area association
text_area.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=text_area.yview)

# Pack the widgets
text_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5, side=tk.LEFT)
scrollbar.pack(fill=tk.BOTH, side=tk.RIGHT)

# Bind the scrollbar to the Text widget
text_area.bind("<MouseWheel>", on_scroll)

# File Menu
menu_bar = tk.Menu(root)
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label=" New            Ctrl+n", command=new_file)
file_menu.add_command(label=" Open          Ctrl+o", command=open_file)
file_menu.add_command(label=" Save            Ctrl+s", command=save_file)
file_menu.add_separator()
file_menu.add_command(label=" Exit              Ctrl+x", command=exit_app)
menu_bar.add_cascade(label="File", menu=file_menu)

# Edit Menu 
edit_menu=tk.Menu(menu_bar,tearoff=0)
edit_menu.add_command(label="Cut            Ctrl+t",command=cut)
edit_menu.add_command(label="Copy         Ctrl+c",command=copy_text)
edit_menu.add_command(label="Paste         Ctrl+p",command=paste_text)
edit_menu.add_separator()
edit_menu.add_command(label="Select       Ctrl+s", command=select_text)
edit_menu.add_command(label="Select All  Ctrl+a", command=select_all_text)
menu_bar.add_cascade(label="Edit",menu=edit_menu)

# Search Manu
search_menu=tk.Menu(menu_bar,tearoff=0)
search_menu.add_command(label="Find            Ctrl+f", command=find)
search_menu.add_command(label="Replace      Ctrl+r", command=replace)
menu_bar.add_cascade(label="Search",menu=search_menu)

# About Menu
about_menu = tk.Menu(menu_bar, tearoff=0)
about_menu.add_command(label="Version", command=show_about_dialog)
menu_bar.add_cascade(label="About", menu=about_menu)


# Keyboard Bindings
root.bind("<Control-a>", lambda event: select_all_text())
root.bind("<Control-c>", lambda event: copy_text())
root.bind("<Control-f>", lambda event: find())
root.bind("<Control-n>", lambda event: new_file())
root.bind("<Control-o>", lambda event: open_file())
root.bind("<Control-p>", lambda event: paste_text())
root.bind("<Control-r>", lambda event: replace())
root.bind("<Control-s>", lambda event: save_file())
root.bind("<Control-t>", lambda event:cut())
root.bind("<Control-x>",lambda event:exit_app())

# Mouse Bindings
root.bind("<Button-1>",on_mouse_down)
root.bind("<B1-Motion>",on_mouse_move)
root.bind("<Button-3>", show_edit_menu)

# Additional Bindings
root.protocol("WM_DELETE_WINDOW", exit_app)
text_area.bind("<Tab>",tab_pressed)

root.config(menu=menu_bar)

root.mainloop()



