import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog as fd
from tkinter import font, simpledialog
from tkinter.simpledialog import askstring


FILETYPES = [
    ('All files', '*.*'),
    ('Python files', '*.py'),
    ('Perl scripts', '*.pl *.plx'),
    ('text files', '*.txt')
]

def custom_dialog(menu_option_name):
    messagebox.showinfo("Action",f"You selected the '{menu_option_name}' menu option.")

def copy_text(text_widget):
    """Copy the highlighted text in the text widget to the clipboard."""
    try:
        selected_text = text_widget.get(tk.SEL_FIRST, tk.SEL_LAST)
        if selected_text:
            root.clipboard_clear()
            root.clipboard_append(selected_text)
        else:
            raise ValueError("No text is currently selected.")
    except tk.TclError:
        # No text is currently selected
        pass
    except Exception as e:
        # Handle other exceptions
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

    # Calculate the dimensions for the dialog
    root_width = root.winfo_width()
    root_height = root.winfo_height()
    dialog_width = root_width // 4
    dialog_height = root_height // 4

def cut_text():
    # Get the selected text
    selected_text = text_widget.get(tk.SEL_FIRST, tk.SEL_LAST)

    if selected_text:
        # Remove the selected text from the text widget
        text_widget.delete(tk.SEL_FIRST, tk.SEL_LAST)

def search_text(text_widget):
    # Get the search query from the user
    search_query = simpledialog.askstring("Search", "Enter search query:")

    if search_query:
        # Clear any previous tags
        text_widget.tag_remove("highlight", "1.0", tk.END)

        # Search for the query in the text widget
        start_pos = "1.0"
        while True:
            start_pos = text_widget.search(search_query, start_pos, stopindex=tk.END, nocase=True)
            if not start_pos:
                break
            end_pos = f"{start_pos}+{len(search_query)}c"
            text_widget.tag_add("highlight", start_pos, end_pos)
            text_widget.tag_config("highlight", background="yellow")
            start_pos = end_pos


def handle_arrow_keys(event):
    if event.keysym == "Up":
        text_widget.mark_set("insert", text_widget.index(tk.INSERT + "-1c"))
    elif event.keysym == "Down":
        text_widget.mark_set("insert", text_widget.index(tk.INSERT + "+1c"))

def new_file(text_widget):
    # Check if there's content in the text_widget
    if text_widget.get('1.0', 'end-1c').strip():
        # If there is content, prompt the user to save it
        if messagebox.askyesno("Save File", "Do you want to save the current file before creating a new one?"):
            # Call your save function, or implement saving logic here
            save_file(text_widget)
    # Clear the text widget for a new file
    text_widget.delete('1.0', 'end')
    # Reset the window title or filename variable if needed


def open_file(text_widget):
    # Open the file dialog and get the selected file name
    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=FILETYPES
    )
    if filename:
        # Open the file for reading
        with open(filename, 'r') as file:
            # Read the file content
            content = file.read()
            # Insert the content into the text_widget
            text_widget.delete('1.0', 'end')  # Clear the current content
            text_widget.insert('1.0', content)  # Insert new content
    


def save_file(text_widget):
    if text_widget.get(1.0, tk.END).strip():
        filename = fd.asksaveasfilename(
            title='Save a file',
            initialdir='/',
            filetypes=FILETYPES
        )
        
        if filename:
            try:
                with open(filename, 'w') as file:
                    file_content = text_widget.get(1.0, tk.END)
                    file.write(file_content)
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

def main(root):
    global text_widget
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    width = screen_width // 2
    height = screen_height // 2

    # Set the position and size of the window (format: widthxheight+x+y)
    root.geometry(f'{width}x{height}+{width // 2}+{height // 2}')
    
    
    menubar = tk.Menu(root)
    root.config(menu=menubar)

    # Set the default font
    default_font = font.Font(family='Arial', size=14)
    # Create a text widget and a vertical scrollbar
    text_widget = tk.Text(root, wrap='word', font=default_font)
    scrollbar = tk.Scrollbar(root, command=text_widget.yview)
    text_widget.config(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
   


    # Create a file menu
    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=file_menu)

    # Add items to the file menu
    file_menu.add_command(label="New	  CTRL+n", command=lambda: new_file(text_widget))
    file_menu.add_command(label="Open	  CTRL+o", command=lambda: open_file(text_widget))
    file_menu.add_command(label="Save	  CTRL+s", command=lambda: save_file(text_widget))
    file_menu.add_separator()
    file_menu.add_command(label="Exit 	  CTRL+x", command=root.quit)
    # Create the edit menu
    edit_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Edit", menu=edit_menu)

    # Add items to the edit menu
    edit_menu.add_command(label="Cut", command=lambda: cut_text())
    edit_menu.add_command(label="Copy", command=lambda: copy_text(text_widget))
    edit_menu.add_command(label="Paste", command=lambda: paste_text(text_widget))
    
    # Create the search menu
    search_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Search", menu=search_menu)

    # Add items to the menu
    search_menu.add_command(label="Find", command=lambda: search_text(text_widget))
    search_menu.add_command(label="Replace", command=lambda: replace_text())
    
    # Create the about menu
    about_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="About", menu=about_menu)

    # Add items to the menu
    about_menu.add_command(label="Help", command = lambda: custom_dialog("About -> Help"))
    about_menu.add_command(label="Version", command = lambda: custom_dialog("About -> Version"))
    

    
if __name__ == "__main__":
    root = tk.Tk()
    main(root)
    # Key Bindings 
    text_widget.bind("<Up>", handle_arrow_keys)
    text_widget.bind("<Down>", handle_arrow_keys) 
    root.mainloop()































