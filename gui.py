
import tkinter as tk
from tkinter import messagebox
from graph_model import Cell, create_graph_from_grid
from dfs_solver import find_path_recursive, dfs_iterative
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import numpy as np
import time
import tracemalloc

class DFSVisualizer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("DFS Pathfinding Visualizer")
        self.geometry("900x700")
        self.configure(bg="#2E2E2E")

        self.grid_frame = tk.Frame(self, bg="#2E2E2E")
        self.grid_frame.pack(side=tk.LEFT, padx=20, pady=20)

        self.controls_frame = tk.Frame(self, bg="#3C3C3C", padx=20, pady=20)
        self.controls_frame.pack(side=tk.RIGHT, fill="both", expand=True)

        self.fig, self.ax = plt.subplots(facecolor="#2E2E2E")
        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')
        self.ax.spines['bottom'].set_color('white')
        self.ax.spines['top'].set_color('white') 
        self.ax.spines['right'].set_color('white')
        self.ax.spines['left'].set_color('white')

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.grid_frame)
        self.canvas.get_tk_widget().pack()

        self.animation = None
        self.is_paused = False

        self.create_controls()

    def create_controls(self):
        control_font = ("Helvetica", 12)
        label_color = "white"
        entry_bg = "#555555"
        entry_fg = "white"
        button_bg = "#007BFF"
        button_fg = "white"

        # Grid size
        tk.Label(self.controls_frame, text="Grid Size (rows, cols):", font=control_font, bg="#3C3C3C", fg=label_color).pack(pady=(0, 5))
        self.grid_size_entry = tk.Entry(self.controls_frame, font=control_font, bg=entry_bg, fg=entry_fg, insertbackground=label_color)
        self.grid_size_entry.pack(pady=(0, 10), fill="x")
        self.grid_size_entry.insert(0, "10,10")

        # Start position
        tk.Label(self.controls_frame, text="Start Position (row, col):", font=control_font, bg="#3C3C3C", fg=label_color).pack(pady=(0, 5))
        self.start_pos_entry = tk.Entry(self.controls_frame, font=control_font, bg=entry_bg, fg=entry_fg, insertbackground=label_color)
        self.start_pos_entry.pack(pady=(0, 10), fill="x")
        self.start_pos_entry.insert(0, "0,0")

        # Goal position
        tk.Label(self.controls_frame, text="Goal Position (row, col):", font=control_font, bg="#3C3C3C", fg=label_color).pack(pady=(0, 5))
        self.goal_pos_entry = tk.Entry(self.controls_frame, font=control_font, bg=entry_bg, fg=entry_fg, insertbackground=label_color)
        self.goal_pos_entry.pack(pady=(0, 10), fill="x")
        self.goal_pos_entry.insert(0, "9,9")

        # Obstacles
        tk.Label(self.controls_frame, text="Obstacles (row,col;row,col;...):", font=control_font, bg="#3C3C3C", fg=label_color).pack(pady=(0, 5))
        self.obstacles_entry = tk.Entry(self.controls_frame, font=control_font, bg=entry_bg, fg=entry_fg, insertbackground=label_color)
        self.obstacles_entry.pack(pady=(0, 20), fill="x")
        self.obstacles_entry.insert(0, "2,2;2,3;2,4;3,4;4,4;5,4;6,4;6,3;6,2;5,2")

        # Buttons
        self.generate_grid_button = tk.Button(self.controls_frame, text="Generate Grid", font=control_font, bg=button_bg, fg=button_fg, command=self.draw_grid, relief="flat", borderwidth=0)
        self.generate_grid_button.pack(pady=5, fill="x")

        self.run_recursive_button = tk.Button(self.controls_frame, text="Run Recursive DFS", font=control_font, bg=button_bg, fg=button_fg, command=self.run_recursive_dfs, relief="flat", borderwidth=0)
        self.run_recursive_button.pack(pady=5, fill="x")

        self.run_iterative_button = tk.Button(self.controls_frame, text="Run Iterative DFS", font=control_font, bg=button_bg, fg=button_fg, command=self.run_iterative_dfs, relief="flat", borderwidth=0)
        self.run_iterative_button.pack(pady=5, fill="x")

        # Animation Controls
        animation_controls_frame = tk.Frame(self.controls_frame, bg="#3C3C3C")
        animation_controls_frame.pack(pady=10, fill="x")

        self.play_pause_button = tk.Button(animation_controls_frame, text="Play/Pause", font=control_font, bg=button_bg, fg=button_fg, command=self.toggle_pause, relief="flat", borderwidth=0)
        self.play_pause_button.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self.speed_slider = tk.Scale(animation_controls_frame, from_=10, to=200, orient="horizontal", label="Speed (ms)", font=control_font, bg="#3C3C3C", fg=label_color, troughcolor="#555555", highlightbackground="#3C3C3C", command=self.update_speed)
        self.speed_slider.set(50)
        self.speed_slider.pack(side="right", fill="x", expand=True, padx=(5, 0))


        self.reset_button = tk.Button(self.controls_frame, text="Reset", font=control_font, bg="#555555", fg=button_fg, command=self.reset, relief="flat", borderwidth=0)
        self.reset_button.pack(pady=15, fill="x")

        # Performance Labels
        self.time_label = tk.Label(self.controls_frame, text="Execution Time: ", font=control_font, bg="#3C3C3C", fg=label_color)
        self.time_label.pack(pady=5)
        self.memory_label = tk.Label(self.controls_frame, text="Memory Usage: ", font=control_font, bg="#3C3C3C", fg=label_color)
        self.memory_label.pack(pady=5)

    def draw_grid(self):
        if self.animation and self.animation.event_source:
            self.animation.event_source.stop()
            self.animation = None
        self.ax.clear()
        self.ax.set_facecolor("#2E2E2E")
        try:
            # Grid size validation
            grid_size_str = self.grid_size_entry.get()
            if not grid_size_str or len(grid_size_str.split(',')) != 2:
                messagebox.showerror("Error", "Invalid Grid Size format. Use 'rows,cols'.")
                return
            self.rows, self.cols = map(int, grid_size_str.split(','))

            # Start position validation
            start_pos_str = self.start_pos_entry.get()
            if not start_pos_str or len(start_pos_str.split(',')) != 2:
                messagebox.showerror("Error", "Invalid Start Position format. Use 'row,col'.")
                return
            self.start_pos = tuple(map(int, start_pos_str.split(',')))

            # Goal position validation
            goal_pos_str = self.goal_pos_entry.get()
            if not goal_pos_str or len(goal_pos_str.split(',')) != 2:
                messagebox.showerror("Error", "Invalid Goal Position format. Use 'row,col'.")
                return
            self.goal_pos = tuple(map(int, goal_pos_str.split(',')))

            # Obstacles validation
            obstacles_str = self.obstacles_entry.get()
            if obstacles_str:
                try:
                    self.obstacles = [tuple(map(int, o.split(','))) for o in obstacles_str.split(';') if o]
                except ValueError:
                    messagebox.showerror("Error", "Invalid Obstacles format. Use 'row,col;row,col;...'.")
                    return
            else:
                self.obstacles = []

            self.ax.set_xticks(np.arange(-.5, self.cols, 1), minor=True)
            self.ax.set_yticks(np.arange(-.5, self.rows, 1), minor=True)
            self.ax.set_xticklabels([])
            self.ax.set_yticklabels([])
            self.ax.grid(which='minor', color='#4A4A4A')

            for r in range(self.rows):
                for c in range(self.cols):
                    if (r, c) == self.start_pos:
                        self.ax.add_patch(plt.Rectangle((c - 0.5, r - 0.5), 1, 1, color='#28a745', ec='#2E2E2E'))
                    elif (r, c) == self.goal_pos:
                        self.ax.add_patch(plt.Rectangle((c - 0.5, r - 0.5), 1, 1, color='#dc3545', ec='#2E2E2E'))
                    elif (r, c) in self.obstacles:
                        self.ax.add_patch(plt.Rectangle((c - 0.5, r - 0.5), 1, 1, color='#6c757d', ec='#2E2E2E'))
                    else:
                        self.ax.add_patch(plt.Rectangle((c - 0.5, r - 0.5), 1, 1, color='#3C3C3C', ec='#4A4A4A'))
            
            self.ax.set_xlim(-0.5, self.cols - 0.5)
            self.ax.set_ylim(-0.5, self.rows - 0.5)
            self.ax.invert_yaxis()
            self.canvas.draw()
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please ensure all values are integers.")

    def run_recursive_dfs(self):
        try:
            self.draw_grid()
            self.graph = create_graph_from_grid((self.rows, self.cols), [Cell(r, c) for r, c in self.obstacles])
            start_node = Cell(self.start_pos[0], self.start_pos[1])
            goal_node = Cell(self.goal_pos[0], self.goal_pos[1])

            tracemalloc.start()
            start_time = time.time()
            path, history, _ = find_path_recursive(self.graph, start_node, goal_node)
            end_time = time.time()
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            self.time_label.config(text=f"Execution Time: {end_time - start_time:.4f}s")
            self.memory_label.config(text=f"Memory Usage: {peak / 1024:.2f} KB")

            self.animate_search(history, path)
            if not path:
                messagebox.showinfo("No Path", "No path found using Recursive DFS.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def run_iterative_dfs(self):
        try:
            self.draw_grid()
            self.graph = create_graph_from_grid((self.rows, self.cols), [Cell(r, c) for r, c in self.obstacles])
            start_node = Cell(self.start_pos[0], self.start_pos[1])
            goal_node = Cell(self.goal_pos[0], self.goal_pos[1])

            tracemalloc.start()
            start_time = time.time()
            path, history = dfs_iterative(self.graph, start_node, goal_node)
            end_time = time.time()
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            self.time_label.config(text=f"Execution Time: {end_time - start_time:.4f}s")
            self.memory_label.config(text=f"Memory Usage: {peak / 1024:.2f} KB")

            self.animate_search(history, path)
            if not path:
                messagebox.showinfo("No Path", "No path found using Iterative DFS.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def animate_search(self, history, path):
        if not history:
            return

        if self.animation and self.animation.event_source:
            self.animation.event_source.stop()
            self.animation = None

        self.is_paused = False
        self.play_pause_button.config(text="Pause")

        visited_patches = {}
        
        def update(frame):
            node = history[frame]
            r, c = node.row, node.col
            
            if (r, c) not in [(self.start_pos), (self.goal_pos)]:
                if (r,c) not in visited_patches:
                    patch = plt.Rectangle((c - 0.5, r - 0.5), 1, 1, color='#17a2b8', ec='#2E2E2E')
                    self.ax.add_patch(patch)
                    visited_patches[(r,c)] = patch
                else:
                    visited_patches[(r,c)].set_color('#17a2b8')


            if frame == len(history) - 1 and path:
                for i in range(len(path) - 1):
                    start_cell = path[i]
                    end_cell = path[i+1]
                    self.ax.plot([start_cell.col, end_cell.col], [start_cell.row, end_cell.row], color='#007BFF', linewidth=3)

            self.canvas.draw()

        self.animation = FuncAnimation(self.fig, update, frames=len(history), repeat=False, interval=self.speed_slider.get())
        self.canvas.draw()

    def toggle_pause(self):
        if not self.animation:
            return
        if self.is_paused:
            self.animation.resume()
            self.play_pause_button.config(text="Pause")
        else:
            self.animation.pause()
            self.play_pause_button.config(text="Play")
        self.is_paused = not self.is_paused

    def update_speed(self, val):
        if self.animation and self.animation.event_source:
            self.animation.event_source.interval = int(val)

    def reset(self):
        if self.animation and self.animation.event_source:
            self.animation.event_source.stop()
            self.animation = None
        self.ax.clear()
        self.ax.set_facecolor("#2E2E2E")
        self.canvas.draw()
        self.grid_size_entry.delete(0, tk.END)
        self.grid_size_entry.insert(0, "10,10")
        self.start_pos_entry.delete(0, tk.END)
        self.start_pos_entry.insert(0, "0,0")
        self.goal_pos_entry.delete(0, tk.END)
        self.goal_pos_entry.insert(0, "9,9")
        self.obstacles_entry.delete(0, tk.END)
        self.obstacles_entry.insert(0, "2,2;2,3;2,4;3,4;4,4;5,4;6,4;6,3;6,2;5,2")
        self.time_label.config(text="Execution Time: ")
        self.memory_label.config(text="Memory Usage: ")
        self.play_pause_button.config(text="Play/Pause")
        self.speed_slider.set(50)

if __name__ == "__main__":
    app = DFSVisualizer()
    app.mainloop()
