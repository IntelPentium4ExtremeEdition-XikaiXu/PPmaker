import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.animation as animation

class EgramPlotter:
    def __init__(self, parent_window=None):
        self.parent_window = parent_window
        self.data = None
        self.xpoints = None
        self.ypoints = None
        self.index = 0

    def load_csv(self):
        """Load egram data from a CSV file."""
        file_path = filedialog.askopenfilename(
            title="Select CSV File", filetypes=[("CSV files", "*.csv")]
        )
        if not file_path:
            messagebox.showerror("Error", "No file selected.")
            return False

        try:
            data = pd.read_csv(file_path)
            if "x" in data.columns and "y" in data.columns:
                self.xpoints = data["x"]
                self.ypoints = data["y"]
                self.data = data
                return True
            else:
                raise ValueError("CSV file must contain 'x' and 'y' columns.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load CSV: {e}")
            return False

    def plot_egram(self):
        """Plot the loaded egram data with animation."""
        if self.data is None:
            messagebox.showerror("Error", "No data to plot. Please load a CSV file first.")
            return

        # Create a new window for the plot
        plot_window = tk.Toplevel(self.parent_window)
        plot_window.title("Electrogram Plot")
        plot_window.geometry("800x600")

        # Create the figure
        figure = Figure(figsize=(5, 4), dpi=100)
        ax = figure.add_subplot(111)
        ax.set_xlabel("X-axis")
        ax.set_ylabel("Y-axis")
        ax.set_title("Electrogram Plot")
        ax.set_xlim(min(self.xpoints), max(self.xpoints))
        ax.set_ylim(min(self.ypoints), max(self.ypoints))

        # Line object to update
        line, = ax.plot([], [], 'bo-', linewidth=1)

        # Animation function
        def update(frame):
            line.set_data(self.xpoints[:frame], self.ypoints[:frame])
            return line,

        # Set up the animation
        ani = animation.FuncAnimation(
            figure, update, frames=len(self.xpoints), interval=100, blit=True
        )

        # Add the plot to the window
        canvas = FigureCanvasTkAgg(figure, plot_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def start(self):
        """Start the process of loading and plotting egram data."""
        if self.load_csv():
            self.plot_egram()