# Drosophila Brain Cocaine Response — Single-Cell RNA-seq Analysis

**Group 2 — Project 2**

**Group Leader:** Tanvir Ahmed ([@tanvirahmed-dr](https://github.com/tanvirahmed-dr))  
**Team Members:** Mantuka Masnoon Umama, Sharfuddin Safin, Tasnim Haque Achal, Suriya Akther, Mahi Kabir Chowdhury, Nahid Hasan, Mobin Ibne Mokbul, Md. Tariqul Islam, Nowshin Tarannum Adriana

## Abstract

This project reanalyzes single-cell RNA-sequencing data from Baker et al. (GEO: GSE152495), profiling the *Drosophila melanogaster* brain following cocaine versus sucrose exposure across both sexes. The dataset contains 8 biological samples: Female/Male × Cocaine/Sucrose × 2 replicates. We reproduce a whole-brain single-cell atlas, annotate major neuronal and glial populations using canonical markers, and test cocaine-responsive transcriptional changes with sample-level pseudobulk differential expression. A full 2×2 sex-by-treatment model is used to test the sex × treatment interaction directly.

## Key Findings

- **Final dataset:** 88,922 cells and 11,946 genes after the QC/normalization workflow.
- **Clustering:** Leiden clustering was evaluated at resolutions 0.5, 0.8, 1.0, and 1.2. The final analysis uses **resolution 0.8 with 29 clusters**. A 5,000-cell fixed sample was used for quantitative silhouette assessment in PCA space; the corresponding silhouette scores are retained in `results/tables/clustering_resolution_comparison.csv`.
- **Cell-type annotation:** 9 of 10 canonical markers were recovered (`repo`, `elav`, `ey`, `Fas2`, `VAChT`, `Gad1`, `ple`, `SerT`, `Tdc2`); `VGlut` was not found. These markers support annotation of major glial, Kenyon-cell, and neurotransmitter-associated neuronal populations.
- **Differential expression:** DE was revised from cell-level testing to **sample-level pseudobulk analysis** using all retained genes passing the count filter. The full design is `~ sex + treatment + sex:treatment` and is fitted with PyDESeq2/DESeq2-style negative-binomial modelling.
  - Female cocaine vs sucrose: **246** genes meeting FDR < 0.05 and |log2FC| ≥ 1.
  - Male cocaine vs sucrose: **109** genes meeting FDR < 0.05 and |log2FC| ≥ 1.
  - Sex × treatment interaction: **46** genes meeting FDR < 0.05 and |log2FC| ≥ 1.
- **Fold-change integrity:** 9,557 genes were tested in each contrast and **0 non-finite log2FC values** remained in the final tables.
- **Pathway enrichment:** FlyBase loss-of-function phenotype enrichment was tested separately for male and female significant DE gene sets. **No enrichment terms passed adjusted p < 0.05** in either sex. Complete, significant, and non-significant enrichment tables are retained for transparency.

The male and female significant-gene counts are descriptive summaries. They are not treated as a statistical test of a sex difference; the **sex × treatment interaction** is the direct inferential test of whether the cocaine response differs between sexes.

## Repository Structure

```text
scproject2-drosophila-brain/
├── notebooks/
│   ├── 01_data_loading_qc.ipynb          # Load 8 samples, QC, filtering, normalization
│   ├── 02_clustering_annotation.ipynb     # PCA, Leiden clustering, marker annotation
│   └── 03_de_pathway_analysis.ipynb       # Pseudobulk DE, interaction testing, enrichment
├── scripts/                               # Standalone .py versions / utility scripts
├── results/
│   ├── figures/                           # Final QC, UMAP, marker, and volcano figures
│   └── tables/                            # DE, interaction, clustering, QC, and enrichment tables
├── report/
│   └── report.md                          # Full write-up
├── peer_review/                           # Review/rebuttal materials
├── data/                                  # Raw data (not tracked — see data/README.md)
└── requirements.txt
```

## Main Results Files

### Figures

- `fig1_qc_summary.png` — QC summary
- `fig2_umap_condition.png` — UMAP by experimental condition
- `fig2_umap_leiden.png` — final Leiden clustering at resolution 0.8
- `fig3_marker_dotplot.png` — canonical marker expression
- `fig3_umap_cell_types.png` — cell-type annotation UMAP
- `fig4_volcano_female.png` — female cocaine vs sucrose
- `fig4_volcano_male.png` — male cocaine vs sucrose
- `fig4_volcano_interaction.png` — sex × treatment interaction

No enrichment figure is generated when there are no significant enrichment terms. The enrichment results remain available as CSV tables.

### Key tables

- `FINAL_REVISED_ANALYSIS_SUMMARY.csv`
- `fold_change_audit.csv`
- `clustering_resolution_comparison.csv`
- `pseudobulk_DE_female_cocaine_vs_sucrose.csv`
- `pseudobulk_DE_male_cocaine_vs_sucrose.csv`
- `pseudobulk_DE_sex_by_treatment_interaction.csv`
- `female_pathway_enrichment_all.csv`
- `female_pathway_enrichment_significant.csv`
- `female_pathway_enrichment_nonsignificant.csv`
- `male_pathway_enrichment_all.csv`
- `male_pathway_enrichment_significant.csv`
- `male_pathway_enrichment_nonsignificant.csv`

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

# Run the notebooks in order:
# 01_data_loading_qc.ipynb
# 02_clustering_annotation.ipynb
# 03_de_pathway_analysis.ipynb
```

For memory-constrained machines, the notebooks can be converted to scripts and executed sequentially.

## Methodology Notes

- **Per-sample filtering** (`min_genes=200`, `min_cells=3`) was applied before merging the 8 samples to reduce peak memory use.
- Mitochondrial content was calculated using the Drosophila-specific `mt:` prefix, and cells above the 10% mitochondrial threshold were excluded.
- Genes with missing/`NaN` symbols in the Drosophila 10x reference were removed prior to downstream analysis.
- Counts were normalized to 10,000 reads per cell and log-transformed. The top 2,000 HVGs were used for scaling/PCA/neighborhood construction; **DE was not restricted to HVGs**.
- `regress_out` was skipped because of memory constraints on the 8GB analysis environment.
- Leiden resolutions 0.5, 0.8, 1.0, and 1.2 were quantitatively compared using a reproducible 5,000-cell silhouette sample in PCA space. Resolution 0.8 was retained as the final clustering resolution.
- Differential expression uses **raw counts aggregated within each biological sample**. The inferential unit is therefore the biological sample rather than the individual cell.
- The DE model uses the full 2×2 design `~ sex + treatment + sex:treatment`. Female treatment, male treatment, and the sex × treatment interaction are extracted as separate contrasts.
- Significance is defined in the final tables as Benjamini–Hochberg adjusted p < 0.05 together with |log2FC| ≥ 1.
- Low-count filtering and fold-change integrity are documented in `low_count_filter_summary.csv` and `fold_change_audit.csv`.
- Pathway enrichment uses the fly-specific `Allele_LoF_Phenotypes_from_FlyBase_2017` Enrichr library and reports significant and non-significant terms separately.

## Interpretation of the Revised DE Analysis

The revised analysis should not use the former cell-level result of “50 male vs 46 female genes” or the associated 1.09 ratio. Those values came from the previous workflow and are no longer the final results.

The current analysis identifies 246 significant female treatment-response genes, 109 significant male treatment-response genes, and 46 significant sex × treatment interaction genes under the stated thresholds. The first two counts describe treatment-associated changes within each sex; the interaction contrast tests whether the treatment effect differs between males and females.

## AI Usage Disclosure

Portions of this pipeline's code (Scanpy workflow structure, debugging of memory/dependency errors, plotting adjustments, and computational workflow development) were developed with assistance from Claude (Anthropic). Analysis code was reviewed and executed by the group leader before inclusion. Design decisions such as QC thresholds, clustering resolution, and memory-related omissions were made based on the observed analysis outputs.

## License

MIT — see `LICENSE`.
