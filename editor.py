import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox
from tkinter import filedialog as fd
from tkinter import font, simpledialog
from tkinter.simpledialog import askstring

buffer = []
FILETYPES = [
    ('All files', '*.*'),
    ('Python files', '*.py'),
    ('Perl scripts', '*.pl *.plx'),
    ('text files', '*.txt')
]
def custom_dialog(menu_option_name):
    messagebox.showinfo("Action",f"You selected the '{menu_option_name}' menu option.")

def new_file(text_widget):
    # Check if there's content in the text_widget
    if text_widget.get('1.0', 'end-1c').strip():
        # If there is content, prompt the user to save it
        if messagebox.askyesno("Save File", "Do you want to save the current file before creating a new one?"):
            # Call your save def, or implement saving logic here
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

def cut_text(text_widget):
    # Get the selected text
    selected_text = text_widget.get(tk.SEL_FIRST, tk.SEL_LAST)
    buffer.append(selected_text)
    if selected_text:
        # Delete the selected text
        text_widget.delete(tk.SEL_FIRST, tk.SEL_LAST)
        
def copy_text(text_widget):
    # Get the selected text
    selected_text = text_widget.get(tk.SEL_FIRST, tk.SEL_LAST)
    
    if selected_text:
        # Store the selected text in a buffer (e.g., a list)
        buffer.append(selected_text)

def paste_text(text_widget):
    # Get the current cursor position
    cursor_pos = text_widget.index(tk.INSERT)

    # Retrieve text from the buffer (if available)
    if buffer:
        text_to_paste = buffer.pop()
        text_widget.insert(cursor_pos, text_to_paste)

        # Clear the buffer after pasting
        buffer.clear()

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

            # Highlight the found occurrence
            end_pos = f"{start_pos}+{len(search_query)}c"
            text_widget.tag_add("highlight", start_pos, end_pos)
            text_widget.tag_config("highlight", background="yellow")

            # Scroll to the found occurrence
            text_widget.see(start_pos)

            # Prompt the user to continue
            user_response = messagebox.askyesno("Next occurrence", "Found. Continue?", parent=text_widget.winfo_toplevel())
            if not user_response:
                # Remove the highlight from all occurrences
                text_widget.tag_remove("highlight", "1.0", tk.END)
                break

            # Move to the next position
            start_pos = end_pos

def replace_text(text_widget):
    
    # Create a custom dialog box
    dialog = tk.Toplevel()
    dialog.title("Replace Text")

    # Set a fixed size for the dialog box
    dialog_width = 250
    dialog_height = 110
    dialog.geometry(f"{dialog_width}x{dialog_height}")

    # Add labels and entry widgets
    replace_label = tk.Label(dialog, text="Replace:")
    replace_entry = tk.Entry(dialog)
    with_label = tk.Label(dialog, text="With:")
    with_entry = tk.Entry(dialog)

    # Place widgets using grid layout
    replace_label.grid(row=0, column=0, padx=10, pady=5)
    replace_entry.grid(row=0, column=1, padx=10, pady=5)
    with_label.grid(row=1, column=0, padx=10, pady=5)
    with_entry.grid(row=1, column=1, padx=10, pady=5)

    # Add an "OK" button
    ok_button = tk.Button(dialog, text="OK", command=dialog.destroy)
    ok_button.grid(row=2, columnspan=2, padx=10, pady=10)

    # Center the dialog within the application window
    screen_width = dialog.winfo_screenwidth()
    screen_height = dialog.winfo_screenheight()
    x_position = (screen_width - dialog_width) // 2
    y_position = (screen_height - dialog_height) // 2
    dialog.geometry(f"{dialog_width}x{dialog_height}+{x_position}+{y_position}")    
def custom_dialog(message):
    # Implement your custom dialog logic here
    pass

def handle_arrow_keys(event):
    # Implement your logic for handling arrow keys here
    pass

def main(root):
    global text_widget
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    width = screen_width // 2
    height = screen_height // 2

    # Set the position and size of the window (format: widthxheight+x+y)
    root.geometry(f'{width}x{height}+{width // 2}+{height // 2}')

    root.wm_title("My Editor")
    menubar = tk.Menu(root)
    root.config(menu=menubar)

    # Set the default font
    default_font = font.Font(family='Arial', size=14)

    # Create a ScrolledText widget
    text_widget = ScrolledText(root, wrap='word', font=default_font)
    text_widget.pack(fill=tk.BOTH, expand=True)

    # Create a file menu
    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=file_menu)
    # Add items to the file menu (you can adapt this part as needed)
    file_menu.add_command(label="New", command=lambda: new_file(text_widget))
    file_menu.add_command(label="Open", command=lambda: open_file(text_widget))
    file_menu.add_command(label="Save", command=lambda: save_file(text_widget))
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)

    # Create the edit menu
    edit_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Edit", menu=edit_menu)

    # Add items to the edit menu
    edit_menu.add_command(label="Cut", command=lambda: cut_text(text_widget))
    edit_menu.add_command(label="Copy", command=lambda: copy_text(text_widget))
    edit_menu.add_command(label="Paste", command=lambda: paste_text(text_widget))
    
    # Create the search menu
    search_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Search", menu=search_menu)

    # Add items to the menu
    search_menu.add_command(label="Find", command=lambda: search_text(text_widget))
    search_menu.add_command(label="Replace", command=lambda: replace_text(text_widget))
    
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



























