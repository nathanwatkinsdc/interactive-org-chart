# Federal Agency Organizational Chart

An interactive, dynamic organizational chart built with D3.js that visualizes the complete reporting structure of a federal agency. Features collapsible tree navigation, rich tooltips, and automatic data processing from CSV files.

![Org Chart Demo](assets/demo-screenshot.png)

## 🚀 Features

- **Interactive Visualization**: Click nodes to expand/collapse organizational levels
- **Rich Tooltips**: Hover over employees to see detailed information (name, title, email, phone, office, location, manager)
- **Color-Coded Hierarchy**: Visual distinction between divisions, offices, branches, and individual employees
- **Zoom & Pan**: Navigate large organizational structures with mouse controls
- **Responsive Design**: Works on desktop and tablet devices
- **Data Processing**: Automatically merges and structures data from multiple CSV sources

## 📁 Project Structure

```
federal-agency-org-chart/
├── README.md                 # This file
├── index.html               # Main org chart application
├── data/                    # CSV data files
│   ├── phonebook_20250625.csv
│   ├── outlook_20250625.csv
│   └── org_units_20250625.csv
├── assets/                  # Images and documentation
│   └── demo-screenshot.png
├── server/                  # Optional Flask server
│   ├── app.py
│   └── requirements.txt
└── docs/                    # Additional documentation
    ├── data-format.md
    └── customization.md
```

## 🎯 Quick Start

### Option 1: Static HTML (Recommended)

1. Clone this repository
1. Place your CSV files in the `data/` directory
1. Open `index.html` in a web browser
1. The chart will automatically load and process your data

### Option 2: Flask Server

1. Clone this repository
1. Install Python dependencies: `pip install -r server/requirements.txt`
1. Run the server: `python server/app.py`
1. Open `http://localhost:5000` in your browser

## 📊 Data Requirements

Your CSV files should follow this structure:

### phonebook_20250625.csv

```csv
Email,Name,Title,Phone,Mobile,Office,Location,Manager
smith.jane@agency.gov,"Smith, Jane",Director,202-555-0100,202-555-1100,OD,HQ,
```

### outlook_20250625.csv

```csv
Email,Name
smith.jane@agency.gov,"Smith, Jane"
```

### org_units_20250625.csv

```csv
Office,Acronym,Type
Office of the Director,OD,Division
```

**Key Points:**

- Email is used as the unique identifier
- Names should be in “Last, First” format
- Manager field should match the Name field of another employee
- Office acronyms should match between phonebook and org_units files

## 🎨 Customization

### Colors

Modify the CSS in `index.html`:

```css
.node.division circle { fill: #e74c3c; }  /* Red for divisions */
.node.office circle { fill: #3498db; }    /* Blue for offices */
.node.branch circle { fill: #27ae60; }    /* Green for branches */
.node.employee circle { fill: #f39c12; }  /* Orange for employees */
```

### Node Sizes

Adjust the radius values in the JavaScript:

```javascript
case 'division': return 8;
case 'office': return 7;
case 'branch': return 6;
default: return 5;  // employees
```

### Tooltip Content

Modify the `showTooltip` function to add/remove information fields.

### Layout Spacing

Change horizontal spacing by modifying:

```javascript
d.y = d.depth * 180;  // Increase for wider spacing
```

## 🔧 Technical Details

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Visualization**: D3.js v7.8.5
- **Data Processing**: Papa Parse v5.4.1
- **Backend** (optional): Python Flask
- **Browser Support**: Modern browsers (Chrome, Firefox, Safari, Edge)

## 📝 Data Processing Logic

1. **Loading**: Reads three CSV files (phonebook, outlook, org_units)
1. **Merging**: Combines phonebook and outlook data using email as primary key
1. **Normalization**: Handles name formatting inconsistencies for manager matching
1. **Hierarchy Building**: Creates reporting tree starting from Agency Director
1. **Unit Mapping**: Associates employees with their organizational units
1. **Rendering**: Generates interactive D3.js tree visualization

## 🚨 Troubleshooting

### Common Issues

**Chart doesn’t load:**

- Check browser console for errors
- Ensure CSV files are properly formatted
- Verify file paths are correct

**Missing employees:**

- Check that email addresses match between files
- Verify manager names match exactly (case-sensitive)
- Ensure Agency Director is properly identified

**Layout issues:**

- Try the “Reset View” button
- Check that organizational units are properly defined
- Verify the hierarchy depth isn’t too deep for display

### Data Validation

Run this checklist on your CSV files:

- [ ] No empty email fields in phonebook
- [ ] Manager names match existing employee names
- [ ] Office acronyms match between phonebook and org_units
- [ ] Agency Director has empty manager field
- [ ] No circular reporting relationships

## 🤝 Contributing

1. Fork the repository
1. Create a feature branch (`git checkout -b feature/amazing-feature`)
1. Commit your changes (`git commit -m 'Add amazing feature'`)
1. Push to the branch (`git push origin feature/amazing-feature`)
1. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the <LICENSE> file for details.

## 👥 Authors

- **Your Name** - *Initial work* - [YourGitHub](https://github.com/yourusername)

## 🙏 Acknowledgments

- D3.js community for the excellent visualization library
- Papa Parse for robust CSV processing
- Federal agency data management best practices

## 📞 Support

For questions or issues:

1. Check the [documentation](docs/)
1. Search existing [issues](https://github.com/yourusername/federal-agency-org-chart/issues)
1. Create a new issue with detailed information

-----

**Note**: This tool is designed for federal agency organizational data. Ensure compliance with your agency’s data sharing and visualization policies before deployment.