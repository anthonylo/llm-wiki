"""Script to create test fixture files that require binary formats."""
from pathlib import Path
import openpyxl

fixtures = Path(__file__).parent / "fixtures"
fixtures.mkdir(exist_ok=True)

wb = openpyxl.Workbook()

# Sheet 1: Employees
ws1 = wb.active
ws1.title = "Employees"
ws1.append(["id", "name", "department", "salary"])
ws1.append([1, "Alice Johnson", "Engineering", 95000])
ws1.append([2, "Bob Smith", "Marketing", 72000])
ws1.append([3, "Carol White", "Engineering", 105000])

# Sheet 2: Projects
ws2 = wb.create_sheet("Projects")
ws2.append(["project_id", "name", "status", "owner"])
ws2.append([101, "Phoenix", "active", "Alice Johnson"])
ws2.append([102, "Atlas", "planning", "Carol White"])

# Sheet 3: Empty (should be skipped)
ws3 = wb.create_sheet("Empty")

wb.save(fixtures / "sample.xlsx")
print(f"Created {fixtures / 'sample.xlsx'}")
