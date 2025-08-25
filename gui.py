
import tkinter as tk
from tkinter import messagebox
from graph_model import Cell, create_graph_from_grid
from dfs_solver import find_path_recursive, dfs_iterative
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation

import numpy as np

class DFSVisualizer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("DFS Pathfinding Visualizer")
        self.geometry("800x600")

        self.grid_frame = tk.Frame(self)
        self.grid_frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.controls_frame = tk.Frame(self)
        self.controls_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.grid_frame)
        self.canvas.get_tk_widget().pack()

        self.create_controls()

    def create_controls(self):
        # Grid size
        tk.Label(self.controls_frame, text="Grid Size (rows, cols):").pack()
        self.grid_size_entry = tk.Entry(self.controls_frame)
        self.grid_size_entry.pack()
        self.grid_size_entry.insert(0, "10,10")

        # Start position
        tk.Label(self.controls_frame, text="Start Position (row, col):").pack()
        self.start_pos_entry = tk.Entry(self.controls_frame)
        self.start_pos_entry.pack()
        self.start_pos_entry.insert(0, "0,0")

        # Goal position
        tk.Label(self.controls_frame, text="Goal Position (row, col):").pack()
        self.goal_pos_entry = tk.Entry(self.controls_frame)
        self.goal_pos_entry.pack()
        self.goal_pos_entry.insert(0, "9,9")

        # Obstacles
        tk.Label(self.controls_frame, text="Obstacles (row,col;row,col;...):").pack()
        self.obstacles_entry = tk.Entry(self.controls_frame)
        self.obstacles_entry.pack()
        self.obstacles_entry.insert(0, "2,2;2,3;2,4;3,4;4,4;5,4;6,4;6,3;6,2;5,2")

        # Buttons
        self.generate_grid_button = tk.Button(self.controls_frame, text="Generate Grid", command=self.draw_grid)
        self.generate_grid_button.pack(pady=5)

        self.run_recursive_button = tk.Button(self.controls_frame, text="Run Recursive DFS", command=self.run_recursive_dfs)
        self.run_recursive_button.pack(pady=5)

        self.run_iterative_button = tk.Button(self.controls_frame, text="Run Iterative DFS", command=self.run_iterative_dfs)
        self.run_iterative_button.pack(pady=5)

        self.reset_button = tk.Button(self.controls_frame, text="Reset", command=self.reset)
        self.reset_button.pack(pady=5)

    def draw_grid(self):
        self.ax.clear()
        try:
            grid_size_str = self.grid_size_entry.get()
            self.rows, self.cols = map(int, grid_size_str.split(','))

            start_pos_str = self.start_pos_entry.get()
            self.start_pos = tuple(map(int, start_pos_str.split(',')))

            goal_pos_str = self.goal_pos_entry.get()
            self.goal_pos = tuple(map(int, goal_pos_str.split(',')))

            obstacles_str = self.obstacles_entry.get()
            self.obstacles = [tuple(map(int, o.split(','))) for o in obstacles_str.split(';')]

            self.ax.set_xticks(np.arange(0, self.cols, 1))
            self.ax.set_yticks(np.arange(0, self.rows, 1))
            self.ax.set_xticklabels([])
            self.ax.set_yticklabels([])
            self.ax.grid(True)

            for r in range(self.rows):
                for c in range(self.cols):
                    if (r, c) == self.start_pos:
                        self.ax.add_patch(plt.Rectangle((c, r), 1, 1, color='green'))
                    elif (r, c) == self.goal_pos:
                        self.ax.add_patch(plt.Rectangle((c, r), 1, 1, color='red'))
                    elif (r, c) in self.obstacles:
                        self.ax.add_patch(plt.Rectangle((c, r), 1, 1, color='black'))
            
            self.canvas.draw()
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please check your input values.")

    def run_recursive_dfs(self):
        try:
            self.draw_grid()
            self.graph = create_graph_from_grid((self.rows, self.cols), [Cell(r, c) for r, c in self.obstacles])
            start_node = Cell(self.start_pos[0], self.start_pos[1])
            goal_node = Cell(self.goal_pos[0], self.goal_pos[1])

            path = find_path_recursive(self.graph, start_node, goal_node)

            if path:
                self.animate_path(path)
            else:
                messagebox.showinfo("No Path", "No path found using Recursive DFS.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def run_iterative_dfs(self):
        try:
            self.draw_grid()
            self.graph = create_graph_from_grid((self.rows, self.cols), [Cell(r, c) for r, c in self.obstacles])
            start_node = Cell(self.start_pos[0], self.start_pos[1])
            goal_node = Cell(self.goal_pos[0], self.goal_pos[1])

            path = dfs_iterative(self.graph, start_node, goal_node)

            if path:
                self.animate_path(path)
            else:
                messagebox.showinfo("No Path", "No path found using Iterative DFS.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def animate_path(self, path):
        line, = self.ax.plot([], [], lw=2)

        def init():
            line.set_data([], [])
            return line,

        def update(frame):
            xdata = [cell.col + 0.5 for cell in path[:frame+1]]
            ydata = [cell.row + 0.5 for cell in path[:frame+1]]
            line.set_data(xdata, ydata)
            return line,

        ani = FuncAnimation(self.fig, update, frames=len(path), init_func=init, blit=True, repeat=False, interval=200)
        self.canvas.draw()

    def reset(self):
        self.ax.clear()
        self.canvas.draw()
        self.grid_size_entry.delete(0, tk.END)
        self.grid_size_entry.insert(0, "10,10")
        self.start_pos_entry.delete(0, tk.END)
        self.start_pos_entry.insert(0, "0,0")
        self.goal_pos_entry.delete(0, tk.END)
        self.goal_pos_entry.insert(0, "9,9")
        self.obstacles_entry.delete(0, tk.END)
        self.obstacles_entry.insert(0, "2,2;2,3;2,4;3,4;4,4;5,4;6,4;6,3;6,2;5,2")

if __name__ == "__main__":
    app = DFSVisualizer()
    app.mainloop()
