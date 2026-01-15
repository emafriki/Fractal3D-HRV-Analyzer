# -*- coding: utf-8 -*-
"""
FractalApp - Sierpinski Triangle (2D) & Tetrahedron (3D)
Author: Alma 💙
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import imageio, os


class FractalApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Fractal Generator - Sierpinski Triangle & Tetrahedron")
        self.root.geometry("1150x720")

        # ====== Layout principal ======
        main = tk.Frame(self.root)
        main.pack(fill=tk.BOTH, expand=True)

        # ====== Panel lateral ======
        side = tk.Frame(main, width=250, padx=10, pady=10, bg="#f0f0f0")
        side.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(side, text="Fractal Options", font=("Arial", 13, "bold"), bg="#f0f0f0").pack(pady=(0,10))

        # Archivo
        tk.Label(side, text="Data File:", bg="#f0f0f0").pack(anchor="w")
        self.entry_file = tk.Entry(side, width=30)
        self.entry_file.pack()
        tk.Button(side, text="Browse", command=self.browse_file, width=20).pack(pady=5)

        # ---- Botones de fractales ----
        tk.Label(side, text="\nSierpinski Triangle (2D):", font=("Arial", 11, "bold"), bg="#f0f0f0").pack(anchor="w", pady=(10,0))
        tk.Button(side, text="Generate Triangle (Control)", command=lambda: self.generate_triangle("controls"), width=25).pack(pady=2)
        tk.Button(side, text="Generate Triangle (Patient)", command=lambda: self.generate_triangle("patients"), width=25).pack(pady=2)
        tk.Button(side, text="Generate Triangle (Random)", command=lambda: self.generate_triangle("random"), width=25).pack(pady=2)

        tk.Label(side, text="\nSierpinski Tetrahedron (3D):", font=("Arial", 11, "bold"), bg="#f0f0f0").pack(anchor="w", pady=(10,0))
        tk.Button(side, text="Generate Tetrahedron (Control)", command=lambda: self.generate_tetrahedron("controls"), width=25).pack(pady=2)
        tk.Button(side, text="Generate Tetrahedron (Patient)", command=lambda: self.generate_tetrahedron("patients"), width=25).pack(pady=2)
        tk.Button(side, text="Generate Tetrahedron (Random)", command=lambda: self.generate_tetrahedron("random"), width=25).pack(pady=2)

        # Guardar
        tk.Label(side, text="\nSave:", bg="#f0f0f0").pack(anchor="w", pady=(15,0))
        tk.Button(side, text="Save Image (2D)", command=self.save_image, width=20).pack(pady=3)
        tk.Button(side, text="Save GIF (3D)", command=self.save_gif, width=20).pack(pady=3)

        # Dimensión fractal
        tk.Label(side, text="\nFractal Dimension:", bg="#f0f0f0").pack(anchor="w", pady=(10,0))
        self.dim_label = tk.Label(side, text="-", bg="#f0f0f0", font=("Arial", 11, "bold"), fg="darkblue")
        self.dim_label.pack(anchor="w")

        # Instrucciones
        tk.Label(side, text="\nNotes:\n- Load a single-column data file.\n- Triangle uses 3 labels.\n- Tetrahedron uses 4 labels.\n- Random assigns random labels.",
                 justify="left", bg="#f0f0f0").pack(anchor="w", pady=(15,0))

        # ====== Panel de gráfica ======
        self.frame_plot = tk.Frame(main)
        self.frame_plot.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.fig = plt.Figure(figsize=(8,7), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_plot)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Variables
        self.points = None
        self.fractal = None

    # ---------------- Archivo ----------------
    def browse_file(self):
        fp = filedialog.askopenfilename(filetypes=[("Text or CSV", "*.txt;*.csv;*.dat"), ("All", "*.*")])
        if fp:
            self.entry_file.delete(0, tk.END)
            self.entry_file.insert(0, fp)
            try:
                self.points = self._read_column(fp)
                messagebox.showinfo("File Loaded", f"{len(self.points)} values loaded successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Could not load file:\n{e}")

    def _read_column(self, filepath):
        try:
            y = pd.read_csv(filepath, sep="\t", header=None, engine="python").values.squeeze()
        except Exception:
            try:
                y = pd.read_csv(filepath, header=None).values.squeeze()
            except Exception:
                y = np.loadtxt(filepath)
        return np.asarray(y).reshape(-1)

    # ---------------- TRIÁNGULO ----------------
    def generate_triangle(self, mode):
        if self.points is None:
            messagebox.showerror("Error", "Please load a data file first.")
            return

        Y = self.points
        p = len(Y)
        if p < 3:
            messagebox.showerror("Error", "Need at least 3 values.")
            return

        arr = np.column_stack((Y, np.zeros(p)))

        if mode == "random":
            np.random.shuffle(arr)
            arr[:,1] = np.random.randint(1, 4, size=p)
        else:
            idx = np.argsort(arr[:,0])
            Y2 = arr[idx]
            t = p // 3
            Y2[:t,1]=1; Y2[t:2*t,1]=2; Y2[2*t:,1]=3
            arr = Y2[np.argsort(idx)]

        # Vértices del triángulo
        p1 = np.array([0,0])
        p2 = np.array([1,0])
        p3 = np.array([0.5,1])
        current = np.array([0.5,0.5])
        pts = np.zeros((p,2))

        for f in range(p):
            lab = int(arr[f,1])
            if lab==1: current=(current+p1)/2
            elif lab==2: current=(current+p2)/2
            else: current=(current+p3)/2
            pts[f,:]=current

        # Color
        color = self._color_by_mode(mode)

        # Plot
        self.fig.clf()
        ax = self.fig.add_subplot(111)
        ax.plot(pts[:,0], pts[:,1], '.', markersize=1, color=color)
        ax.set_title(f"Sierpinski Triangle (2D) — {mode.capitalize()}")
        ax.axis("off")
        ax.set_aspect("equal")
        self.ax = ax
        self.canvas.draw()

        self.fractal = pts
        D = self._box_counting_2d(pts)
        self.dim_label.config(text=f"{D:.4f}")

    # ---------------- TETRAEDRO ----------------
    def generate_tetrahedron(self, mode):
        if self.points is None:
            messagebox.showerror("Error", "Please load a data file first.")
            return

        Y = self.points
        p = len(Y)
        if p < 4:
            messagebox.showerror("Error", "Need at least 4 values.")
            return

        arr = np.column_stack((Y, np.zeros(p)))

        if mode == "random":
            arr[:,1] = np.random.randint(1, 5, size=p)
        else:
            idx = np.argsort(arr[:,0])
            Y2 = arr[idx]
            t = p // 4
            Y2[:t,1]=1; Y2[t:2*t,1]=2; Y2[2*t:3*t,1]=3; Y2[3*t:,1]=4
            arr = Y2[np.argsort(idx)]

        verts = np.array([
            [0,0,0],
            [1,0,0],
            [0.5,np.sqrt(3)/2,0],
            [0.5,np.sqrt(3)/6,np.sqrt(6)/3]
        ])
        current = np.array([0.5,np.sqrt(3)/6,np.sqrt(6)/12])
        pts = np.zeros((p,3))
        for f in range(p):
            v = verts[int(arr[f,1])-1]
            current = (current+v)/2
            pts[f,:]=current

        color = self._color_by_mode(mode)

        self.fig.clf()
        ax = self.fig.add_subplot(111, projection="3d")
        ax.scatter(pts[:,0], pts[:,1], pts[:,2], s=0.5, c=color)
        ax.set_title(f"Sierpinski Tetrahedron (3D) — {mode.capitalize()}")
        ax.axis("off")
        ax.set_box_aspect([1,1,1])
        self.ax = ax
        self.canvas.draw()

        self.fractal = pts
        D = self._box_counting_3d(pts)
        self.dim_label.config(text=f"{D:.4f}")

    # ---------------- CÁLCULOS ----------------
    def _color_by_mode(self, mode):
        if mode == "patients": return "red"
        if mode == "controls": return "blue"
        return "green"

    def _box_counting_2d(self, pts):
        P = (pts - pts.min(0)) / (pts.max(0)-pts.min(0))
        sizes = np.logspace(-3, 0, 10)
        counts = []
        for s in sizes:
            idx = np.floor(P/s).astype(int)
            counts.append(len(np.unique(idx[:,0]*1000+idx[:,1])))
        D = np.polyfit(np.log(1/sizes), np.log(counts), 1)[0]
        return D

    def _box_counting_3d(self, pts):
        P = (pts - pts.min(0)) / (pts.max(0)-pts.min(0))
        eps = np.logspace(np.log10(0.005), np.log10(0.3), 10)
        N = []
        for e in eps:
            idx = np.floor(P/e).astype(int)
            N.append(len(np.unique(idx[:,0]*1e6+idx[:,1]*1e3+idx[:,2])))
        D = np.polyfit(np.log(1/eps), np.log(N), 1)[0]
        return D

    # ---------------- GUARDADO ----------------
    def save_image(self):
        if self.fractal is None:
            messagebox.showerror("Error", "No fractal generated.")
            return
        fp = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG","*.png")])
        if fp:
            self.fig.savefig(fp, dpi=300)
            messagebox.showinfo("Saved", f"Image saved: {fp}")

    def save_gif(self):
        if self.fractal is None:
            messagebox.showerror("Error", "No fractal generated.")
            return
        fp = filedialog.asksaveasfilename(defaultextension=".gif", filetypes=[("GIF","*.gif")])
        if not fp: return

        out_dir = os.path.splitext(fp)[0] + "_frames"
        os.makedirs(out_dir, exist_ok=True)
        frames = []

        for i, ang in enumerate(range(0,360,5)):
            self.ax.view_init(30, ang)
            self.fig.canvas.draw()
            buf, size = self.fig.canvas.print_to_buffer()
            img = np.frombuffer(buf, dtype=np.uint8).reshape(size[1], size[0], 4)
            img = img[:,:,:3]
            frames.append(img)
            plt.imsave(os.path.join(out_dir, f"frame_{i:03d}.png"), img)

        imageio.mimsave(fp, frames, fps=15)
        messagebox.showinfo("Saved", f"GIF saved: {fp}\nFrames stored in:\n{out_dir}")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = FractalApp()
    app.run()
