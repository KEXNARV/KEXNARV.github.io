import tkinter as tk
from tkinter import messagebox
from run_analysis import format_text


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Ingresar datos ANOVA")
        self.rows = 4
        self.cols = 4
        self.header_vars = []
        self.cell_vars = []
        self.table = tk.Frame(root)
        self.table.pack(padx=10, pady=10)
        self.draw_table()
        self.control_panel()

    def draw_table(self):
        # Header row
        for c in range(self.cols):
            var = tk.StringVar(value=f"T{c+1}")
            entry = tk.Entry(self.table, textvariable=var, width=10)
            entry.grid(row=0, column=c, padx=2, pady=2)
            self.header_vars.append(var)
        # Data cells
        for r in range(self.rows):
            row_vars = []
            for c in range(self.cols):
                var = tk.StringVar()
                e = tk.Entry(self.table, textvariable=var, width=8)
                e.grid(row=r+1, column=c, padx=2, pady=2)
                row_vars.append(var)
            self.cell_vars.append(row_vars)

    def control_panel(self):
        panel = tk.Frame(self.root)
        panel.pack(pady=5)
        tk.Button(panel, text="Añadir fila", command=self.add_row).grid(row=0, column=0, padx=2)
        tk.Button(panel, text="Eliminar fila", command=self.del_row).grid(row=0, column=1, padx=2)
        tk.Button(panel, text="Añadir columna", command=self.add_col).grid(row=0, column=2, padx=2)
        tk.Button(panel, text="Eliminar columna", command=self.del_col).grid(row=0, column=3, padx=2)
        tk.Button(panel, text="Mostrar resultados", command=self.generate).grid(row=0, column=4, padx=10)

    def add_row(self):
        row_vars = []
        for c in range(self.cols):
            var = tk.StringVar()
            e = tk.Entry(self.table, textvariable=var, width=8)
            e.grid(row=self.rows+1, column=c, padx=2, pady=2)
            row_vars.append(var)
        self.cell_vars.append(row_vars)
        self.rows += 1

    def del_row(self):
        if self.rows <= 1:
            return
        for c in range(self.cols):
            widget = self.table.grid_slaves(row=self.rows, column=c)[0]
            widget.destroy()
        self.cell_vars.pop()
        self.rows -= 1

    def add_col(self):
        var = tk.StringVar(value=f"T{self.cols+1}")
        entry = tk.Entry(self.table, textvariable=var, width=10)
        entry.grid(row=0, column=self.cols, padx=2, pady=2)
        self.header_vars.append(var)
        for r in range(self.rows):
            varc = tk.StringVar()
            e = tk.Entry(self.table, textvariable=varc, width=8)
            e.grid(row=r+1, column=self.cols, padx=2, pady=2)
            self.cell_vars[r].append(varc)
        self.cols += 1

    def del_col(self):
        if self.cols <= 1:
            return
        for r in range(self.rows+1):
            widget = self.table.grid_slaves(row=r, column=self.cols-1)[0]
            widget.destroy()
        self.header_vars.pop()
        for r in range(self.rows):
            self.cell_vars[r].pop()
        self.cols -= 1

    def collect_data(self):
        groups = {}
        for c in range(self.cols):
            name = self.header_vars[c].get().strip() or f"T{c+1}"
            values = []
            for r in range(self.rows):
                txt = self.cell_vars[r][c].get().strip()
                if txt:
                    try:
                        values.append(float(txt))
                    except ValueError:
                        messagebox.showerror("Error", f"Valor inválido en fila {r+1}, columna {c+1}")
                        return None
            if values:
                groups[name] = values
        return groups

    def generate(self):
        groups = self.collect_data()
        if not groups:
            messagebox.showerror("Error", "No se ingresaron datos válidos")
            return
        try:
            report = format_text(groups)
        except Exception as exc:
            messagebox.showerror("Error", str(exc))
            return
        self.show_report(report)

    def show_report(self, text):
        win = tk.Toplevel(self.root)
        win.title("Resultados")
        txt = tk.Text(win, width=100, height=30)
        txt.pack(padx=10, pady=10)
        txt.insert("1.0", text)
        txt.config(state="disabled")


def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
