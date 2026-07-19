import tkinter as tk
from tkinter import messagebox
import math

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora")
        self.root.geometry("360x520")
        self.root.configure(bg="#1e1e2e")
        self.root.resizable(True, True)
        self.root.minsize(300, 450)

        # Style colors (Catppuccin Mocha theme)
        self.bg_color = "#1e1e2e"
        self.display_bg = "#181825"
        self.text_color = "#cdd6f4"
        self.text_secondary = "#a6adc8"
        self.btn_bg_num = "#313244"
        self.btn_bg_op = "#45475a"
        self.btn_bg_accent = "#f38ba8"  # Clear / Reset
        self.btn_bg_equal = "#89b4fa"   # Equal
        self.btn_hover = "#585b70"
        self.btn_equal_hover = "#b4befe"

        # State variables
        self.equation_text = ""
        self.result_shown = False

        self.create_widgets()
        self.bind_keys()

    def create_widgets(self):
        # Configure grid row/column weights for responsiveness
        self.root.rowconfigure(0, weight=2)
        self.root.rowconfigure(1, weight=5)
        self.root.columnconfigure(0, weight=1)

        # Display Frame
        display_frame = tk.Frame(self.root, bg=self.display_bg, bd=0, highlightthickness=0)
        display_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        display_frame.columnconfigure(0, weight=1)
        display_frame.rowconfigure(0, weight=1)
        display_frame.rowconfigure(1, weight=1)

        # Equation Label (History/Expression)
        self.equation_label = tk.Label(
            display_frame, 
            text="", 
            anchor="e", 
            bg=self.display_bg, 
            fg=self.text_secondary, 
            font=("Consolas", 14),
            padx=15
        )
        self.equation_label.grid(row=0, column=0, sticky="nsew")

        # Current Input Label
        self.display_label = tk.Label(
            display_frame, 
            text="0", 
            anchor="e", 
            bg=self.display_bg, 
            fg=self.text_color, 
            font=("Consolas", 28, "bold"),
            padx=15
        )
        self.display_label.grid(row=1, column=0, sticky="nsew")

        # Buttons Frame
        btn_frame = tk.Frame(self.root, bg=self.bg_color)
        btn_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

        # Grid weights for buttons
        for r in range(5):
            btn_frame.rowconfigure(r, weight=1)
        for c in range(4):
            btn_frame.columnconfigure(c, weight=1)

        # Button definitions (Text, row, col, columnspan, type)
        buttons = [
            ("C", 0, 0, 1, 'clear'), ("√", 0, 1, 1, 'op'), ("x²", 0, 2, 1, 'op'), ("/", 0, 3, 1, 'op'),
            ("7", 1, 0, 1, 'num'),   ("8", 1, 1, 1, 'num'),  ("9", 1, 2, 1, 'num'),   ("*", 1, 3, 1, 'op'),
            ("4", 2, 0, 1, 'num'),   ("5", 2, 1, 1, 'num'),  ("6", 2, 2, 1, 'num'),   ("-", 2, 3, 1, 'op'),
            ("1", 3, 0, 1, 'num'),   ("2", 3, 1, 1, 'num'),  ("3", 3, 2, 1, 'num'),   ("+", 3, 3, 1, 'op'),
            ("+/-", 4, 0, 1, 'op'),  ("0", 4, 1, 1, 'num'),  (".", 4, 2, 1, 'num'),   ("=", 4, 3, 1, 'equal')
        ]

        self.btn_objects = {}
        for (text, row, col, col_span, btn_type) in buttons:
            # Color assignment
            if btn_type == 'num':
                bg = self.btn_bg_num
                fg = self.text_color
                hover_bg = self.btn_hover
            elif btn_type == 'op':
                bg = self.btn_bg_op
                fg = self.text_color
                hover_bg = self.btn_hover
            elif btn_type == 'clear':
                bg = self.btn_bg_accent
                fg = self.bg_color
                hover_bg = "#f38ba8" 
            elif btn_type == 'equal':
                bg = self.btn_bg_equal
                fg = self.bg_color
                hover_bg = self.btn_equal_hover

            btn = tk.Button(
                btn_frame, 
                text=text, 
                bg=bg, 
                fg=fg, 
                font=("Consolas", 18, "bold"),
                bd=0, 
                relief="flat",
                activebackground=hover_bg,
                activeforeground=fg if btn_type not in ['clear', 'equal'] else self.bg_color,
                command=lambda t=text: self.on_button_click(t)
            )
            btn.grid(row=row, column=col, columnspan=col_span, sticky="nsew", padx=3, pady=3)
            
            # Bind hover animations
            btn.bind("<Enter>", lambda e, b=btn, h=hover_bg: b.configure(bg=h))
            btn.bind("<Leave>", lambda e, b=btn, orig=bg: b.configure(bg=orig))
            
            self.btn_objects[text] = btn

    def bind_keys(self):
        # Keyboard support
        self.root.bind("<Key>", self.on_key_press)
        self.root.bind("<Return>", lambda e: self.on_button_click("="))
        self.root.bind("<BackSpace>", lambda e: self.on_button_click("⌫"))
        self.root.bind("<Escape>", lambda e: self.on_button_click("C"))

    def on_key_press(self, event):
        char = event.char
        if char in "0123456789.+-*/":
            self.on_button_click(char)

    def update_display(self, text):
        if len(text) > 14:
            self.display_label.configure(font=("Consolas", 18, "bold"))
        else:
            self.display_label.configure(font=("Consolas", 28, "bold"))
        self.display_label.configure(text=text)

    def on_button_click(self, char):
        current_display = self.display_label.cget("text")

        if self.result_shown and char not in "+-*/=√x²":
            self.equation_text = ""
            current_display = "0"
            self.equation_label.configure(text="")
            self.result_shown = False

        if char == "C":
            self.equation_text = ""
            self.update_display("0")
            self.equation_label.configure(text="")
            self.result_shown = False

        elif char == "⌫":
            if self.result_shown:
                self.equation_label.configure(text="")
                self.result_shown = False
            else:
                new_text = current_display[:-1]
                if new_text == "" or new_text == "-":
                    new_text = "0"
                self.update_display(new_text)

        elif char == "+/-":
            if current_display != "0":
                if current_display.startswith("-"):
                    self.update_display(current_display[1:])
                else:
                    self.update_display("-" + current_display)

        elif char in "0123456789":
            if current_display == "0":
                self.update_display(char)
            else:
                self.update_display(current_display + char)

        elif char == ".":
            if "." not in current_display:
                self.update_display(current_display + ".")

        elif char in "+-*/":
            self.equation_text = current_display + " " + char + " "
            self.equation_label.configure(text=self.equation_text)
            self.update_display("0")
            self.result_shown = False

        elif char == "√":
            try:
                val = float(current_display)
                if val < 0:
                    raise ValueError
                res = math.sqrt(val)
                if res.is_integer():
                    res = int(res)
                self.equation_label.configure(text=f"√({current_display})")
                self.update_display(str(res))
                self.result_shown = True
            except ValueError:
                self.update_display("Error")
                self.result_shown = True

        elif char == "x²":
            try:
                val = float(current_display)
                res = val ** 2
                if res.is_integer() and res < 1e15:
                    res = int(res)
                self.equation_label.configure(text=f"({current_display})²")
                self.update_display(str(res))
                self.result_shown = True
            except Exception:
                self.update_display("Error")
                self.result_shown = True

        elif char == "=":
            if not self.equation_text:
                return

            full_expression = self.equation_text + current_display
            try:
                eval_expr = full_expression.replace(" ", "")
                if any(c not in "0123456789.+-*/()" for c in eval_expr):
                    raise ValueError("Invalid expression")
                
                result = eval(eval_expr)
                
                if isinstance(result, float) and result.is_integer():
                    result = int(result)
                
                res_str = str(result)
                if len(res_str) > 16:
                    res_str = f"{result:.8g}"
                
                self.equation_label.configure(text=full_expression + " =")
                self.update_display(res_str)
                self.equation_text = ""
                self.result_shown = True
            except ZeroDivisionError:
                self.update_display("Error: Div/0")
                self.result_shown = True
            except Exception:
                self.update_display("Error")
                self.result_shown = True

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()
