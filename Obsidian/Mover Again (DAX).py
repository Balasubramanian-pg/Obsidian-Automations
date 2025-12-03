import os
import shutil
import pandas as pd
from pathlib import Path

# ==========================================
# 1. CONFIGURATION
# ==========================================

# The folder where the files are CURRENTLY stuck
source_folder = Path(r"C:\Users\BalasubramanianPG\Videos\Obsidian Vault\Power BI\Query Langauges\DAX\Core Functions\Other")

# The ROOT folder (The "DAX" folder) where we want to build the structure
# We go up two levels from "Other": Other -> Core Functions -> DAX
root_base = source_folder.parent.parent 

print(f"📍 Source of files: {source_folder}")
print(f"📍 Destination Root: {root_base}")

# ==========================================
# 2. THE CATEGORIZATION MAP (Brainstormed & Organized)
# ==========================================
# I have consolidated your list and ensured casing matches standard DAX functions
categorization = {
    # --- Aggregation ---
    "average.md": ("Core Functions", "Aggregation"),
    "averagea.md": ("Core Functions", "Aggregation"),
    "averagex.md": ("Core Functions", "Aggregation"),
    "count.md": ("Core Functions", "Aggregation"),
    "counta.md": ("Core Functions", "Aggregation"),
    "countax.md": ("Core Functions", "Aggregation"),
    "countblank.md": ("Core Functions", "Aggregation"),
    "countrows.md": ("Core Functions", "Aggregation"),
    "countx.md": ("Core Functions", "Aggregation"),
    "max.md": ("Core Functions", "Aggregation"),
    "maxa.md": ("Core Functions", "Aggregation"),
    "maxx.md": ("Core Functions", "Aggregation"),
    "min.md": ("Core Functions", "Aggregation"),
    "mina.md": ("Core Functions", "Aggregation"),
    "minx.md": ("Core Functions", "Aggregation"),
    "product.md": ("Core Functions", "Aggregation"),
    "productx.md": ("Core Functions", "Aggregation"),
    "sum.md": ("Core Functions", "Aggregation"),
    "sumx.md": ("Core Functions", "Aggregation"),
    
    # --- Date & Time ---
    "date.md": ("Core Functions", "Date-Time"),
    "dateadd.md": ("Core Functions", "Date-Time"),
    "datediff.md": ("Core Functions", "Date-Time"),
    "datevalue.md": ("Core Functions", "Date-Time"),
    "day.md": ("Core Functions", "Date-Time"),
    "edate.md": ("Core Functions", "Date-Time"),
    "eomonth.md": ("Core Functions", "Date-Time"),
    "hour.md": ("Core Functions", "Date-Time"),
    "minute.md": ("Core Functions", "Date-Time"),
    "month.md": ("Core Functions", "Date-Time"),
    "now.md": ("Core Functions", "Date-Time"),
    "quarter.md": ("Core Functions", "Date-Time"),
    "second.md": ("Core Functions", "Date-Time"),
    "time.md": ("Core Functions", "Date-Time"),
    "timevalue.md": ("Core Functions", "Date-Time"),
    "today.md": ("Core Functions", "Date-Time"),
    "utcnow.md": ("Core Functions", "Date-Time"),
    "utctoday.md": ("Core Functions", "Date-Time"),
    "weekday.md": ("Core Functions", "Date-Time"),
    "weeknum.md": ("Core Functions", "Date-Time"),
    "year.md": ("Core Functions", "Date-Time"),
    "yearfrac.md": ("Core Functions", "Date-Time"),
    "calendar.md": ("Core Functions", "Date-Time"),
    "calendarauto.md": ("Core Functions", "Date-Time"),

    # --- Filter ---
    "all.md": ("Core Functions", "Filter"),
    "allcrossfiltered.md": ("Core Functions", "Filter"),
    "allexcept.md": ("Core Functions", "Filter"),
    "allnoblankrow.md": ("Core Functions", "Filter"),
    "allselected.md": ("Core Functions", "Filter"),
    "calculate.md": ("Core Functions", "Filter"),
    "calculatetable.md": ("Core Functions", "Filter"),
    "filter.md": ("Core Functions", "Filter"),
    "hasonefilter.md": ("Core Functions", "Filter"),
    "hasonevalue.md": ("Core Functions", "Filter"),
    "iscrossfiltered.md": ("Core Functions", "Filter"),
    "isfiltered.md": ("Core Functions", "Filter"),
    "isinscope.md": ("Core Functions", "Filter"),
    "issubtotal.md": ("Core Functions", "Filter"),
    "keepfilters.md": ("Core Functions", "Filter"),
    "removefilters.md": ("Core Functions", "Filter"),
    "selectedvalue.md": ("Core Functions", "Filter"),
    "treatas.md": ("Core Functions", "Filter"),

    # --- Financial (Huge list from your folder) ---
    "accrint.md": ("Core Functions", "Financial"),
    "accrintm.md": ("Core Functions", "Financial"),
    "amordegrc.md": ("Core Functions", "Financial"),
    "amorlinc.md": ("Core Functions", "Financial"),
    "coupdaybs.md": ("Core Functions", "Financial"),
    "coupdays.md": ("Core Functions", "Financial"),
    "coupdaysnc.md": ("Core Functions", "Financial"),
    "coupncd.md": ("Core Functions", "Financial"),
    "coupnum.md": ("Core Functions", "Financial"),
    "couppcd.md": ("Core Functions", "Financial"),
    "cumipmt.md": ("Core Functions", "Financial"),
    "cumprinc.md": ("Core Functions", "Financial"),
    "db.md": ("Core Functions", "Financial"),
    "ddb.md": ("Core Functions", "Financial"),
    "disc.md": ("Core Functions", "Financial"),
    "dollarde.md": ("Core Functions", "Financial"),
    "dollarfr.md": ("Core Functions", "Financial"),
    "duration.md": ("Core Functions", "Financial"),
    "effect.md": ("Core Functions", "Financial"),
    "fv.md": ("Core Functions", "Financial"),
    "intrate.md": ("Core Functions", "Financial"),
    "ipmt.md": ("Core Functions", "Financial"),
    "ispmt.md": ("Core Functions", "Financial"),
    "mduration.md": ("Core Functions", "Financial"),
    "nominal.md": ("Core Functions", "Financial"),
    "nper.md": ("Core Functions", "Financial"),
    "oddfprice.md": ("Core Functions", "Financial"),
    "oddfyield.md": ("Core Functions", "Financial"),
    "oddlprice.md": ("Core Functions", "Financial"),
    "oddlyield.md": ("Core Functions", "Financial"),
    "pduration.md": ("Core Functions", "Financial"),
    "pmt.md": ("Core Functions", "Financial"),
    "ppmt.md": ("Core Functions", "Financial"),
    "price.md": ("Core Functions", "Financial"),
    "pricedisc.md": ("Core Functions", "Financial"),
    "pricemat.md": ("Core Functions", "Financial"),
    "pv.md": ("Core Functions", "Financial"),
    "rate.md": ("Core Functions", "Financial"),
    "received.md": ("Core Functions", "Financial"),
    "rri.md": ("Core Functions", "Financial"),
    "sln.md": ("Core Functions", "Financial"),
    "syd.md": ("Core Functions", "Financial"),
    "tbilleq.md": ("Core Functions", "Financial"),
    "tbillprice.md": ("Core Functions", "Financial"),
    "tbillyield.md": ("Core Functions", "Financial"),
    "vdb.md": ("Core Functions", "Financial"),
    "xirr.md": ("Core Functions", "Financial"),
    "xnpv.md": ("Core Functions", "Financial"),
    "yield.md": ("Core Functions", "Financial"),
    "yielddisc.md": ("Core Functions", "Financial"),
    "yieldmat.md": ("Core Functions", "Financial"),

    # --- Information ---
    "contains.md": ("Core Functions", "Information"),
    "containsrow.md": ("Core Functions", "Information"),
    "containsstring.md": ("Core Functions", "Information"),
    "customdata.md": ("Core Functions", "Information"),
    "isblank.md": ("Core Functions", "Information"),
    "iserror.md": ("Core Functions", "Information"),
    "iseven.md": ("Core Functions", "Information"),
    "islogical.md": ("Core Functions", "Information"),
    "isnumber.md": ("Core Functions", "Information"),
    "isodd.md": ("Core Functions", "Information"),
    "istext.md": ("Core Functions", "Information"),
    "username.md": ("Core Functions", "Information"),
    "userprincipalname.md": ("Core Functions", "Information"),
    "lookupvalue.md": ("Core Functions", "Information"), # Often considered Info/Filter

    # --- Logical ---
    "and.md": ("Core Functions", "Logical"),
    "false.md": ("Core Functions", "Logical"),
    "if.md": ("Core Functions", "Logical"),
    "iferror.md": ("Core Functions", "Logical"),
    "not.md": ("Core Functions", "Logical"),
    "or.md": ("Core Functions", "Logical"),
    "switch.md": ("Core Functions", "Logical"),
    "true.md": ("Core Functions", "Logical"),
    "coalesce.md": ("Core Functions", "Logical"),

    # --- Math & Trig (Moved ABS here as per MS Standard) ---
    "abs.md": ("Core Functions", "Math-Trig"),
    "acos.md": ("Core Functions", "Math-Trig"),
    "acosh.md": ("Core Functions", "Math-Trig"),
    "acot.md": ("Core Functions", "Math-Trig"),
    "acoth.md": ("Core Functions", "Math-Trig"),
    "asin.md": ("Core Functions", "Math-Trig"),
    "asinh.md": ("Core Functions", "Math-Trig"),
    "atan.md": ("Core Functions", "Math-Trig"),
    "atanh.md": ("Core Functions", "Math-Trig"),
    "ceiling.md": ("Core Functions", "Math-Trig"),
    "combin.md": ("Core Functions", "Math-Trig"),
    "combina.md": ("Core Functions", "Math-Trig"),
    "cos.md": ("Core Functions", "Math-Trig"),
    "cosh.md": ("Core Functions", "Math-Trig"),
    "cot.md": ("Core Functions", "Math-Trig"),
    "coth.md": ("Core Functions", "Math-Trig"),
    "currency.md": ("Core Functions", "Math-Trig"),
    "degrees.md": ("Core Functions", "Math-Trig"),
    "divide.md": ("Core Functions", "Math-Trig"),
    "even.md": ("Core Functions", "Math-Trig"),
    "exp.md": ("Core Functions", "Math-Trig"),
    "fact.md": ("Core Functions", "Math-Trig"),
    "floor.md": ("Core Functions", "Math-Trig"),
    "gcd.md": ("Core Functions", "Math-Trig"),
    "int.md": ("Core Functions", "Math-Trig"),
    "iso-ceiling.md": ("Core Functions", "Math-Trig"),
    "lcm.md": ("Core Functions", "Math-Trig"),
    "ln.md": ("Core Functions", "Math-Trig"),
    "log.md": ("Core Functions", "Math-Trig"),
    "log10.md": ("Core Functions", "Math-Trig"),
    "mod.md": ("Core Functions", "Math-Trig"),
    "mround.md": ("Core Functions", "Math-Trig"),
    "odd.md": ("Core Functions", "Math-Trig"),
    "pi.md": ("Core Functions", "Math-Trig"),
    "power.md": ("Core Functions", "Math-Trig"),
    "quotient.md": ("Core Functions", "Math-Trig"),
    "radians.md": ("Core Functions", "Math-Trig"),
    "rand.md": ("Core Functions", "Math-Trig"),
    "randbetween.md": ("Core Functions", "Math-Trig"),
    "round.md": ("Core Functions", "Math-Trig"),
    "rounddown.md": ("Core Functions", "Math-Trig"),
    "roundup.md": ("Core Functions", "Math-Trig"),
    "sign.md": ("Core Functions", "Math-Trig"),
    "sin.md": ("Core Functions", "Math-Trig"),
    "sinh.md": ("Core Functions", "Math-Trig"),
    "sqrt.md": ("Core Functions", "Math-Trig"),
    "sqrtpi.md": ("Core Functions", "Math-Trig"),
    "tan.md": ("Core Functions", "Math-Trig"),
    "tanh.md": ("Core Functions", "Math-Trig"),
    "trunc.md": ("Core Functions", "Math-Trig"),

    # --- Statistical ---
    "beta-dist.md": ("Core Functions", "Statistical"),
    "beta-inv.md": ("Core Functions", "Statistical"),
    "chisq-dist.md": ("Core Functions", "Statistical"),
    "chisq-inv.md": ("Core Functions", "Statistical"),
    "confidence-norm.md": ("Core Functions", "Statistical"),
    "confidence-t.md": ("Core Functions", "Statistical"),
    "geomean.md": ("Core Functions", "Statistical"),
    "median.md": ("Core Functions", "Statistical"),
    "medianx.md": ("Core Functions", "Statistical"),
    "norm-dist.md": ("Core Functions", "Statistical"),
    "norm-inv.md": ("Core Functions", "Statistical"),
    "percentile-exc.md": ("Core Functions", "Statistical"),
    "percentile-inc.md": ("Core Functions", "Statistical"),
    "permut.md": ("Core Functions", "Statistical"),
    "poisson-dist.md": ("Core Functions", "Statistical"),
    "rank-eq.md": ("Core Functions", "Statistical"),
    "rankx.md": ("Core Functions", "Statistical"),
    "stdev-p.md": ("Core Functions", "Statistical"),
    "stdev-s.md": ("Core Functions", "Statistical"),
    "t-dist.md": ("Core Functions", "Statistical"),
    "t-inv.md": ("Core Functions", "Statistical"),
    
    # --- Text ---
    "blank.md": ("Core Functions", "Text"),
    "concatenate.md": ("Core Functions", "Text"),
    "concatenatex.md": ("Core Functions", "Text"),
    "exact.md": ("Core Functions", "Text"),
    "find.md": ("Core Functions", "Text"),
    "fixed.md": ("Core Functions", "Text"),
    "format.md": ("Core Functions", "Text"),
    "left.md": ("Core Functions", "Text"),
    "len.md": ("Core Functions", "Text"),
    "lower.md": ("Core Functions", "Text"),
    "mid.md": ("Core Functions", "Text"),
    "replace.md": ("Core Functions", "Text"),
    "rept.md": ("Core Functions", "Text"),
    "right.md": ("Core Functions", "Text"),
    "search.md": ("Core Functions", "Text"),
    "substitute.md": ("Core Functions", "Text"),
    "trim.md": ("Core Functions", "Text"),
    "unichar.md": ("Core Functions", "Text"),
    "unicode.md": ("Core Functions", "Text"),
    "upper.md": ("Core Functions", "Text"),
    "value.md": ("Core Functions", "Text"),

    # --- Time Intelligence ---
    "closingbalancemonth.md": ("Core Functions", "Time-Intelligence"),
    "closingbalancequarter.md": ("Core Functions", "Time-Intelligence"),
    "closingbalanceyear.md": ("Core Functions", "Time-Intelligence"),
    "datesmtd.md": ("Core Functions", "Time-Intelligence"),
    "datesqtd.md": ("Core Functions", "Time-Intelligence"),
    "datesytd.md": ("Core Functions", "Time-Intelligence"),
    "endofmonth.md": ("Core Functions", "Time-Intelligence"),
    "firstdate.md": ("Core Functions", "Time-Intelligence"),
    "lastdate.md": ("Core Functions", "Time-Intelligence"),
    "openingbalancemonth.md": ("Core Functions", "Time-Intelligence"),
    "parallelperiod.md": ("Core Functions", "Time-Intelligence"),
    "sameperiodlastyear.md": ("Core Functions", "Time-Intelligence"),
    "startofmonth.md": ("Core Functions", "Time-Intelligence"),
    "totalmtd.md": ("Core Functions", "Time-Intelligence"),
    "totalqtd.md": ("Core Functions", "Time-Intelligence"),
    "totalytd.md": ("Core Functions", "Time-Intelligence"),
    
    # --- Table Manipulation ---
    "addcolumns.md": ("Core Functions", "Table-Manipulation"),
    "crossjoin.md": ("Core Functions", "Table-Manipulation"),
    "distinct.md": ("Core Functions", "Table-Manipulation"),
    "except.md": ("Core Functions", "Table-Manipulation"),
    "generate.md": ("Core Functions", "Table-Manipulation"),
    "groupby.md": ("Core Functions", "Table-Manipulation"),
    "intersect.md": ("Core Functions", "Table-Manipulation"),
    "naturalinnerjoin.md": ("Core Functions", "Table-Manipulation"),
    "row.md": ("Core Functions", "Table-Manipulation"),
    "selectcolumns.md": ("Core Functions", "Table-Manipulation"),
    "summarize.md": ("Core Functions", "Table-Manipulation"),
    "summarizecolumns.md": ("Core Functions", "Table-Manipulation"),
    "topn.md": ("Core Functions", "Table-Manipulation"),
    "union.md": ("Core Functions", "Table-Manipulation"),
    "values.md": ("Core Functions", "Table-Manipulation"),

    # --- Other / Parent-Child / Bitwise ---
    "path.md": ("Core Functions", "Parent-Child"),
    "pathcontains.md": ("Core Functions", "Parent-Child"),
    "pathitem.md": ("Core Functions", "Parent-Child"),
    "pathlength.md": ("Core Functions", "Parent-Child"),
    "bitand.md": ("Core Functions", "Bitwise"),
    "bitor.md": ("Core Functions", "Bitwise"),
    "bitxor.md": ("Core Functions", "Bitwise"),
    "bitlshift.md": ("Core Functions", "Bitwise"),
    "bitrshift.md": ("Core Functions", "Bitwise"),
    "related.md": ("Core Functions", "Relationship"),
    "relatedtable.md": ("Core Functions", "Relationship"),
    "userelationship.md": ("Core Functions", "Relationship"),
}

# ==========================================
# 3. HELPER FUNCTION: HEURISTICS
# ==========================================
def get_category_heuristic(filename):
    """Fallback if not in dictionary"""
    f = filename.lower()
    if f.startswith("is"): return ("Core Functions", "Information")
    if "date" in f or "day" in f or "year" in f: return ("Core Functions", "Date-Time")
    if "filter" in f: return ("Core Functions", "Filter")
    if "path" in f: return ("Core Functions", "Parent-Child")
    if "join" in f or "table" in f: return ("Core Functions", "Table-Manipulation")
    if "dist" in f or "norm" in f or "rank" in f: return ("Core Functions", "Statistical")
    return ("Core Functions", "Other") # Stay where it is if we really don't know

# ==========================================
# 4. EXECUTION
# ==========================================
def organize_files():
    if not source_folder.exists():
        print(f"❌ CRITICAL ERROR: Source folder not found: {source_folder}")
        return

    files = list(source_folder.glob("*.md"))
    print(f"🔍 Found {len(files)} files to organize.")
    
    moved_count = 0
    
    for file_path in files:
        filename = file_path.name.lower()
        original_filename = file_path.name
        
        # Determine Destination
        if filename in categorization:
            cat, subcat = categorization[filename]
        else:
            cat, subcat = get_category_heuristic(filename)
            
        # If heuristics say "Other", and it's already in "Other", skip it
        if subcat == "Other" and file_path.parent.name == "Other":
            print(f"⏩ Skipping {original_filename} (Cannot identify category)")
            continue

        # Build path: Root/Core Functions/Subcategory
        if subcat:
            dest_dir = root_base / cat / subcat
        else:
            dest_dir = root_base / cat

        # Move
        try:
            dest_dir.mkdir(parents=True, exist_ok=True)
            dest_file = dest_dir / original_filename
            
            # Handle collision
            if dest_file.exists():
                print(f"⚠️ File exists at destination: {original_filename}. Skipping.")
                continue
                
            shutil.move(str(file_path), str(dest_file))
            moved_count += 1
            if moved_count % 20 == 0:
                print(f"✅ Moved {moved_count} files...")
                
        except Exception as e:
            print(f"❌ Error moving {original_filename}: {e}")

    print("="*50)
    print(f"🎉 OPERATION COMPLETE. Moved {moved_count} files.")
    print("="*50)

# Run it
organize_files()