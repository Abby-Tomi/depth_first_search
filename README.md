# DFS Pathfinding Visualizer

This project is a Python application that visualizes the Depth-First Search (DFS) algorithm for finding a path in a grid. It provides a graphical user interface (GUI) to configure the grid, run the DFS algorithm (both recursive and iterative implementations), and visualize the search process in real-time.

## Features

*   **Interactive Grid Configuration:** Set the grid size, define start and goal positions, and add obstacles.
*   **Dual DFS Implementations:** Choose between recursive and iterative DFS algorithms.
*   **Real-time Visualization:** Watch the DFS algorithm explore the grid with animations.
*   **Path Highlighting:** The final path from start to goal is highlighted.
*   **Performance Metrics:** Compare the execution time and memory usage of both DFS implementations.
*   **Animation Controls:** Play, pause, and control the speed of the visualization.
*   **Reset Functionality:** Easily reset the grid to the default configuration.

## Technologies Used

*   **Python:** The core programming language.
*   **Tkinter:** For the graphical user interface (GUI).
*   **Matplotlib:** For creating the grid and animating the search process.
*   **NumPy:** For numerical operations.

## Getting Started

### Prerequisites

*   Python 3.x
*   Tkinter
*   Matplotlib
*   NumPy

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/your-username/your-repository-name.git
    ```
2.  Navigate to the project directory:
    ```bash
    cd your-repository-name
    ```
3.  Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

To run the application, execute the `main.py` script:

```bash
python main.py
```

## File Structure

```
.
├── main.py               # Main entry point of the application
├── gui.py                # GUI implementation using Tkinter and Matplotlib
├── dfs_solver.py         # Recursive and iterative DFS implementations
├── graph_model.py        # Graph representation of the grid
├── test_dfs_solver.py    # Unit tests for the DFS solver
├── analysis.py           # Performance analysis script
├── .gitignore            # Git ignore file
├── README.md             # This file
└── ...
```

## Running Tests

To run the unit tests, execute the `test_dfs_solver.py` script:

```bash
python test_dfs_solver.py
```
