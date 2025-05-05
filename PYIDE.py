from tkinter import *
from tkinter.filedialog import asksaveasfilename, askopenfilename
from tkinter import ttk
import subprocess

compiler = Tk()
compiler.title('PYIDE')
compiler.geometry(f"{compiler.winfo_screenwidth()}x{compiler.winfo_screenheight()}")

themes = {
    "light": {"bg": "white", "fg": "black", "insert": "black", "select_bg": "#cce7ff", "select_fg": "black"},
    "dark": {"bg": "#1e1e1e", "fg": "white", "insert": "white", "select_bg": "#444444", "select_fg": "white"}
}
current_theme = "light"

notebook = ttk.Notebook(compiler)
notebook.pack(fill=BOTH, expand=True)

file_paths = {}

def apply_theme(theme):
    global current_theme
    current_theme = theme
    colors = themes[theme]
    for tab in notebook.tabs():
        frame = notebook.nametowidget(tab)
        text_widget = frame.winfo_children()[0]
        text_widget.config(bg=colors["bg"], fg=colors["fg"], insertbackground=colors["insert"],
                           selectbackground=colors["select_bg"], selectforeground=colors["select_fg"])
    code_output.config(bg=colors["bg"], fg=colors["fg"], insertbackground=colors["insert"],
                       selectbackground=colors["select_bg"], selectforeground=colors["select_fg"])
    compiler.config(bg=colors["bg"])

def add_new_tab(content='', path=''):
    global file_paths
    frame = Frame(notebook)
    text_editor = Text(frame, wrap=NONE, bg=themes[current_theme]["bg"], fg=themes[current_theme]["fg"],
                       insertbackground=themes[current_theme]["insert"], selectbackground=themes[current_theme]["select_bg"],
                       selectforeground=themes[current_theme]["select_fg"])
    text_editor.insert('1.0', content)
    text_editor.pack(fill=BOTH, expand=True)
    tab_title = path if path else "Untitled"
    notebook.add(frame, text=f"{tab_title}   ")
    file_paths[frame] = path

def close_tab():
    current_tab = notebook.select()
    if current_tab:
        notebook.forget(current_tab)

def get_current_tab():
    return notebook.nametowidget(notebook.select())

def open_file():
    paths = askopenfilename(filetypes=[('Python Files', '*.py')], multiple=True)
    for path in paths:
        if path:
            try:
                with open(path, 'r', encoding='utf-8') as file:
                    code = file.read()
                    add_new_tab(content=code, path=path)
            except UnicodeDecodeError:
                error_popup = Toplevel()
                error_popup.title("Encoding Error")
                Label(error_popup, text="Cannot open file: Encoding must be UTF-8",
                      bg=themes[current_theme]["bg"], fg=themes[current_theme]["fg"]).pack(pady=10)
                Button(error_popup, text="OK", command=error_popup.destroy, bg=themes[current_theme]["bg"],
                       fg=themes[current_theme]["fg"]).pack(pady=5)

def save_as():
    current_tab = get_current_tab()
    text_widget = current_tab.winfo_children()[0]
    path = asksaveasfilename(filetypes=[('Python Files', '*.py')])
    if path:
        with open(path, 'w', encoding='utf-8') as file:
            code = text_widget.get('1.0', END)
            file.write(code)
        notebook.tab(current_tab, text=path)
        file_paths[current_tab] = path

def save():
    current_tab = get_current_tab()
    text_widget = current_tab.winfo_children()[0]
    path = file_paths.get(current_tab, '')
    if not path:
        save_as()
    else:
        with open(path, 'w', encoding='utf-8') as file:
            code = text_widget.get('1.0', END)
            file.write(code)

def run():
    current_tab = get_current_tab()
    path = file_paths.get(current_tab, '')
    if not path:
        save_as_prompt = Toplevel()
        save_as_prompt.title("Save Required")
        Label(save_as_prompt, text="Please save your code first!", bg=themes[current_theme]["bg"],
              fg=themes[current_theme]["fg"]).pack(pady=10)
        Button(save_as_prompt, text="OK", command=save_as_prompt.destroy, bg=themes[current_theme]["bg"],
               fg=themes[current_theme]["fg"]).pack(pady=5)
        return
    command = f'python "{path}"'
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    code_output.delete('1.0', END)
    code_output.insert('1.0', error if error else output)

menu_bar = Menu(compiler)

file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label='Open', command=open_file)
file_menu.add_command(label='Save', command=save)
file_menu.add_command(label='Save As', command=save_as)
file_menu.add_command(label='New Tab', command=lambda: add_new_tab())
file_menu.add_command(label='Close Tab', command=close_tab)
file_menu.add_command(label='Exit', command=compiler.quit)
menu_bar.add_cascade(label='File', menu=file_menu)

run_bar = Menu(menu_bar, tearoff=0)
run_bar.add_command(label='Run', command=run)
menu_bar.add_cascade(label='Run', menu=run_bar)

theme_menu = Menu(menu_bar, tearoff=0)
theme_menu.add_command(label='Light Theme', command=lambda: apply_theme("light"))
theme_menu.add_command(label='Dark Theme', command=lambda: apply_theme("dark"))
menu_bar.add_cascade(label='Theme', menu=theme_menu)

compiler.config(menu=menu_bar)

code_output = Text(compiler, height=10, bg=themes[current_theme]["bg"], fg=themes[current_theme]["fg"],
                   insertbackground=themes[current_theme]["insert"], selectbackground=themes[current_theme]["select_bg"],
                   selectforeground=themes[current_theme]["select_fg"])
code_output.pack(fill=X, padx=5, pady=5)

add_new_tab()

compiler.mainloop()
