# Importing necessary modules
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import RadioButtons

# Defining the Koch curve iterator
class KochCurveIterator:
    def __init__(self, x1, y1, x2, y2, iterations):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.iterations = iterations
        self.points = [[x1, y1]]
        self._generate_curve(self.x1, self.y1, self.x2, self.y2, self.iterations, self.points)
    
    def _generate_curve(self, x1, y1, x2, y2, iterations, points):
        if iterations == 0:  # Base case to stop recursion
            points.append([x2, y2])
            return

        dx = x2 - x1
        dy = y2 - y1

        x3 = x1 + dx / 3.0
        y3 = y1 + dy / 3.0

        x4 = x1 + 2 * dx / 3.0
        y4 = y1 + 2 * dy / 3.0

        angle = np.pi / 3.0
        x5 = x3 + (x4 - x3) * np.cos(angle) - (y4 - y3) * np.sin(angle)
        y5 = y3 + (x4 - x3) * np.sin(angle) + (y4 - y3) * np.cos(angle)

        self._generate_curve(x1, y1, x3, y3, iterations-1, points)
        self._generate_curve(x3, y3, x5, y5, iterations-1, points)
        self._generate_curve(x5, y5, x4, y4, iterations-1, points)
        self._generate_curve(x4, y4, x2, y2, iterations-1, points)
    
    def __iter__(self):
        self.index = 0
        return self
    
    def __next__(self):
        if self.index < len(self.points):
            point = self.points[self.index]
            self.index += 1
            return point
        else:
            raise StopIteration

class KochSnowflakeIterator:
    def __init__(self, x1, y1, x2, y2, iterations):
        self.iterations = iterations
        self.points = []
        
        # Adjusted coordinates for the third vertex
        x3 = 0.5 * (x1 + x2)
        y3 = y1 - (x2 - x1) * np.sqrt(3) / 2
        
        self._generate_curve(x1, y1, x2, y2, iterations, self.points)
        self._generate_curve(x2, y2, x3, y3, iterations, self.points)
        self._generate_curve(x3, y3, x1, y1, iterations, self.points)

    def _generate_curve(self, x1, y1, x2, y2, iterations, points):
        if iterations == 0:
            points.append([x2, y2]); return
        dx, dy = x2 - x1, y2 - y1
        x3, y3 = x1 + dx / 3, y1 + dy / 3
        x4, y4 = 0.5 * (x1 + x2) + np.sqrt(3) * (y1 - y2) / 6, 0.5 * (y1 + y2) + np.sqrt(3) * (x2 - x1) / 6
        x5, y5 = x1 + 2 * dx / 3, y1 + 2 * dy / 3
        self._generate_curve(x1, y1, x3, y3, iterations - 1, points)
        self._generate_curve(x3, y3, x4, y4, iterations - 1, points)
        self._generate_curve(x4, y4, x5, y5, iterations - 1, points)
        self._generate_curve(x5, y5, x2, y2, iterations - 1, points)

    def __iter__(self):
        self.index = 0
        return self
    
    def __next__(self):
        if self.index < len(self.points):
            point = self.points[self.index]
            self.index += 1
            return point
        else:
            raise StopIteration

# Testing the iterator
koch_iterator = KochCurveIterator(-0.5, 0, 0.5, 0, 2)
koch_points = [point for point in koch_iterator]

# Convert to NumPy array for easier manipulation
koch_points = np.array(koch_points)

# Calculate the shift needed to center the curve vertically
y_min = np.min(koch_points[:, 1])
y_max = np.max(koch_points[:, 1])
y_center = (y_min + y_max) / 2
y_shift = -y_center
koch_points[:, 1] += y_shift
fig, ax = plt.subplots()
# Initial plot with 0 iterations
iterations = 0

# Function to plot and update graph
def plot_graph(iterator_class, iterations):
    iterator = iterator_class(-0.5, 0, 0.5, 0, iterations)
    points = [point for point in iterator]
    points = np.array(points)

    y_min = np.min(points[:, 1])
    y_max = np.max(points[:, 1])
    y_center = (y_min + y_max) / 2
    y_shift = -y_center
    points[:, 1] += y_shift

    ax.clear()
    ax.plot(points[:, 0], points[:, 1])
    ax.text(0.05, 0.9, f'Iterations: {iterations}', transform=ax.transAxes)
    ax.text(0.05, 1.1, f'Press < to show the previous iteration, or > to show the next.', transform=ax.transAxes)
    ax.set_xlim([-0.6, 0.6])
    ax.set_ylim([-0.3, 0.3])
    ax.set_aspect('equal', adjustable='box')
    plt.draw()

terations = 0
current_iterator = KochCurveIterator  # Default iterator

def on_key(event):
    global iterations, current_iterator
    if event.key == '>':
        iterations = min(10, iterations + 1)  # Clamp to a sensible limit
        plot_graph(current_iterator, iterations)
    elif event.key == '<':
        iterations = max(0, iterations - 1)
        plot_graph(current_iterator, iterations)

# Create a single figure instance
# fig, ax = plt.subplots()
fig.canvas.mpl_connect('key_press_event', on_key)

# Display initial plot with 0 iterations
while True:
    print("1. Koch Curve")
    print("2. Koch Snowflake")
    print("3. Exit")
    choice = int(input("Enter your choice: "))
    if choice == 1:
        current_iterator = KochCurveIterator
        plot_graph(current_iterator, iterations)
        plt.show()
        break
    elif choice == 2:
        current_iterator = KochSnowflakeIterator
        plot_graph(current_iterator, iterations)
        plt.show()
        break
    elif choice == 3:
        break
    else:
        print("Invalid choice")
        continue

