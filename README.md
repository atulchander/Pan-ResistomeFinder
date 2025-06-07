# Pan-ResistomeFinder

**Pan-ResistomeFinder** is a tool for automated extraction of stress-response and resistance genes across one or more annotated microbial genomes. It supports spreadsheets exported from annotation platforms and identifies functional genes using a curated set of biological keywords.

## 🔍 Features

- ✅ Detects stress-related and resistance-associated genes using flexible keyword filtering
- ✅ Supports `.tsv`, `.csv`, `.xls`, and `.xlsx` formats
- ✅ Automatically merges multi-organism gene tables into a unified presence/absence matrix
- ✅ Works on both single-genome and pan-genome datasets
- ✅ Designed for use in Google Colab or local Python environments

---

## 📥 Input Requirements

To use Pan-ResistomeFinder, prepare the following:

- **File formats supported:**  
  `.tsv`, `.csv`, `.xls`, `.xlsx`
  Each files should be saved in single folder after the name of organism for better annotated compiled results.

- **Required columns (case-sensitive):**  
  `Category`, `Subcategory`, `Subsystem`, and `Role`

- **Input content:**  
  The tool expects spreadsheet-formatted genomic annotations. It has been tested primarily on output files exported from **RAST** (Rapid Annotations using Subsystems Technology).

- **Single-genome support:**  
  If only one file is provided, the tool performs resistome discovery on that dataset.

- **Multi-genome (pangenome) support:**  
  When multiple files are found in the input folder, the tool merges the data into a presence-absence matrix. 

> ℹ️ While this tool currently supports RAST-annotated spreadsheets, collaboration is welcome to extend support to other annotation outputs.

---

## 🚀 How to Use

1. Clone or download the repository.
2. Place all your annotated genome spreadsheets into a folder (e.g. `ANNOTATIONs/`).
3. Run the script in a Python environment (e.g., Google Colab or locally via terminal).
4. Provide the folder path when prompted.

---

## 📤 Output

- `Full_Merged_Gene_Presence_Matrix.csv`  
  → Combined matrix of all annotated roles across strains

- `Resistome_output.csv`  
  → Filtered table containing only stress-response/resistance genes

---

## 🤝 Collaboration

We welcome collaborations to:
- Expand keyword libraries
- Support annotations from other tools (e.g., Prokka, PGAP)
- Integrate additional resistome prediction layers

---

## License

This project is currently private. Reach out to the authors for access or contribution.

