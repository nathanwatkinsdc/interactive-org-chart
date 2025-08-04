# Data Format Specification

This document describes the required format for CSV files used by the Federal Agency Org Chart application.

## File Overview

The application requires three CSV files:

1. `phonebook_20250625.csv` - Employee contact and organizational information
1. `outlook_20250625.csv` - Email directory (optional, used for validation)
1. `org_units_20250625.csv` - Organizational unit definitions

## phonebook_20250625.csv

The primary data file containing employee information and reporting relationships.

### Required Columns

|Column  |Type  |Description                           |Example                         |
|--------|------|--------------------------------------|--------------------------------|
|Email   |String|Unique employee identifier            |`smith.jane@agency.gov`         |
|Name    |String|Employee name in “Last, First” format |`"Smith, Jane"`                 |
|Title   |String|Job title                             |`"Director"`, `"Senior Analyst"`|
|Phone   |String|Office phone number                   |`"202-555-0100"`                |
|Mobile  |String|Mobile phone number                   |`"202-555-1100"`                |
|Office  |String|Office/unit acronym                   |`"OD"`, `"DSP"`                 |
|Location|String|Physical location                     |`"HQ"`, `"DC"`                  |
|Manager |String|Manager’s name in “Last, First” format|`"Doe, John"`                   |

### Data Rules

1. **Email**: Must be unique across all records
1. **Name**: Should follow “Last, First” format for consistency
1. **Manager**: Must match the Name field of another employee, or be empty for top-level directors
1. **Office**: Must correspond to an Acronym in the org_units file

### Example

```csv
Email,Name,Title,Phone,Mobile,Office,Location,Manager
smith.jane@agency.gov,"Smith, Jane",Director,202-555-0100,202-555-1100,OD,HQ,
doe.john@agency.gov,"Doe, John",Division Director,202-555-0101,202-555-1101,DSP,HQ,director
brown.lisa@agency.gov,"Brown, Lisa",Office Director,202-555-0102,202-555-1102,OO,HQ,"doe, john"
```

## outlook_20250625.csv

Email directory for validation and cross-referencing.

### Required Columns

|Column|Type  |Description           |Example                |
|------|------|----------------------|-----------------------|
|Email |String|Employee email address|`smith.jane@agency.gov`|
|Name  |String|Employee name         |`"Smith, Jane"`        |

### Purpose

- Validates that phonebook entries have corresponding email accounts
- Helps identify missing or incorrect email addresses
- Optional file - application works without it

### Example

```csv
Email,Name
smith.jane@agency.gov,"Smith, Jane"
doe.john@agency.gov,"Doe, John"
brown.lisa@agency.gov,"Brown, Lisa"
```

## org_units_20250625.csv

Organizational unit definitions and hierarchy.

### Required Columns

|Column |Type  |Description                           |Example                   |
|-------|------|--------------------------------------|--------------------------|
|Office |String|Full organizational unit name         |`"Office of the Director"`|
|Acronym|String|Short identifier used in phonebook    |`"OD"`                    |
|Type   |String|Unit type: Division, Office, or Branch|`"Division"`              |

### Organizational Types

1. **Division**: Top-level organizational units (red nodes)
1. **Office**: Mid-level units within divisions (blue nodes)
1. **Branch**: Lower-level units within offices (green nodes)

### Hierarchy Rules

- Divisions report to the Agency Director
- Offices belong to Divisions
- Branches belong to Offices
- Employees belong to Branches (or Offices if no Branch exists)

### Example

```csv
Office,Acronym,Type
Office of the Director,OD,Division
Division of Supervision Policy,DSP,Division
Office of Oversight,OO,Office
Branch of Market Surveillance,BMS,Branch
```

## Data Validation Checklist

Before using your CSV files, verify:

### ✅ File Structure

- [ ] All three CSV files are present
- [ ] Files use comma separators
- [ ] Headers match exactly (case-sensitive)
- [ ] No empty rows at the end

### ✅ Data Integrity

- [ ] No duplicate email addresses in phonebook
- [ ] All Manager names exist as employee Names (except for directors)
- [ ] All Office acronyms in phonebook exist in org_units
- [ ] At least one employee has empty Manager field (the director)

### ✅ Name Formatting

- [ ] Names consistently use “Last, First” format
- [ ] Manager names exactly match employee names
- [ ] Handle special cases (Jr., Sr., hyphenated names)

### ✅ Organizational Structure

- [ ] Clear hierarchy: Division → Office → Branch → Employee
- [ ] No circular reporting relationships
- [ ] Reasonable span of control (managers don’t have too many direct reports)

## Common Issues and Solutions

### Issue: Chart doesn’t display employees

**Cause**: Manager names don’t match employee names exactly
**Solution**: Ensure exact string matching, including capitalization and punctuation

### Issue: Missing organizational units

**Cause**: Office acronyms in phonebook don’t exist in org_units
**Solution**: Add missing units to org_units.csv or correct acronyms in phonebook

### Issue: Multiple directors appear

**Cause**: Multiple employees have empty Manager fields
**Solution**: Identify the single Agency Director and ensure all others have managers

### Issue: Employees appear at wrong levels

**Cause**: Incorrect organizational unit types or missing hierarchy
**Solution**: Verify Division → Office → Branch structure in org_units.csv

## File Naming Convention

Use date stamps in filenames to track versions:

- `phonebook_YYYYMMDD.csv`
- `outlook_YYYYMMDD.csv`
- `org_units_YYYYMMDD.csv`

Update the file references in `index.html` if using different dates.

## Data Privacy Considerations

When working with employee data:

1. Ensure proper authorization for data access
1. Consider anonymizing personal information for demos
1. Follow agency data handling policies
1. Secure file storage and transmission
1. Limit access to authorized personnel only