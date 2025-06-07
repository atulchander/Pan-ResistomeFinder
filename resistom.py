import os
import glob
import re
import pandas as pd

def load_annotation_file(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == '.tsv':
        df = pd.read_csv(path, sep='\t', dtype=str)
    elif ext == '.csv':
        df = pd.read_csv(path, dtype=str)
    elif ext in ('.xls', '.xlsx'):
        df = pd.read_excel(path, dtype=str)
    else:
        return None
    required = ["Category", "Subcategory", "Subsystem", "Role"]
    if not all(col in df.columns for col in required):
        raise ValueError(f"Missing required columns in {path}")
    df = df[required].dropna(how='all').copy()
    return df

def merge_annotations(directory):
    patterns = ["*.tsv", "*.csv", "*.xls", "*.xlsx"]
    files = []
    for pat in patterns:
        files.extend(glob.glob(os.path.join(directory, pat)))
    if not files:
        raise FileNotFoundError(f"No annotation files found in {directory}")
    dfs = []
    for path in sorted(files):
        strain = os.path.splitext(os.path.basename(path))[0]
        print(f"Loading {strain} from {path}")
        df = load_annotation_file(path)
        df[strain] = 1
        dfs.append(df)
    if len(dfs) == 1:
        print("Only one file found; skipping merge and using single annotation DataFrame.")
        merged = dfs[0]
    else:
        merged = dfs[0]
        for df in dfs[1:]:
            merged = pd.merge(merged, df, on=["Category", "Subcategory", "Subsystem", "Role"], how="outer")
    merged.fillna(0, inplace=True)
    presence_cols = [c for c in merged.columns if c not in ["Category", "Subcategory", "Subsystem", "Role"]]
    merged[presence_cols] = merged[presence_cols].astype(int)
    return merged

def resistome_search(df):
    keywords = [
        "resist", "stress", "efflux", "permease", "peroxide",
        "sod", "superoxide", "heat shock", "shock", "chaperone",
        "cold shock", "redox", "katG", "ahp", "dnaK", "groEL",
        "recA", "soxR", "dps", "lexA", "SOS", "hypoxia",
        "toxin", "detox", "thioredoxin", "glutaredoxin",
        "reduct", "transport", "DNA repair", "repair"
    ]
    pattern = r'(' + '|'.join(re.escape(k) for k in keywords) + r')'
    combined = (
        df['Category'].fillna('') + ' ' +
        df['Subcategory'].fillna('') + ' ' +
        df['Subsystem'].fillna('') + ' ' +
        df['Role'].fillna('')
    )
    mask = combined.str.contains(pattern, flags=re.IGNORECASE, regex=True, na=False)
    return df[mask].copy()

from google.colab import drive
drive.mount('/content/drive')

user_input = input("Enter path to your annotation folder (e.g. /content/drive/MyDrive/ANNOTATIONs):\n").strip()

if not os.path.isdir(user_input):
    print(f"Folder does not exist: {user_input}")
else:
    try:
        merged = merge_annotations(user_input)
        merged_path = os.path.join(user_input, "Full_Merged_Gene_Presence_Matrix.csv")
        merged.to_csv(merged_path, index=False)
        print(f"Saved merged matrix to: {merged_path}")

        filtered = resistome_search(merged)
        out_path = os.path.join(user_input, "Resistome_output.csv")
        filtered.to_csv(out_path, index=False)
        print(f"Saved resistome filter results to: {out_path}")
        print(f"Total entries: {filtered.shape[0]}, Unique roles: {filtered['Role'].nunique()}")
    except Exception as e:
        print("Error:", e)

