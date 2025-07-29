from flask import Flask, render_template, request, jsonify, session
from datetime import datetime
import json
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production

# Removed top-level session initialization

def calculate_bmi(weight_kg, height_cm):
    """Calculate BMI given weight in kg and height in cm"""
    height_m = height_cm / 100  # Convert cm to meters
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 2)

def get_bmi_category(bmi):
    """Get BMI category based on BMI value"""
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obese"

@app.route('/')
def index():
    """Home page with BMI calculator"""
    return render_template('index.html')

@app.route('/about')
def about():
    """About page with BMI information"""
    return render_template('about.html')

@app.route('/project')
def project():
    """Project information page"""
    return render_template('project.html')

@app.route('/history-page')
def history_page():
    """History page to view calculation history"""
    return render_template('history.html')

@app.route('/contact')
def contact():
    """Contact page"""
    return render_template('contact.html')

@app.route('/calculate-bmi', methods=['POST'])
def calculate_bmi_api():
    """API endpoint to calculate BMI"""
    try:
        data = request.get_json()
        weight = float(data.get('weight'))
        height = float(data.get('height'))
        
        # Validate input
        if weight <= 0 or height <= 0:
            return jsonify({'error': 'Weight and height must be positive values'}), 400
        
        # Calculate BMI
        bmi = calculate_bmi(weight, height)
        category = get_bmi_category(bmi)
        
        # Save to history
        history_entry = {
            'bmi': bmi,
            'weight': weight,
            'height': height,
            'category': category,
            'date': datetime.now().strftime('%Y-%m-%d'),
            'time': datetime.now().strftime('%H:%M:%S')
        }
        
        # Add to session history (limit to last 50 entries)
        if 'bmi_history' not in session:
            session['bmi_history'] = []
        session['bmi_history'].append(history_entry)
        if len(session['bmi_history']) > 50:
            session['bmi_history'] = session['bmi_history'][-50:]
        
        return jsonify({
            'bmi': bmi,
            'category': category,
            'success': True
        })
        
    except (ValueError, KeyError) as e:
        return jsonify({'error': 'Invalid input data'}), 400
    except Exception as e:
        return jsonify({'error': 'An error occurred during calculation'}), 500

@app.route('/history')
def get_history():
    """API endpoint to get BMI calculation history"""
    try:
        if 'bmi_history' not in session:
            session['bmi_history'] = []
        history = session.get('bmi_history', [])
        return jsonify(history)
    except Exception as e:
        return jsonify({'error': 'Error retrieving history'}), 500

@app.route('/clear-history', methods=['POST'])
def clear_history():
    """API endpoint to clear BMI calculation history"""
    try:
        session['bmi_history'] = []
        return jsonify({'success': True, 'message': 'History cleared successfully'})
    except Exception as e:
        return jsonify({'error': 'Error clearing history'}), 500

@app.route('/contact-submit', methods=['POST'])
def contact_submit():
    """Handle contact form submission"""
    try:
        data = request.get_json()
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        subject = data.get('subject', '').strip()
        message = data.get('message', '').strip()
        
        # Basic validation
        if not all([name, email, subject, message]):
            return jsonify({'error': 'All fields are required'}), 400
        
        # Email validation (basic)
        if '@' not in email or '.' not in email:
            return jsonify({'error': 'Please enter a valid email address'}), 400
        
        # In a real application, you would save this to a database or send an email
        # For now, we'll just return success
        return jsonify({
            'success': True,
            'message': 'Thank you for your message! We will get back to you soon.'
        })
        
    except Exception as e:
        return jsonify({'error': 'Error submitting contact form'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
