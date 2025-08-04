# Customization Guide

This guide explains how to customize the Federal Agency Org Chart to match your organization’s needs and branding.

## Visual Customization

### Colors and Styling

#### Node Colors

Modify the CSS in `index.html` to change node colors:

```css
/* Division nodes (top level) */
.node.division circle {
    fill: #e74c3c;  /* Red */
    r: 8;
}

/* Office nodes */
.node.office circle {
    fill: #3498db;  /* Blue */
    r: 7;
}

/* Branch nodes */
.node.branch circle {
    fill: #27ae60;  /* Green */
    r: 6;
}

/* Employee nodes */
.node.employee circle {
    fill: #f39c12;  /* Orange */
    r: 5;
}
```

#### Color Schemes

Popular alternatives:

**Government Blue Theme:**

```css
.node.division circle { fill: #1f3a93; }
.node.office circle { fill: #2e5bba; }
.node.branch circle { fill: #4472c4; }
.node.employee circle { fill: #6c8ebf; }
```

**Monochrome Theme:**

```css
.node.division circle { fill: #2c3e50; }
.node.office circle { fill: #34495e; }
.node.branch circle { fill: #7f8c8d; }
.node.employee circle { fill: #95a5a6; }
```

#### Text Styling

Customize text appearance:

```css
.node text {
    font-size: 12px;
    font-weight: 500;
    fill: #2c3e50;
    font-family: 'Arial', sans-serif;
}

.node.division text {
    font-size: 14px;
    font-weight: 700;
    fill: #1a252f;
}
```

### Layout Adjustments

#### Node Spacing

Adjust horizontal and vertical spacing:

```javascript
// Horizontal spacing between levels
nodes.forEach(d => d.y = d.depth * 200);  // Default: 180

// Tree dimensions
tree = d3.tree().size([height - 100, width - 250]);  // Adjust margins
```

#### Node Sizes

Modify node sizes in the update function:

```javascript
nodeUpdate.select('circle')
    .attr('r', d => {
        switch(d.data.type) {
            case 'division': return 10;  // Larger divisions
            case 'office': return 8;
            case 'branch': return 6;
            case 'director': return 12;  // Special director size
            default: return 4;  // Smaller employees
        }
    });
```

### Tooltip Customization

#### Adding Fields

Modify the `showTooltip` function to include additional information:

```javascript
function showTooltip(event, d) {
    if (!d.data.data) return;
    
    const data = d.data.data;
    let content = `<strong>${data.name}</strong><br/>`;
    if (data.title) content += `Title: ${data.title}<br/>`;
    if (data.email) content += `Email: ${data.email}<br/>`;
    if (data.phone) content += `Phone: ${data.phone}<br/>`;
    if (data.mobile) content += `Mobile: ${data.mobile}<br/>`;
    if (data.office) content += `Office: ${data.office}<br/>`;
    if (data.location) content += `Location: ${data.location}<br/>`;
    if (data.manager) content += `Manager: ${data.manager}<br/>`;
    
    // Add custom fields
    if (data.startDate) content += `Start Date: ${data.startDate}<br/>`;
    if (data.grade) content += `Grade: ${data.grade}<br/>`;
    if (data.clearance) content += `Clearance: ${data.clearance}`;
    
    // ... rest of tooltip code
}
```

#### Tooltip Styling

Customize tooltip appearance:

```css
.tooltip {
    position: absolute;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 15px;
    border-radius: 8px;
    font-size: 13px;
    line-height: 1.5;
    pointer-events: none;
    z-index: 1000;
    max-width: 350px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    border: 1px solid rgba(255,255,255,0.2);
}
```

## Functional Customization

### Node Labels

Customize what text appears on nodes:

```javascript
nodeEnter.append('text')
    .text(d => {
        if (d.data.data?.title) {
            // Show name and title
            return `${d.data.name} (${d.data.data.title})`;
        } else if (d.data.type === 'division') {
            // Show just division name
            return d.data.name;
        } else {
            // Custom format
            return d.data.name.split(' ')[0]; // First name only
        }
    });
```

### Filtering and Search

Add a search function:

```javascript
function searchNodes(searchTerm) {
    const term = searchTerm.toLowerCase();
    
    // Reset all nodes
    g.selectAll('.node').style('opacity', 1);
    
    if (term) {
        g.selectAll('.node')
            .style('opacity', d => {
                const name = d.data.name?.toLowerCase() || '';
                const title = d.data.data?.title?.toLowerCase() || '';
                const email = d.data.data?.email?.toLowerCase() || '';
                
                return name.includes(term) || 
                       title.includes(term) || 
                       email.includes(term) ? 1 : 0.3;
            });
    }
}
```

Add search HTML:

```html
<div class="controls">
    <input type="text" id="searchBox" placeholder="Search employees..." 
           oninput="searchNodes(this.value)">
    <button onclick="expandAll()">Expand All</button>
    <button onclick="collapseAll()">Collapse All</button>
</div>
```

### Data Processing Customization

#### Custom Data Sources

Modify the data loading to use different file formats:

```javascript
// Load from JSON instead of CSV
async function loadDataFromJSON() {
    const response = await fetch('data/org-data.json');
    const data = await response.json();
    return processJSONData(data);
}

// Load from API endpoint
async function loadDataFromAPI() {
    const response = await fetch('/api/org-data');
    const data = await response.json();
    return processAPIData(data);
}
```

#### Custom Hierarchy Rules

Modify the hierarchy building logic:

```javascript
function getNodeType(employee, orgMap) {
    const title = employee.title.toLowerCase();
    const office = employee.office;
    
    // Custom rules for your organization
    if (title.includes('deputy director')) return 'division';
    if (title.includes('associate director')) return 'office';
    if (title.includes('team lead')) return 'branch';
    if (title.includes('senior')) return 'senior-employee';
    
    return 'employee';
}
```

## Agency-Specific Customization

### Branding

Add your agency logo and colors:

```html
<div class="header">
    <img src="assets/agency-logo.png" alt="Agency Logo" class="logo">
    <h1>Your Agency Name - Organizational Chart</h1>
</div>
```

```css
.header {
    text-align: center;
    padding: 20px;
    background: linear-gradient(135deg, #your-color-1, #your-color-2);
    color: white;
    margin-bottom: 30px;
}

.logo {
    height: 60px;
    margin-bottom: 10px;
}
```

### Custom Classifications

Add security clearance or grade level indicators:

```javascript
nodeEnter.append('text')
    .attr('class', 'grade-indicator')
    .attr('x', 12)
    .attr('y', -8)
    .text(d => d.data.data?.grade || '')
    .style('font-size', '10px')
    .style('fill', '#7f8c8d');
```

### Export Functionality

Add PDF export capability:

```html
<button onclick="exportToPDF()">Export PDF</button>

<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
<script>
function exportToPDF() {
    const svg
```