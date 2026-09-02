data_dir = Path("data")# recover_missing_markers.py
import scanpy as sc
import anndata as ad
import numpy as np
from pathlib import Path
import gc

sc.settings.verbosity = 3

data_dir = Path("data")
sample_dirs = sorted([p for p in data_dir.iterdir() if p.is_dir() and (p / "matrix.mtx.gz").exists()])

adatas = {}
for sample_path in sample_dirs:
    sample_name = sample_path.name
    a = sc.read_10x_mtx(path=sample_path, var_names="gene_symbols", cache=False)
    parts = sample_name.split("_")
    a.obs["sample"] = sample_name
    a.obs["sex"] = parts[0]
    a.obs["treatment"] = parts[1]
    a.obs["replicate"] = parts[2]
    a.obs["condition"] = f"{parts[0]}_{parts[1]}"
    sc.pp.filter_cells(a, min_genes=200)
    sc.pp.filter_genes(a, min_cells=3)
    adatas[sample_name] = a

adata_full = ad.concat(adatas, label="sample_batch", index_unique="-", join="outer", fill_value=0)
adata_full.var_names_make_unique()
adata_full = adata_full[:, adata_full.var_names.notna()].copy()
del adatas
gc.collect()

adata_full.var["mt"] = adata_full.var_names.astype(str).str.startswith("mt:")
sc.pp.calculate_qc_metrics(adata_full, qc_vars=["mt"], percent_top=None, log1p=False, inplace=True)
adata_full = adata_full[adata_full.obs["pct_counts_mt"] < 10.0, :].copy()

sc.pp.normalize_total(adata_full, target_sum=1e4)
sc.pp.log1p(adata_full)

# Only keep the two missing marker genes + cell barcodes — discard everything else immediately
markers_needed = ["elav", "VGlut"]
found = [g for g in markers_needed if g in adata_full.var_names]
print(f"Found: {found}")

marker_expr = adata_full[:, found].to_df()
marker_expr.to_csv("results/tables/recovered_markers.csv")
print("Saved recovered marker expression to results/tables/recovered_markers.csv")
