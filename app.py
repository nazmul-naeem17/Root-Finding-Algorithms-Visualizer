from flask import Flask, render_template, request, jsonify
from sympy import symbols, lambdify, sympify, diff
import numpy as np

app = Flask(__name__)

x = symbols('x')


def bisection_method_with_error(f, x1, x2, E=1e-5, max_iter=100):
    iterations, errors = [], []
    
    try:
        if f(x1) * f(x2) >= 0:
             raise ValueError("Bisection method fails: f(a) and f(b) must have opposite signs.")
    except Exception as e:
        raise ValueError(f"Error evaluating initial points: {str(e)}")

    for _ in range(max_iter):
        x0 = (x1 + x2) / 2
        
        try:
            current_error = abs(f(x0))
        except:
            current_error = float('inf')

        errors.append(float(current_error))
        iterations.append((float(x1), float(x2), float(x0)))

        if abs(x2 - x1) < E or abs(f(x0)) < E:
            return x0, iterations, errors

        if f(x0) * f(x1) < 0:
            x2 = x0
        else:
            x1 = x0
            
    return x0, iterations, errors

def newton_raphson_method_with_error(f, df, x0, E=1e-5, max_iter=100):
    iterations, errors = [], []
    for _ in range(max_iter):
        try:
            derivative = df(x0)
            if abs(derivative) < 1e-6:
                raise ValueError(f"Derivative too small at x={x0:.4f}")
            
            x1 = x0 - f(x0) / derivative
            
            # Error checking
            current_val = abs(f(x1))
            errors.append(float(current_val))
            iterations.append(float(x1))
            
            if abs(x1 - x0) < E:
                break
            
            x0 = x1
        except OverflowError:
            raise ValueError("Numbers became too large (Divergence). Try a different guess.")
            
    return x1, iterations, errors

def secant_method_with_error(f, x0, x1, E=1e-5, max_iter=100):
    iterations, errors = [], []
    x2 = x1 # Default
    
    for _ in range(max_iter):
        try:
            fx0 = f(x0)
            fx1 = f(x1)
            denominator = fx1 - fx0
            
            if abs(denominator) < 1e-6:
                raise ValueError("Denominator too small (Secant method).")
                
            x2 = x1 - (fx1 * (x1 - x0)) / denominator
            
            errors.append(float(abs(f(x2))))
            iterations.append((float(x0), float(x1), float(x2)))
            
            if abs(x2 - x1) < E:
                break
                
            x0, x1 = x1, x2
        except OverflowError:
             raise ValueError("Numbers became too large. Method diverged.")

    return x2, iterations, errors

def regular_false_position_with_error(f, x0, x1, E=1e-5, max_iter=100):
    iterations, errors = [], []
    x2 = x0
    
    if f(x0) * f(x1) >= 0:
         raise ValueError("False Position fails: f(a) and f(b) must have opposite signs.")

    for _ in range(max_iter):
        fx0 = f(x0)
        fx1 = f(x1)
        
        if abs(fx1 - fx0) < 1e-6:
            break
            
        x2 = x1 - (fx1 * (x1 - x0)) / (fx1 - fx0)
        f_x2 = f(x2)
        
        errors.append(float(abs(f_x2)))
        iterations.append((float(x0), float(x1), float(x2)))
        
        if abs(f_x2) < E or abs(x1 - x0) < E:
            break
            
        if f_x2 * fx0 < 0:
            x1 = x2
        else:
            x0 = x2
            
    return x2, iterations, errors

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/solve', methods=['POST'])
def solve():
    try:
        data = request.json
        equation = data.get('equation')
        interval_raw = data.get('interval', [])
        method = data.get('method')

        if not equation or not interval_raw:
            return jsonify({"error": "Missing equation or interval"}), 400

        try:
            interval = [float(i) for i in interval_raw]
        except ValueError:
            return jsonify({"error": "Interval must contain numbers"}), 400

        equation = equation.replace('^', '**')
        
        try:
            func_expr = sympify(equation)
            f = lambdify(x, func_expr, 'numpy')
            df = lambdify(x, diff(func_expr, x), 'numpy')
        except Exception as e:
            return jsonify({"error": f"Invalid Equation Syntax: {str(e)}"}), 400

        results = {}
        
        if method == "Bisection" or method == "All":
            root, iterations, errors = bisection_method_with_error(f, interval[0], interval[1])
            results["Bisection"] = {"root": root, "iterations": iterations, "errors": errors}

        if method == "Newton-Raphson" or method == "All":
            root, iterations, errors = newton_raphson_method_with_error(f, df, interval[0])
            results["Newton-Raphson"] = {"root": root, "iterations": iterations, "errors": errors}

        if method == "Secant" or method == "All":
            root, iterations, errors = secant_method_with_error(f, interval[0], interval[1])
            results["Secant"] = {"root": root, "iterations": iterations, "errors": errors}

        if method == "Regular False Position" or method == "All":
            root, iterations, errors = regular_false_position_with_error(f, interval[0], interval[1])
            results["Regular False Position"] = {"root": root, "iterations": iterations, "errors": errors}

        return jsonify(results)

    except ValueError as ve:
        return jsonify({"error": str(ve)})
    except Exception as e:
        return jsonify({"error": f"Calculation Error: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)