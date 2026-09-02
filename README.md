# Drosophila Brain Cocaine Response — Single-Cell RNA-seq Analysis

**Group 2 — Project 2**

**Group Leader:** Tanvir Ahmed ([@tanvirahmed-dr](https://github.com/tanvirahmed-dr))
**Team Members:** Mantuka Masnoon Umama, Sharfuddin Safin, Tasnim Haque Achal, Suriya Akther, Mahi Kabir Chowdhury, Nahid Hasan, Mobin Ibne Mokbul, Md. Tariqul Islam, Nowshin Tarannum Adriana

## Abstract

This project reanalyzes single-cell RNA-sequencing data from Bainton et al. (GEO: GSE152495), profiling the *Drosophila melanogaster* brain following cocaine versus sucrose exposure across both sexes (8 samples: Female/Male × Cocaine/Sucrose × 2 replicates). We reproduce the original cell-clustering atlas, annotate major neuronal and glial populations using canonical markers, and test for sex-biased transcriptional changes in response to cocaine exposure.

## Key Findings

- **Clustering:** Identified **28 clusters** at Leiden resolution 0.8 (paper reports ~36; resolutions 1.0 and 1.2 were also tested, yielding 35 and 37 clusters respectively — see Methods for the resolution selection rationale).
- **Cell-type annotation:** 7 of 9 canonical markers (`repo`, `ey`, `Fas2`, `VAChT`, `Gad1`, `ple`, `SerT`, `Tdc2`) were recovered within the top 2000 highly variable genes and used to annotate glial, Kenyon cell, cholinergic, GABAergic, dopaminergic, serotonergic, and octopaminergic populations.
- **Differential expression (Cocaine vs. Sucrose):**
  - Male: **50** significant DE genes (|log2FC| > 1, adj. p < 0.05)
  - Female: **46** significant DE genes
  - Male/Female ratio: **1.09** — a milder sex-biased response than reported in the original study, discussed further in `report/report.md`.
- **Pathway enrichment:** FlyBase Loss-of-Function phenotype enrichment (Enrichr) performed separately for male and female DE gene sets.

## Repository Structure

```
scproject2-drosophila-brain/
├── notebooks/
│   ├── 01_data_loading_qc.ipynb          # Load 8 samples, QC, filtering, normalization
│   ├── 02_clustering_annotation.ipynb    # PCA, Leiden clustering, marker annotation
│   └── 03_de_pathway_analysis.ipynb      # DE testing + pathway enrichment
├── scripts/                               # Standalone .py versions for memory-safe execution
├── results/
│   ├── figures/                           # Figures 1–5
│   └── tables/                            # DE gene lists, pathway enrichment results
├── report/
│   └── report.md                          # Full write-up
├── peer_review/                           # Review received + rebuttal
├── data/                                  # Raw data (not tracked — see data/README.md)
└── requirements.txt
```

## Quickstart

```bash
git clone https://github.com/tanvirahmed-dr/scproject2-drosophila-brain.git
cd scproject2-drosophila-brain

# Set up environment
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt

# Data: place the 8 sample folders (Female_Cocaine_1, Male_Sucrose_2, etc.)
# from GSE152495 into data/ — see data/README.md for details.

# Run the pipeline (recommended: as scripts, for memory-constrained machines)
jupyter nbconvert --to script notebooks/01_data_loading_qc.ipynb --output-dir scripts/
python scripts/01_data_loading_qc.py
# repeat for 02_clustering_annotation and 03_de_pathway_analysis
```

## Methodology Notes

- **`regress_out` was skipped** during normalization due to memory constraints (8GB RAM environment); PCA and the neighbor graph were relied upon to absorb residual technical variance instead.
- **Per-sample filtering** (`min_genes=200`, `min_cells=3`) was applied before merging the 8 samples, rather than after, to reduce peak memory usage during concatenation.
- Genes with missing/`NaN` symbols in the Drosophila 10x reference were removed prior to downstream analysis.
- Pathway enrichment used the `Allele_LoF_Phenotypes_from_FlyBase_2017` Enrichr library (fly-specific), since human-organism library names are not valid for this organism.

## AI Usage Disclosure

Portions of this pipeline's code (Scanpy workflow structure, debugging of memory/dependency errors, plotting adjustments) were developed with the assistance of Claude (Anthropic). See `report/report.md` Appendix for full disclosure details including specific prompts and purposes, per the project's Academic Integrity policy.

## License

MIT — see `LICENSE`.
