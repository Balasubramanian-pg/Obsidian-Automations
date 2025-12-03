import os
import shutil
from pathlib import Path

# ==========================================
# 1. SETUP PATHS
# ==========================================
# The folder where the files are currently STUCK
source_folder = Path(r"C:\Users\BalasubramanianPG\Videos\Obsidian Vault\Power BI\Query Langauges\DAX\Core Functions\Other")

# The ROOT DAX folder (We need this to move "Concepts" files out of "Core Functions")
root_base = source_folder.parent.parent 

print(f"📍 Source: {source_folder}")
print(f"📍 Root:   {root_base}")

# ==========================================
# 2. THE COMPREHENSIVE MAPPING (Based on your Screenshots)
# ==========================================
categorization = {
    # --- STATISTICAL ---
    "chisq-inv-rt.md": ("Core Functions", "Statistical"),
    "geomeanx.md": ("Core Functions", "Statistical"),
    "linest.md": ("Core Functions", "Statistical"),
    "linestx.md": ("Core Functions", "Statistical"),
    "percentilex-exc.md": ("Core Functions", "Statistical"),
    "percentilex-inc.md": ("Core Functions", "Statistical"),
    "stdevx-p.md": ("Core Functions", "Statistical"),
    "stdevx-s.md": ("Core Functions", "Statistical"),
    "t-inv-2t.md": ("Core Functions", "Statistical"),
    "var-p.md": ("Core Functions", "Statistical"),
    "var-s.md": ("Core Functions", "Statistical"),
    "varx-p.md": ("Core Functions", "Statistical"),
    "varx-s.md": ("Core Functions", "Statistical"),

    # --- TIME INTELLIGENCE ---
    "closingbalanceweek.md": ("Core Functions", "Time-Intelligence"),
    "endofquarter.md": ("Core Functions", "Time-Intelligence"),
    "endofweek.md": ("Core Functions", "Time-Intelligence"),
    "firstnonblank.md": ("Core Functions", "Time-Intelligence"),
    "firstnonblankvalue.md": ("Core Functions", "Time-Intelligence"),
    "lastnonblank.md": ("Core Functions", "Time-Intelligence"),
    "lastnonblankvalue.md": ("Core Functions", "Time-Intelligence"),
    "nextquarter.md": ("Core Functions", "Time-Intelligence"),
    "nextweek.md": ("Core Functions", "Time-Intelligence"),
    "openingbalancequarter.md": ("Core Functions", "Time-Intelligence"),
    "openingbalanceweek.md": ("Core Functions", "Time-Intelligence"),
    "previousquarter.md": ("Core Functions", "Time-Intelligence"),
    "previousweek.md": ("Core Functions", "Time-Intelligence"),
    "startofquarter.md": ("Core Functions", "Time-Intelligence"),
    "startofweek.md": ("Core Functions", "Time-Intelligence"),
    "totalwtd.md": ("Core Functions", "Time-Intelligence"),

    # --- TABLE MANIPULATION / WINDOW FUNCTIONS ---
    # Microsoft categorizes Window functions (Offset, Index, Window) under Table Manipulation
    "addmissingitems.md": ("Core Functions", "Table-Manipulation"),
    "columnstatistics.md": ("Core Functions", "Table-Manipulation"),
    "generateseries.md": ("Core Functions", "Table-Manipulation"),
    "groupcrossapply.md": ("Core Functions", "Table-Manipulation"),
    "index.md": ("Core Functions", "Table-Manipulation"), 
    "matchby.md": ("Core Functions", "Table-Manipulation"),
    "offset.md": ("Core Functions", "Table-Manipulation"),
    "orderby.md": ("Core Functions", "Table-Manipulation"),
    "partitionby.md": ("Core Functions", "Table-Manipulation"),
    "rollup.md": ("Core Functions", "Table-Manipulation"),
    "rollupaddissubtotal.md": ("Core Functions", "Table-Manipulation"),
    "rollupgroup.md": ("Core Functions", "Table-Manipulation"),
    "rollupissubtotal.md": ("Core Functions", "Table-Manipulation"),
    "rownumber.md": ("Core Functions", "Table-Manipulation"),
    "sample.md": ("Core Functions", "Table-Manipulation"),
    "samplecartesianpointsbycover.md": ("Core Functions", "Table-Manipulation"),
    "substitutewithindex.md": ("Core Functions", "Table-Manipulation"),
    "topnskip.md": ("Core Functions", "Table-Manipulation"),
    "window.md": ("Core Functions", "Table-Manipulation"),

    # --- INFORMATION ---
    "containsstringexact.md": ("Core Functions", "Information"),
    "error.md": ("Core Functions", "Information"),
    "info-annotations.md": ("Core Functions", "Information"),
    "info-calcdependency.md": ("Core Functions", "Information"),
    "info-view-columns.md": ("Core Functions", "Information"),
    "info-view-measures.md": ("Core Functions", "Information"),
    "info-view-relationships.md": ("Core Functions", "Information"),
    "userculture.md": ("Core Functions", "Information"),
    "userobjectid.md": ("Core Functions", "Information"),

    # --- TEXT ---
    "combinevalues.md": ("Core Functions", "Text"),
    "tocsv.md": ("Core Functions", "Text"),
    "tojson.md": ("Core Functions", "Text"),

    # --- LOGICAL ---
    "if-eager.md": ("Core Functions", "Logical"),

    # --- VISUAL CALCULATIONS (New Category to clean up Other) ---
    # These are specific to Visual Calculations and don't fit perfectly elsewhere
    "collapse.md": ("Core Functions", "Visual-Calculations"),
    "collapseall.md": ("Core Functions", "Visual-Calculations"),
    "expand.md": ("Core Functions", "Visual-Calculations"),
    "expandall.md": ("Core Functions", "Visual-Calculations"),
    "first.md": ("Core Functions", "Visual-Calculations"),
    "last.md": ("Core Functions", "Visual-Calculations"),
    "lookup.md": ("Core Functions", "Visual-Calculations"), # This is the Visual Calc Lookup
    "lookupwithtotals.md": ("Core Functions", "Visual-Calculations"),
    "movingaverage.md": ("Core Functions", "Visual-Calculations"),
    "next.md": ("Core Functions", "Visual-Calculations"),
    "previous.md": ("Core Functions", "Visual-Calculations"),
    "range.md": ("Core Functions", "Visual-Calculations"),
    "isatlevel.md": ("Core Functions", "Visual-Calculations"),

    # --- CONCEPTS / STATEMENTS (Move out of Core Functions) ---
    "define-statement-dax.md": ("Concepts", "Statements"),
    "evaluate-statement-dax.md": ("Concepts", "Statements"),
    "function-statement-dax.md": ("Concepts", "Statements"),
    "measure-statement-dax.md": ("Concepts", "Statements"),
    "orderby-statement-dax.md": ("Concepts", "Statements"),
    "startat-statement-dax.md": ("Concepts", "Statements"),
    "statements-dax.md": ("Concepts", "Statements"),
    "var-dax.md": ("Concepts", "Statements"), # VAR keyword
    "virtual-column-statement-dax.md": ("Concepts", "Statements"),
    "understanding-functions-for-parent-child-hierarchies-in-dax.md": ("Concepts", "Special-Topics"),
    
    # --- REMAINING ITEMS (Keep in Other or Specific) ---
    "convert.md": ("Core Functions", "Other"), # Data type conversion
    "detailrows.md": ("Core Functions", "Other"),
    "evaluateandlog.md": ("Core Functions", "Other"), # Debugging
    "externalmeasure.md": ("Core Functions", "Other"), # Excel specific
    "nonvisual.md": ("Core Functions", "Other"),
    "shadowcluster.md": ("Core Functions", "Other"),
    "alwaysapply.md": ("Core Functions", "Other"),
    "dependon.md": ("Core Functions", "Other"),
    "ignore.md": ("Core Functions", "Other"),
}

# ==========================================
# 3. EXECUTION LOGIC
# ==========================================
def run_organization():
    if not source_folder.exists():
        print(f"❌ Error: Source folder not found: {source_folder}")
        return

    # Get list of all markdown files in the 'Other' folder
    files = list(source_folder.glob("*.md"))
    print(f"🔍 Found {len(files)} files in 'Other'...")
    
    moved_count = 0
    
    for file_path in files:
        filename = file_path.name.lower()
        original_name = file_path.name
        
        # Check if we have a mapping for this file
        if filename in categorization:
            main_cat, sub_cat = categorization[filename]
            
            # Construct destination path
            # Example: DAX / Core Functions / Statistical
            if sub_cat:
                dest_dir = root_base / main_cat / sub_cat
            else:
                dest_dir = root_base / main_cat
            
            # Create folder if it doesn't exist
            dest_dir.mkdir(parents=True, exist_ok=True)
            dest_file = dest_dir / original_name
            
            try:
                # Don't overwrite if it exists, just skip or print warning
                if dest_file.exists():
                    print(f"⚠️  Skipped {original_name} (Already exists in {sub_cat})")
                else:
                    shutil.move(str(file_path), str(dest_file))
                    print(f"✅ Moved {original_name} -> {main_cat}/{sub_cat}")
                    moved_count += 1
            except Exception as e:
                print(f"❌ Error moving {original_name}: {e}")
        else:
            # Files not in the list stay in 'Other'
            pass

    print("\n" + "="*50)
    print(f"🎉 Cleanup Complete. Moved {moved_count} files out of 'Other'.")
    print("="*50)

# Run the script
run_organization()