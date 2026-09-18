# Author Rebuttal Response

## Paper Title

**Single-Cell Transcriptomics of the Drosophila Brain Under Cocaine Exposure**

## GitHub Repository

https://github.com/tanvirahmed-dr/scproject2-drosophila-brain

We thank the reviewer for the detailed and constructive assessment of our project. The review identified several important methodological and reproducibility issues in the original analysis. We have substantially revised the computational workflow in response to these comments.

The most important revision was replacement of the original cell-level differential-expression analysis with a **sample-level pseudobulk analysis** using the eight biological samples and an explicit **2 × 2 sex-by-treatment model**. We also expanded differential-expression testing beyond the 2,000 highly variable genes, added fold-change integrity auditing, regenerated the final differential-expression and enrichment outputs, added sample-level QC information, quantitatively compared clustering resolutions, and updated the README and report.

The final analysis contains **88,922 cells and 11,946 genes** after the QC/normalization workflow. The pseudobulk analysis tested **9,557 genes**. Under the predefined criteria of BH-adjusted p < 0.05 and |log2FC| ≥ 1, we identified **246 female treatment-response genes, 109 male treatment-response genes, and 46 genes with a significant sex × treatment interaction**.

We respond to each reviewer comment below.

---

# PART 4: MAJOR COMMENTS & METHODOLOGICAL CONCERNS

## 1. The complete pipeline could not be reproduced

**Reviewer comment:**
The data-loading notebook could not proceed beyond the sample-loading step, and the necessary raw data/intermediate files were not available in a form that allowed end-to-end reproduction.

**Response:**
We agree that reproducibility was insufficient in the earlier version and have revised the repository structure and documentation accordingly.

The final repository provides:

* the three analysis notebooks in execution order;
* the eight expected sample directories;
* a `data/README.md` describing the raw-data organization;
* the required Python packages in `requirements.txt`;
* the generated intermediate `.h5ad` objects;
* final figures and tables;
* sample metadata and QC cell-count information;
* the revised pseudobulk differential-expression results;
* the fold-change integrity audit;
* clustering-resolution comparison results; and
* an updated README describing the data organization and execution order.

The expected workflow is now explicitly documented as:

1. Obtain the eight samples from GEO GSE152495.
2. Place the samples in the corresponding directories under `data/`.
3. Create the environment and install the requirements.
4. Run Notebook 1.
5. Run Notebook 2.
6. Run Notebook 3.

We also corrected the study attribution in the revised documentation. The dataset is **GEO GSE152495**, corresponding to the Drosophila cocaine single-cell study by Baker et al.

We acknowledge that the reviewer was unable to independently complete the entire pipeline during the original review. We therefore do not claim independent reproduction by the reviewer. Instead, we have addressed the identified reproducibility problems by making the expected data organization, execution order, intermediate outputs, final outputs, and analysis assumptions explicit.

---

## 2. Differential expression appears to be performed on scaled data

**Reviewer comment:**
The original workflow appeared to use scaled expression for differential expression, making the reported fold changes difficult to interpret.

**Response:**
We agree with this concern and replaced the original cell-level differential-expression workflow.

The final differential-expression analysis is **not performed on the scaled expression matrix**. Instead, raw counts are aggregated across cells within each biological sample to generate a sample-by-gene pseudobulk count matrix.

The pseudobulk counts are analysed using a DESeq2-style negative-binomial framework implemented with PyDESeq2.

The final model is:

`~ sex + treatment + sex:treatment`

Female treatment, male treatment, and the sex × treatment interaction are extracted as separate contrasts.

The final repository also contains `fold_change_audit.csv`. For each of the three contrasts, 9,557 genes were tested and **zero non-finite log2FC values** were present in the final result tables.

This revision removes the previous ambiguity concerning fold changes derived from scaled expression.

---

## 3. Differential expression is restricted to 2,000 highly variable genes

**Reviewer comment:**
DE should not be restricted to the 2,000 HVGs used for dimensionality reduction and clustering.

**Response:**
We agree and have corrected this.

The 2,000 HVGs remain part of the dimensionality-reduction and clustering workflow, but the differential-expression analysis is **not restricted to the HVGs**.

For pseudobulk DE, genes are retained following the count-based filtering step. The final analysis tested **9,557 genes**.

The corresponding final result files are:

* `pseudobulk_DE_female_cocaine_vs_sucrose.csv`
* `pseudobulk_DE_male_cocaine_vs_sucrose.csv`
* `pseudobulk_DE_sex_by_treatment_interaction.csv`

Therefore, genes outside the HVG set were eligible for differential-expression testing.

---

## 4. Potential consideration of cells as independent replicates

**Reviewer comment:**
The original analysis compared individual cells despite the experiment containing two biological samples per sex and treatment. A sample-level pseudobulk approach was recommended.

**Response:**
We agree and made this the principal methodological revision.

The original cell-level differential-expression analysis has been replaced with **sample-level pseudobulk analysis**.

The dataset contains eight biological samples representing:

* Female Cocaine — replicate 1
* Female Cocaine — replicate 2
* Female Sucrose — replicate 1
* Female Sucrose — replicate 2
* Male Cocaine — replicate 1
* Male Cocaine — replicate 2
* Male Sucrose — replicate 1
* Male Sucrose — replicate 2

Counts are aggregated across cells within each biological sample. Thus, the biological sample rather than the individual cell is the inferential unit.

The revised analysis uses a DESeq2-style negative-binomial model through PyDESeq2.

We also explicitly acknowledge that there are only **two biological replicates per sex × treatment combination**, which limits statistical power and precision. This limitation is now discussed in the final report.

---

## 5. Comparing 50 vs. 46 significant genes does not directly test a sex difference

**Reviewer comment:**
The difference between the numbers of significant genes in males and females is descriptive and does not directly test whether the treatment response differs between sexes.

**Response:**
We agree.

The previous interpretation based on the 50-versus-46 comparison has been removed from the final analysis.

The revised model is:

`~ sex + treatment + sex:treatment`

The explicit **sex × treatment interaction** is now used as the inferential test of whether the cocaine treatment effect differs between males and females.

The final results are:

| Contrast                    | Significant genes |
| --------------------------- | ----------------: |
| Female cocaine vs sucrose   |           **246** |
| Male cocaine vs sucrose     |           **109** |
| Sex × treatment interaction |            **46** |

The 246 and 109 values are now reported only as treatment-response counts within each sex. They are not interpreted as evidence that one sex has a statistically stronger response.

The **46 interaction genes** represent genes for which the estimated treatment effect differs between sexes under the fitted model.

Sample-level QC information is retained in `qc_cell_counts_by_sample.csv`, and experimental metadata are retained in `sample_metadata.csv`.

---

## 6. Undefined fold-change values should be reported

**Reviewer comment:**
The original DE analysis produced warnings about invalid values during log2 fold-change calculation.

**Response:**
We addressed this explicitly in the revised workflow.

A low-count filtering step is documented and the resulting information is retained in:

`results/tables/low_count_filter_summary.csv`

We also added a dedicated fold-change integrity audit:

`results/tables/fold_change_audit.csv`

The final audit reports:

| Contrast                    | Genes tested | Non-finite log2FC | Significant |
| --------------------------- | -----------: | ----------------: | ----------: |
| Female treatment            |        9,557 |                 0 |         246 |
| Male treatment              |        9,557 |                 0 |         109 |
| Sex × treatment interaction |        9,557 |                 0 |          46 |

Thus, **zero non-finite log2FC values** remain in the final differential-expression tables.

---

## 7. Figure 5 should be regenerated and checked

**Reviewer comment:**
The pathway-enrichment terms shown in the previous Figure 5 did not fully match the notebook output.

**Response:**
We agree and regenerated the pathway-enrichment outputs using the revised differential-expression results.

The final repository contains separate files for complete, significant, and non-significant enrichment results:

* `female_pathway_enrichment_all.csv`
* `female_pathway_enrichment_significant.csv`
* `female_pathway_enrichment_nonsignificant.csv`
* `male_pathway_enrichment_all.csv`
* `male_pathway_enrichment_significant.csv`
* `male_pathway_enrichment_nonsignificant.csv`

No enrichment terms passed the adjusted p < 0.05 threshold in either sex.

Because the final analysis contains no adjusted-significant enrichment terms, we no longer present a pathway-enrichment figure that could be interpreted as showing significant enrichment. The complete enrichment results remain available as CSV tables for transparency.

The previously described terms such as "mating defective" and "sleep defective" are therefore no longer reported as significant findings from the final analysis.

---

# PART 5: MINOR COMMENTS & PRESENTATION IMPROVEMENTS

## 1. Report significant and non-significant enrichment terms separately

**Response:**
Implemented.

The final repository provides separate significant and non-significant enrichment tables for both sexes, together with the complete enrichment results.

No terms passed the adjusted p < 0.05 threshold in either sex.

---

## 2. Add clear axis labels and gene labels

**Response:**
The final volcano figures were regenerated from the revised pseudobulk result tables.

The repository now contains:

* `fig4_volcano_female.png`
* `fig4_volcano_male.png`
* `fig4_volcano_interaction.png`

The plots clearly distinguish effect size from statistical significance.

Because the underlying DE analysis was substantially revised, the final figures were regenerated rather than retaining the earlier cell-level DE figures.

---

## 3. Report cell numbers before and after QC

**Response:**
Implemented.

The final repository contains:

`results/tables/qc_cell_counts_by_sample.csv`

This provides sample-level cell-count information for the QC workflow.

The final post-QC dataset contains **88,922 cells and 11,946 genes**.

The QC workflow also documents the mitochondrial-content threshold and other filtering criteria.

---

## 4. Consider doublet detection

**Response:**
We acknowledge that a dedicated doublet-detection method such as Scrublet was not included in the final workflow.

We did not add a doublet-detection method retrospectively without validating its effect on the complete analysis, as doing so could introduce another unvalidated analytical change.

This has therefore been retained as a limitation of the current analysis and is identified as a possible future improvement.

---

## 5. Improve marker-based cell-type interpretation

**Response:**
The marker-based annotation was reviewed and documented more explicitly.

Nine of the ten intended canonical markers were recovered:

`repo`, `elav`, `ey`, `Fas2`, `VAChT`, `Gad1`, `ple`, `SerT`, and `Tdc2`.

`VGlut` was not recovered in the retained gene set.

The final repository contains:

* `fig3_marker_dotplot.png`
* `fig3_umap_cell_types.png`
* `cluster_marker_mean_expression.csv`

The report also discusses the overlapping expression of markers such as `ple`, `SerT`, and `Tdc2` and emphasizes that marker-based annotations should be interpreted in the context of cluster-level expression rather than as mutually exclusive classifications.

---

## 6. Provide a quantitative basis for clustering resolution

**Response:**
Implemented.

Leiden clustering was evaluated at resolutions:

* 0.5
* 0.8
* 1.0
* 1.2

The corresponding cluster numbers were:

| Resolution | Clusters |
| ---------: | -------: |
|        0.5 |       21 |
|        0.8 |       29 |
|        1.0 |       32 |
|        1.2 |       34 |

A fixed 5,000-cell sample was used for reproducible silhouette assessment in PCA space.

Resolution **0.8**, producing 29 clusters, was retained as the final clustering resolution.

The complete comparison is available in:

`results/tables/clustering_resolution_comparison.csv`

---

## 7. Fix documentation inconsistencies

**Response:**
Implemented.

The README and report have been updated to reflect the final analysis.

The final documentation consistently reports:

* 88,922 final cells;
* 11,946 genes in the normalized object;
* 29 clusters at Leiden resolution 0.8;
* 9,557 genes tested in pseudobulk DE;
* 246 female treatment-response genes;
* 109 male treatment-response genes;
* 46 significant sex × treatment interaction genes;
* zero non-finite log2FC values; and
* zero adjusted-significant enrichment terms in either sex.

The figure filenames have also been standardized.

The previous cell-level result of 50 male versus 46 female genes is explicitly identified as a superseded result rather than a final finding.

---

## 8. Complete the AI disclosure

**Response:**
The README now contains an AI usage disclosure describing the role of AI assistance in computational workflow development, debugging, plotting adjustments, and related code development.

The final analysis code was reviewed and executed by the group leader before inclusion in the repository.

The disclosure also distinguishes computational assistance from the group's analytical decisions regarding QC, clustering resolution, and interpretation.

---

# PART 6: GITHUB & REPRODUCIBILITY

We appreciate the reviewer highlighting reproducibility as a major issue.

The final repository now provides a documented execution path:

1. Obtain the eight GSE152495 sample matrices.
2. Place them in the documented `data/` directory structure.
3. Create the Python environment and install the requirements.
4. Execute Notebook 1 for data loading and QC.
5. Execute Notebook 2 for clustering and annotation.
6. Execute Notebook 3 for pseudobulk differential expression, interaction testing, and pathway enrichment.

The repository also retains intermediate objects and final result tables, allowing the reported outputs to be inspected independently of the original notebook session.

We acknowledge that the reviewer was unable to complete an independent end-to-end execution during the original review. We have therefore treated reproducibility as a substantive issue and addressed it through clearer data organization, explicit execution instructions, retained intermediate outputs, and revised analysis notebooks.

---

# PART 7: PRIORITY ACTIONS BEFORE FINAL SUBMISSION

| Reviewer recommendation                         | Final status                                                      |
| ----------------------------------------------- | ----------------------------------------------------------------- |
| Fix data-loading/reproducibility problem        | **Addressed through revised data organization and documentation** |
| Preserve appropriate expression for DE          | **Addressed through raw-count pseudobulk DE**                     |
| Do not restrict DE to 2,000 HVGs                | **Addressed; 9,557 genes tested**                                 |
| Address pseudoreplication                       | **Addressed using sample-level pseudobulk analysis**              |
| Regenerate pathway analysis                     | **Addressed; enrichment outputs regenerated**                     |
| Report cell counts                              | **Addressed with sample-level QC table**                          |
| Treat 50 vs. 46 as descriptive                  | **Addressed; previous interpretation removed**                    |
| Directly test sex × treatment                   | **Addressed with explicit interaction term**                      |
| Audit undefined fold changes                    | **Addressed; zero non-finite log2FC values**                      |
| Separate significant/non-significant enrichment | **Addressed**                                                     |
| Quantitatively assess clustering resolution     | **Addressed with silhouette comparison**                          |
| Update AI disclosure                            | **Addressed in README**                                           |

---

# Final Response

We thank the reviewer for identifying the methodological weaknesses in the original workflow. The review led to substantial changes to the analysis rather than only changes to the written discussion.

The most important revision was replacement of cell-level differential expression with **sample-level pseudobulk analysis**, treating biological samples rather than individual cells as the inferential units. We additionally implemented an explicit **sex × treatment interaction model**, expanded DE testing beyond the 2,000 HVGs, added a fold-change integrity audit, regenerated the final differential-expression and enrichment outputs, added sample-level QC information, and quantitatively evaluated clustering resolution.

The final analysis contains **88,922 cells and 11,946 genes**, with **9,557 genes tested** in the pseudobulk analysis. Under FDR < 0.05 and |log2FC| ≥ 1, the final analysis identifies **246 female treatment-response genes, 109 male treatment-response genes, and 46 genes with a significant sex × treatment interaction**. The fold-change audit found **zero non-finite log2FC values**, and no FlyBase phenotype-enrichment terms reached adjusted significance in either sex.

The previous 50-versus-46 cell-level comparison is no longer used as evidence for a sex difference. The explicit interaction contrast is now used for that purpose.

We appreciate the reviewer's methodological guidance, particularly regarding biological replication, pseudobulk analysis, interaction testing, reproducibility, and transparent reporting. These recommendations substantially improved the methodological rigor and transparency of the final project.
