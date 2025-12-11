# Root Finding Algorithms Visualizer

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![Chart.js](https://img.shields.io/badge/Chart.js-4.0-orange)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

A web-based interactive tool to visualize and compare numerical methods for finding roots of non-linear equations. Built for the **CSE-4745/4746 Numerical Methods** course.

![Project Screenshot](https://via.placeholder.com/800x400?text=Run+Project+And+Take+Screenshot)
## 🚀 Features

* **Equation Parsing:** Supports complex mathematical inputs (e.g., `x^3 - x - 2`, `sin(x) - x/2`) using SymPy.
* **Four Numerical Methods:**
    1.  Bisection Method
    2.  Newton-Raphson Method
    3.  Secant Method
    4.  Regular False Position (Regula Falsi)
* **Comparative Analysis:** The "All Methods" mode runs all algorithms simultaneously.
* **Visual Analytics:** Uses **Chart.js** to plot the convergence rate (Error vs. Iterations) on a logarithmic scale.
* **Safety Mechanisms:** Backend logic (Python) handles division by zero, divergence, and iteration limits to prevent crashes.
* **Modern UI:** Responsive design with a glassmorphism aesthetic using CSS variables.

## 🛠️ Tech Stack

* **Backend:** Python (Flask), NumPy, SymPy (for symbolic mathematics).
* **Frontend:** HTML5, CSS3, JavaScript.
* **Visualization:** Chart.js.

## 📂 Project Structure

```text
Project/
├── app.py                # Main Flask application and logic
├── requirements.txt      # Python dependencies
├── static/
│   ├── CSS/
│   │   └── style.css     # Styling and Glassmorphism effects
│   └── JS/
│       └── script.js     # Fetch API calls and Chart.js configuration
└── templates/
    └── index.html        # Main user interface
