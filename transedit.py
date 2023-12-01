import tkinter as tk
from tkinter import scrolledtext

import tkinter.filedialog as fd
import re

import sys

class P:
    def __init__(self, text):
        self.lines = text.split('\n')
        self.pipeline = []
        self.start = self.line_generator()

    def line_generator(self):
        for line in self.lines:
            yield line

    def grep(self, pattern):
        def fn(lines):
            for line in lines:
                if pattern in line:
                    yield line
        self.pipeline.append(fn)
        return self

    def grep_v(self, pattern):
        def fn(lines):
            for line in lines:
                if pattern not in line:
                    yield line
        self.pipeline.append(fn)
        return self

    def replace(self, old, new):
        def fn(lines):
            for line in lines:
                yield line.replace(old, new)
        self.pipeline.append(fn)
        return self

    def run(self):
        current = self.start
        for process in self.pipeline:
            current = process(current)
        return '\n'.join(list(current))


class ScriptRunner:
    def __init__(self):
        self.transform = lambda x: x  # Default transform function

    def update_transform(self, new_transform_code):
        # Define a local transform function based on the new code
        local_vars = {'P': P,'re': re}
        exec(new_transform_code, globals(), local_vars)
        self.transform = local_vars.get('transform', self.transform)

    def transform(self, text):
        return text

def process_script():
    script_code = script_editor.get("1.0", tk.END)
    script_runner.update_transform(script_code)
    result = script_runner.transform(file_data)
    result_editor.delete("1.0", tk.END)
    result_editor.insert("1.0", result)



def save_file():
    file_path = fd.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, 'w') as file:
            file.write(result_editor.get("1.0", tk.END))

# Read file data if a file name is provided
if len(sys.argv) > 1:
    file_name = sys.argv[1]
    try:
        with open(file_name, 'r') as file:
            file_data = file.read()
    except IOError:
        print(f"Could not read file: {file_name}")
        sys.exit()
else:
    print("No file name provided. Exiting.")
    sys.exit()

# GUI setup
# GUI setup
root = tk.Tk()
root.title("Text Processor")

frame_left = tk.Frame(root)
frame_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

frame_right = tk.Frame(root)
frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

script_editor = scrolledtext.ScrolledText(frame_left, wrap=tk.WORD, height=10)
script_editor.pack(fill=tk.BOTH, expand=True)

result_editor = scrolledtext.ScrolledText(frame_right, wrap=tk.WORD, height=10)
result_editor.pack(fill=tk.BOTH, expand=True)

process_button = tk.Button(root, text="Process Script", command=process_script)
process_button.pack(fill=tk.X)

save_button = tk.Button(root, text="Save Result", command=save_file)
save_button.pack(fill=tk.X)


script_runner = ScriptRunner()
 
root.mainloop()




