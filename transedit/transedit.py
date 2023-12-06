import tkinter as tk
from tkinter import scrolledtext

import tkinter.filedialog as fd
import re

from bs4 import BeautifulSoup

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

    def re_search(self, pattern):
        def fn(lines):
            for line in lines:
                if re.search(pattern, line):
                    yield line
        self.pipeline.append(fn)
        return self
        
    def re_search_fails(self, pattern):
        def fn(lines):
            for line in lines:
                if not re.search(pattern, line):
                    yield line
        self.pipeline.append(fn)
        return self

    def replace(self, old, new):
        def fn(lines):
            for line in lines:
                yield line.replace(old, new)
        self.pipeline.append(fn)
        return self
      
    def re_sub(self, pattern, new_pattern):  # Added re_sub function
        def fn(lines):
            for line in lines:
                yield re.sub(pattern, new_pattern, line)
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
        local_vars = {'P': P,'re': re, 'BeautifulSoup': BeautifulSoup}
        exec(new_transform_code, globals(), local_vars)
        self.transform = local_vars.get('transform', self.transform)

    def transform(self, text):
        return text


class TransEdit :

    def __init__(self,init_data="") :
        self.file_data = init_data
        self.script_runner = ScriptRunner()
        
        self.root = tk.Tk()
        self.root.title("Transedit")

        self.frame_left = tk.Frame(self.root)
        self.frame_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.frame_right = tk.Frame(self.root)
        self.frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.script_editor = scrolledtext.ScrolledText(self.frame_left, wrap=tk.WORD, height=10)
        self.script_editor.pack(fill=tk.BOTH, expand=True)

        self.result_editor = scrolledtext.ScrolledText(self.frame_right, wrap=tk.WORD, height=10)
        self.result_editor.pack(fill=tk.BOTH, expand=True)

        # Buttons
        self.load_data_btn = tk.Button(self.root, text="Load Data File", command=self.load_data_file)
        self.load_data_btn.pack(side=tk.TOP)
        
        self.load_script_btn = tk.Button(self.root, text="Load Script File", command=self.load_script_file)
        self.load_script_btn.pack(side=tk.TOP)
        

        self.process_button = tk.Button(self.root, text="Process Script", command=self.process_script)
        self.process_button.pack(fill=tk.X)

        self.save_button = tk.Button(self.root, text="Save Result", command=self.save_file)
        self.save_button.pack(fill=tk.X)
        
        # Pre-fill the script editor with the default script
        default_script = """def transform(text) :
    return text"""
        self.script_editor.insert(tk.END, default_script)  # Insert the default script

        self.process_script()        
        
        self.root.mainloop()
        
    def process_script(self):
        script_code = self.script_editor.get("1.0", tk.END)
        self.script_runner.update_transform(script_code)
        result = self.script_runner.transform(self.file_data)
        self.result_editor.delete("1.0", tk.END)
        self.result_editor.insert("1.0", result)

    def load_data_file(self):
        global file_data
        file_path = fd.askopenfilename(title="Select a file", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'r') as file:
                self.file_data = file.read()        

    def load_script_file(self):
        file_path = fd.askopenfilename(title="Select a script file", filetypes=[("Python files", "*.py"), ("Text files","*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'r') as file:
                script = file.read()
            self.script_editor.delete('1.0', tk.END)
            self.script_editor.insert(tk.END, script)


    def save_file(self):
        file_path = fd.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.result_editor.get("1.0", tk.END))
   
   
transeditor = None

def main() :
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
        try:
            with open(file_name, 'r') as file:
                transeditor=TransEdit(file.read())
        except IOError:
            print(f"Could not read file: {file_name}")
            sys.exit()
    else:
        transeditor=TransEdit()
        
     
if __name__ == '__main__' :
    main()



