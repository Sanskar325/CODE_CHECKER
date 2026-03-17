import os
import time  # <--- ADD THIS
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename

# Import your scripts from Day 1 and Day 2
from checker import ROSCodeChecker
from runner import SimulationRunner

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Global variable to store last report (simple storage)
latest_report = None

@app.route('/', methods=['GET', 'POST'])
def index():
    global latest_report
    
    if request.method == 'POST':
        # 1. Check if file is present
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)

        # 2. Save the file
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # 3. Run the Checker (Day 1 Logic)
            checker = ROSCodeChecker()
            latest_report = checker.run_check(filename)
            
            # ... (inside index function, after checker runs) ...
            latest_report = checker.run_check(filename)
            
            # PASS 'timestamp' to the template
            return render_template('index.html', report=latest_report, timestamp=time.time())

    # Update the default return at the bottom too
    return render_template('index.html', report=None, timestamp=time.time())

    return render_template('index.html', report=None)

@app.route('/run_sim', methods=['POST'])
def run_simulation():
    runner = SimulationRunner()
    runner.run_full_test(duration=15)
    
    # Redirect back to the main page to show the image
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
