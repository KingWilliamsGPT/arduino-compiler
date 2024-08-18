import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
import os.path
import platform
import sys


LINUX_COMPILER_NAME = 'arduino-cli'
WINDOWS_COMPILER_NAME = 'arduino-cli.exe'
COMPILER_DIRECTORY  = '.'

class UnsupportedOS(OSError):
    pass

def get_compiler(dir):
    # returns the path to the compilter for this os
    d = {
        'Windows': WINDOWS_COMPILER_NAME,
        'Linux': LINUX_COMPILER_NAME,
    }

    try:
        COMPILER_NAME = d[platform.system()]
    except KeyError:
        raise UnsupportedOS('The current os is not supported')

    return os.path.join(dir, COMPILER_NAME)
    
    

class ArduinoCompilerApp:
    def __init__(self, root, arduino_cli):
        self.root = root
        self.root.title("Arduino Sketch Compiler")
        self.arduino_cli = arduino_cli

        # Create UI elements
        self.create_widgets()
        self.create_menu()

    def create_widgets(self):
        # Sketch file selection
        self.sketch_label = tk.Label(self.root, text="Select Sketch File:")
        self.sketch_label.grid(row=0, column=0, padx=10, pady=10)

        self.sketch_path = tk.Entry(self.root, width=50)
        self.sketch_path.grid(row=0, column=1, padx=10, pady=10)

        self.browse_sketch_button = tk.Button(self.root, text="Browse", command=self.browse_sketch)
        self.browse_sketch_button.grid(row=0, column=2, padx=10, pady=10)

        # Output directory selection
        self.output_label = tk.Label(self.root, text="Select Output Directory:")
        self.output_label.grid(row=1, column=0, padx=10, pady=10)

        self.output_path = tk.Entry(self.root, width=50)
        self.output_path.grid(row=1, column=1, padx=10, pady=10)

        self.browse_output_button = tk.Button(self.root, text="Browse", command=self.browse_output)
        self.browse_output_button.grid(row=1, column=2, padx=10, pady=10)

        # Compile button
        self.compile_button = tk.Button(self.root, text="Compile", command=self.compile_sketch)
        self.compile_button.grid(row=2, column=1, padx=10, pady=20)

    def create_menu(self):
        # Create menu bar
        menubar = tk.Menu(self.root)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="How to Use", command=self.show_instructions)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menubar)

    def browse_sketch(self):
        # Open file dialog to select the sketch file
        sketch_file = filedialog.askopenfilename(
            title="Select Sketch File",
            filetypes=(("Arduino Sketch", "*.ino"), ("All Files", "*.*"))
        )
        if sketch_file:
            self.sketch_path.delete(0, tk.END)
            self.sketch_path.insert(0, sketch_file)

    def browse_output(self):
        # Open file dialog to select the output directory
        output_dir = filedialog.askdirectory(title="Select Output Directory")
        if output_dir:
            self.output_path.delete(0, tk.END)
            self.output_path.insert(0, output_dir)

    def compile_sketch(self):
        sketch_file = self.sketch_path.get()
        output_dir = self.output_path.get().strip()
        arduino_cli = self.arduino_cli

        # for debugging
        self.sf = sketch_file
        self.dst = output_dir 

        if not sketch_file:
            messagebox.showerror("Error", "Please select both a sketch file and an output directory.")
            return
        if not output_dir:
            output_dir = os.path.join(os.path.dirname(sketch_file), 'jargons')
            if not os.path.exists(output_dir):
                os.mkdir(output_dir)

        # Compile the sketch using arduino-cli
        try:
            command = f"{arduino_cli} compile --fqbn arduino:avr:uno --output-dir \"{output_dir}\" \"{sketch_file}\""
            
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                # print(result.stdout)
                messagebox.showinfo("Success", f"Compilation successful! HEX file saved in {output_dir}.")
            else:
                messagebox.showerror("Compilation Failed", result.stderr)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Compilation Failed", f"An error occurred during compilation:\n{e}")

    def show_instructions(self):
        instructions = (
            "1. Click the 'Browse' button next to 'Select Sketch File' to choose your Arduino sketch (.ino file).\n"
            "2. Click the 'Browse' button next to 'Select Output Directory' to choose the directory where the compiled HEX file will be saved.\n"
            "3. Click the 'Compile' button to compile the sketch and save the HEX file to the selected directory.\n"
            "4. Ensure that 'arduino-cli' is installed and available in your system's PATH."
        )
        messagebox.showinfo("How to Use", instructions)


if __name__ == "__main__":
    try:
        arduino_cli_excecutable = get_compiler(os.path.dirname(__file__))
    except UnsupportedOS as ex:
        messagebox.showerror('Unsupported OS', str(ex))
        sys.exit(1)
    root = tk.Tk()
    app = ArduinoCompilerApp(root, arduino_cli=arduino_cli_excecutable)
    root.mainloop()
