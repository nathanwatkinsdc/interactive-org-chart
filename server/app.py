from flask import Flask, render_template, send_from_directory, jsonify
import pandas as pd
import json
import os
from pathlib import Path

app = Flask(**name**)

# Configuration

DATA_DIR = Path(**file**).parent.parent / ‘data’
STATIC_DIR = Path(**file**).parent.parent

@app.route(’/’)
def index():
“”“Serve the main org chart page”””
try:
with open(STATIC_DIR / ‘index.html’, ‘r’, encoding=‘utf-8’) as f:
html_content = f.read()
return html_content
except FileNotFoundError:
return “Error: index.html not found. Please ensure the file exists in the project root.”, 404

@app.route(’/data/<filename>’)
def serve_data(filename):
“”“Serve CSV files from the data directory”””
try:
return send_from_directory(DATA_DIR, filename)
except FileNotFoundError:
return f”Error: {filename} not found in data directory”, 404

@app.route(’/api/org-data’)
def get_org_data():
“”“API endpoint to get processed organizational data as JSON”””
try:
# Load CSV files
phonebook_file = DATA_DIR / ‘phonebook_20250625.csv’
outlook_file = DATA_DIR / ‘outlook_20250625.csv’
org_units_file = DATA_DIR / ‘org_units_20250625.csv’

    # Check if files exist
    for file_path, name in [(phonebook_file, 'phonebook'), 
                           (outlook_file, 'outlook'), 
                           (org_units_file, 'org_units')]:
        if not file_path.exists():
            return jsonify({'error': f'{name} CSV file not found'}), 404
    
    # Read CSV files
    phonebook = pd.read_csv(phonebook_file)
    outlook = pd.read_csv(outlook_file)
    org_units = pd.read_csv(org_units_file)
    
    # Basic data validation
    required_phonebook_cols = ['Email', 'Name', 'Title', 'Office', 'Manager']
    required_outlook_cols = ['Email', 'Name']
    required_org_cols = ['Office', 'Acronym', 'Type']
    
    for df, cols, name in [(phonebook, required_phonebook_cols, 'phonebook'),
                          (outlook, required_outlook_cols, 'outlook'),
                          (org_units, required_org_cols, 'org_units')]:
        missing_cols = [col for col in cols if col not in df.columns]
        if missing_cols:
            return jsonify({
                'error': f'Missing columns in {name}: {missing_cols}'
            }), 400
    
    # Convert DataFrames to dictionaries for JSON response
    data = {
        'phonebook': phonebook.fillna('').to_dict('records'),
        'outlook': outlook.fillna('').to_dict('records'),
        'org_units': org_units.fillna('').to_dict('records'),
        'stats': {
            'total_employees': len(phonebook),
            'total_org_units': len(org_units),
            'divisions': len(org_units[org_units['Type'] == 'Division']),
            'offices': len(org_units[org_units['Type'] == 'Office']),
            'branches': len(org_units[org_units['Type'] == 'Branch'])
        }
    }
    
    return jsonify(data)
    
except Exception as e:
    return jsonify({'error': f'Error processing data: {str(e)}'}), 500

@app.route(’/api/validate-data’)
def validate_data():
“”“API endpoint to validate the CSV data structure”””
try:
phonebook_file = DATA_DIR / ‘phonebook_20250625.csv’
outlook_file = DATA_DIR / ‘outlook_20250625.csv’
org_units_file = DATA_DIR / ‘org_units_20250625.csv’

    validation_results = {
        'valid': True,
        'errors': [],
        'warnings': [],
        'stats': {}
    }
    
    # Check file existence
    for file_path, name in [(phonebook_file, 'phonebook'), 
                           (outlook_file, 'outlook'), 
                           (org_units_file, 'org_units')]:
        if not file_path.exists():
            validation_results['valid'] = False
            validation_results['errors'].append(f'{name}.csv file not found')
            return jsonify(validation_results)
    
    # Load and validate data
    phonebook = pd.read_csv(phonebook_file)
    outlook = pd.read_csv(outlook_file)
    org_units = pd.read_csv(org_units_file)
    
    # Email validation
    phonebook_emails = set(phonebook['Email'].dropna())
    outlook_emails = set(outlook['Email'].dropna())
    
    missing_in_outlook = phonebook_emails - outlook_emails
    if missing_in_outlook:
        validation_results['warnings'].append(
            f'Emails in phonebook but not outlook: {list(missing_in_outlook)[:5]}...'
        )
    
    # Manager validation
    employee_names = set(phonebook['Name'].dropna().str.lower())
    managers = set(phonebook['Manager'].dropna().str.lower())
    invalid_managers = managers - employee_names - {'', 'director'}
    
    if invalid_managers:
        validation_results['warnings'].append(
            f'Manager names not found as employees: {list(invalid_managers)[:5]}...'
        )
    
    # Office acronym validation
    phonebook_offices = set(phonebook['Office'].dropna())
    org_unit_acronyms = set(org_units['Acronym'].dropna())
    missing_org_units = phonebook_offices - org_unit_acronyms
    
    if missing_org_units:
        validation_results['warnings'].append(
            f'Office acronyms in phonebook not found in org_units: {list(missing_org_units)}'
        )
    
    # Statistics
    validation_results['stats'] = {
        'phonebook_records': len(phonebook),
        'outlook_records': len(outlook),
        'org_units': len(org_units),
        'unique_emails_phonebook': len(phonebook_emails),
        'unique_emails_outlook': len(outlook_emails),
        'employees_with_managers': len(phonebook[phonebook['Manager'].notna()]),
        'potential_directors': len(phonebook[phonebook['Manager'].isna() | 
                                             (phonebook['Manager'].str.lower() == 'director')])
    }
    
    return jsonify(validation_results)
    
except Exception as e:
    return jsonify({
        'valid': False,
        'errors': [f'Error validating data: {str(e)}']
    }), 500

@app.route(’/health’)
def health_check():
“”“Health check endpoint”””
return jsonify({
‘status’: ‘healthy’,
‘data_directory’: str(DATA_DIR),
‘files_exist’: {
‘phonebook’: (DATA_DIR / ‘phonebook_20250625.csv’).exists(),
‘outlook’: (DATA_DIR / ‘outlook_20250625.csv’).exists(),
‘org_units’: (DATA_DIR / ‘org_units_20250625.csv’).exists()
}
})

@app.errorhandler(404)
def not_found(error):
return jsonify({‘error’: ‘Not found’}), 404

@app.errorhandler(500)
def internal_error(error):
return jsonify({‘error’: ‘Internal server error’}), 500

if **name** == ‘**main**’:
# Create data directory if it doesn’t exist
DATA_DIR.mkdir(exist_ok=True)

print(f"Starting Federal Agency Org Chart Server...")
print(f"Data directory: {DATA_DIR}")
print(f"Static files: {STATIC_DIR}")
print(f"Visit: http://localhost:5000")

app.run(debug=True, host='0.0.0.0', port=5000)