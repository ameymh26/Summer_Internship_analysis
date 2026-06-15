import pandas as pd
from pathlib import Path

# Root folder containing folders 100, 101, ..., 111
root = Path(r"C:\Users\Amey\Desktop\Amey\Python")

all_dfs = []

# ==========================================
# Read all Excel files
# ==========================================

for pcb_folder in root.iterdir():

    if pcb_folder.is_dir():

        excel_files = list(pcb_folder.glob("*.xlsx"))

        if not excel_files:
            print(f"No Excel file found in {pcb_folder.name}")
            continue

        df = pd.read_excel(excel_files[0])

        all_dfs.append(df)

# ==========================================
# Combine all files
# ==========================================

combined_df = pd.concat(all_dfs, ignore_index=True)

# ==========================================
# Fix Month Column
# Handles both:
#   2020-01 -> 1
#   1 -> 1
# ==========================================

combined_df["Month"] = combined_df["Month"].astype(str)

mask = combined_df["Month"].str.contains("-", na=False)

combined_df.loc[mask, "Month"] = (
    combined_df.loc[mask, "Month"]
    .str.split("-")
    .str[1]
)

combined_df["Month"] = pd.to_numeric(
    combined_df["Month"],
    errors="coerce"
)

# Check for problematic rows
if combined_df["Month"].isna().sum() > 0:
    print("\nInvalid Month Values Found:")
    print(
        combined_df.loc[
            combined_df["Month"].isna(),
            ["Month"]
        ].drop_duplicates()
    )

combined_df["Month"] = combined_df["Month"].astype("Int64")

# ==========================================
# Validation
# ==========================================

print("\nCombined Shape:")
print(combined_df.shape)

print("\nMaterials:")
print(sorted(combined_df["Material"].unique()))

print("\nNumber of Materials:")
print(combined_df["Material"].nunique())

print("\nYears:")
print(sorted(combined_df["Year"].dropna().unique()))

print("\nMonths:")
print(sorted(combined_df["Month"].dropna().unique()))

# ==========================================
# Save Combined File
# ==========================================

output_file = root / "All_PCBs_Combined.xlsx"

combined_df.to_excel(
    output_file,
    index=False
)

print("\nFile saved successfully!")
print(output_file)