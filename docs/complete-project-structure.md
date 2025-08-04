# Federal Agency Org Chart - Complete File Structure

Here’s the complete file structure you need to create in your GitHub repository:

```
federal-agency-org-chart/
├── README.md                    # Main documentation
├── index.html                   # Main org chart application (FIXED)
├── LICENSE                      # MIT License
├── .gitignore                   # Git ignore file
├── data/                        # CSV data files directory
│   ├── phonebook_20250625.csv   # Employee data
│   ├── outlook_20250625.csv     # Email directory
│   └── org_units_20250625.csv   # Organizational units
├── assets/                      # Images and static files
│   └── .gitkeep                 # Keep directory in git
├── server/                      # Optional Flask server
│   ├── app.py                   # Flask application
│   └── requirements.txt         # Python dependencies
└── docs/                        # Documentation
    ├── data-format.md           # Data format specification
    └── customization.md         # Customization guide
```

## Key Fixes Made to index.html:

1. **Fixed CSV Loading**: Now properly loads external CSV files from `data/` directory
1. **Better Error Handling**: Shows clear error messages if files can’t be loaded
1. **Improved Data Processing**: Better name normalization and hierarchy building
1. **Console Logging**: Added debugging output to help troubleshoot issues
1. **Robust Parsing**: Better handling of empty fields and malformed data

## Quick Setup Instructions:

1. **Create the directory structure**:
   
   ```bash
   mkdir federal-agency-org-chart
   cd federal-agency-org-chart
   mkdir data assets server docs
   ```
1. **Create the CSV files** in the `data/` directory using the sample data provided
1. **Save the corrected `index.html`** in the root directory
1. **Test locally**:
- Option A: Open `index.html` directly in a browser (may have CORS issues)
- Option B: Use a simple HTTP server:
  
  ```bash
  # Python 3
  python -m http.server 8000
  
  # Python 2
  python -m SimpleHTTPServer 8000
  
  # Node.js (if you have it)
  npx http-server
  ```
1. **View the chart**: Open `http://localhost:8000` in your browser

## Troubleshooting:

- **CORS errors**: Use an HTTP server instead of opening the file directly
- **CSV not loading**: Check file paths and ensure files are in `data/` directory
- **No chart appears**: Check browser console for error messages
- **Wrong hierarchy**: Verify manager names exactly match employee names in the CSV

The corrected HTML file should now work properly with external CSV files!