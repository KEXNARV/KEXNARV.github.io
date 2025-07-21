import tkinter as tk
from tkinter import messagebox
from run_analysis import generate_html


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Ingresar datos ANOVA")
        self.rows = []
        self.table = tk.Frame(root)
        self.table.pack(padx=10, pady=10)
        header = tk.Frame(self.table)
        header.pack()
        tk.Label(header, text="Tratamiento", width=12).pack(side=tk.LEFT)
        tk.Label(header, text="Observaciones (separadas por comas)", width=40).pack(side=tk.LEFT)
        for _ in range(4):
            self.add_row()
        btns = tk.Frame(root)
        btns.pack(pady=5)
        tk.Button(btns, text="Agregar tratamiento", command=self.add_row).pack(side=tk.LEFT, padx=5)
        tk.Button(btns, text="Generar resultados", command=self.generate).pack(side=tk.LEFT, padx=5)

    def add_row(self):
        row_frame = tk.Frame(self.table)
        row_frame.pack(pady=2)
        name_var = tk.StringVar()
        values_var = tk.StringVar()
        tk.Entry(row_frame, textvariable=name_var, width=12).pack(side=tk.LEFT, padx=2)
        tk.Entry(row_frame, textvariable=values_var, width=40).pack(side=tk.LEFT, padx=2)
        self.rows.append((name_var, values_var))

    def generate(self):
        groups = {}
        for name_var, values_var in self.rows:
            name = name_var.get().strip()
            values_text = values_var.get().strip()
            if not name or not values_text:
                continue
            try:
                values = [float(v) for v in values_text.split(',') if v.strip()]
            except ValueError:
                messagebox.showerror("Error", f"Datos inválidos para {name}")
                return
            groups[name] = values
        if not groups:
            messagebox.showerror("Error", "No se ingresaron datos")
            return
        html = generate_html(groups)
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html)
        messagebox.showinfo("Éxito", "Archivo index.html generado con los resultados")


def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
