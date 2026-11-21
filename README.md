# PAM: Medication Non-Adherence Prediction on NHANES 2013-2014

[Portuguese version / Versão em português](README.pt-BR.md)


## Problem

Can we flag adults aged 50+ who are likely **not adhering to the medication prescribed for a
chronic condition**, using only broadly available demographic, functional and
medication-count information?

- **Unit of analysis:** one row per *(patient, condition)* pair, for four chronic conditions:
  diabetes, osteoporosis, high blood pressure, high cholesterol.
- **Target (`target`, binary):** a *proxy* for non-adherence, built from NHANES answers:
  - `1` (non-adherent): the patient has the condition and a doctor prescribed medication, but
    **says they do not take it**, or **says they take it but no matching medication was seen** by the
    interviewer (RXQ_RX_H, matched by ICD reason-for-use codes).
  - `0` (adherent): says they take it and a matching medication was seen.
  - Overall prevalence of class 1 is about 36% (35.6% in train, 39.6% in test).
- Variables used only to build the target (diabetes/BP/cholesterol/osteoporosis medication
  questions, prescription records) are **not** model features.

## Data

[NHANES](https://www.cdc.gov/nchs/nhanes/) (National Health and Nutrition Examination Survey),
2013-2014 cycle ("H"), published by the CDC's National Center for Health Statistics (public
domain). 18 modules (demographics, questionnaires, dietary, prescriptions) are merged on `SEQN`.
Documentation: [NHANES 2013-2014 data and documentation](https://wwwn.cdc.gov/nchs/nhanes/continuousnhanes/default.aspx?BeginYear=2013).

**Citation:** Centers for Disease Control and Prevention (CDC), National Center for Health
Statistics (NCHS). *National Health and Nutrition Examination Survey Data, 2013-2014.* Hyattsville, MD:
U.S. Department of Health and Human Services, CDC.

**Getting the raw data** (not redistributed here, ~75 MB):

```bash
python data/download.py     # downloads the .xpt files into data/
```

The intermediate CSVs in `data/` (`filtered_data.csv` through `final_selection_with_target.csv`, ~5 MB) and
the final train/test split (`data/final/`) are included, so training and most of `data.ipynb` run without
the raw files. Variable descriptions: [`docs/data_dictionary.md`](docs/data_dictionary.md); table lineage:
[`docs/data_lineage.md`](docs/data_lineage.md).

## Pipeline

```
NHANES .xpt modules (18)
        |  utils.load_and_verify
        v
  merge on SEQN -> keep age >= 50 -> ~30 selected variables
        |
        v
  null handling (domain-aware constants, feature engineering) -> invalid-code removal (7/9: 0.4% of rows)
        |
        v
  encoding / normalization -> one row per (patient, condition) pair
        |
        v
  target engineering (non-adherence proxy)  -->  data/final/{X,y}_{train,test}.csv  (80/20, ordered split)
        |
        v
  training.ipynb: tree-model benchmark -> SHAP feature pruning -> threshold & ROI analysis
```

## Methodology

1. **Preparation (`data.ipynb`)**: module loading and validation, null analysis per variable,
   semantic recoding, feature selection, target construction, split.
2. **Features (16)**: sex, normalized age, education, marital status, hearing / seeing /
   concentrating / walking / remembering difficulty flags, confusion, condition flags,
   condition type, and prescription count (`RXDCOUNT`).
3. **Benchmark v1**: LightGBM, Random Forest and XGBoost with `GridSearchCV` (5-fold stratified, ROC-AUC).
4. **v2/v3**: LightGBM re-run with SHAP-based feature pruning at thresholds 0.1 to 0.5.
5. **v4**: sweep of the decision threshold (F2 score) and an illustrative expected-value
   (ROI) analysis. The ROI inputs are **hypothetical business assumptions** (hospitalization
   cost 15,000, intervention efficacy 30%, 5 hospitalizations per 1,000 non-adherent patients, assumed
   36% prevalence, alert cost 0 to 30 per false positive), giving about 62.5 of value per true positive.

## Results

Hold-out test set: 659 rows (261 positives). Metrics from `results/*.csv` (decision threshold 0.5 unless noted).

| Model (v1 benchmark) | ROC-AUC | F1 | Precision | Recall | Brier |
|---|---|---|---|---|---|
| LightGBM | 0.750 | 0.559 | 0.753 | 0.444 | 0.229 |
| Random Forest | 0.747 | 0.536 | 0.837 | 0.395 | 0.201 |
| XGBoost | 0.731 | 0.541 | 0.732 | 0.429 | 0.221 |

LightGBM with SHAP-based pruning (`results/threshold_metrics.csv`):

| SHAP threshold | ROC-AUC | F1 | Precision | Recall |
|---|---|---|---|---|
| 0.1 | 0.749 | 0.545 | 0.714 | 0.441 |
| 0.2 | 0.720 | 0.520 | 0.690 | 0.418 |
| 0.3 | 0.739 | 0.532 | 0.632 | 0.460 |
| 0.4 | 0.779 | 0.478 | 0.869 | 0.330 |
| 0.5 | 0.779 | 0.499 | 0.900 | 0.345 |

Threshold / expected-value analysis (`results/roi_threshold_optimal.csv`): with a low or zero
cost per alert the best threshold is very low (0.01 to 0.02, i.e. flag almost everyone: e.g. at 0.01,
recall 226/261 with 252 false positives); at a cost of 30 per alert it rises to 0.10
(181 TP, 129 FP). The F2-optimal threshold is also 0.01 (F2 = 0.742, recall 0.866, precision 0.473).

Overall the models are modest (ROC-AUC about 0.72 to 0.78): the signal in these features is limited.

## Reproduce

```bash
python -m venv .venv && source .venv/bin/activate     # Python 3.11+
pip install -r requirements.txt
python data/download.py          # optional: only needed to re-run data.ipynb
jupyter lab                      # run data.ipynb (optional), then training.ipynb
pytest                           # small unit tests for utils.py
```

`training.ipynb` only needs `data/final/`. Re-running notebooks overwrites files in `data/` and `results/`.
Use the benchmarker directly:

```python
from training import TreeModelBenchmarker
b = TreeModelBenchmarker(X_train, y_train, X_test, y_test)
b.execute_pipeline(); print(b.get_metrics_report())
```

## Repository structure

```
data.ipynb          data preparation, target engineering, split
training.ipynb      models, SHAP pruning, threshold and ROI analysis
training.py         TreeModelBenchmarker (GridSearchCV + hold-out metrics)
utils.py            NHANES module loading / variable verification
data/download.py    downloads raw NHANES .xpt files from the CDC
data/*.csv           intermediate tables (see docs/data_lineage.md)
data/final/         train/test split (X_*, y_*)
docs/               data dictionary and table lineage
results/            benchmark, threshold and ROI CSVs
tests/              pytest tests for utils
```

## Limitations

- **Proxy target:** built from self-reports and what the interviewer saw; it does not measure true adherence
  and has no biomarker validation.
- **Small, cross-sectional sample** (3,295 rows after filtering): one survey cycle, 50+ only, results
  have wide uncertainty and are not weighted with NHANES survey weights (not nationally representative as used).
- **Split:** sequential 80/20 by row order (not random); class balance differs (35.6% vs 39.6%), and the
  same patient can appear in more than one row.
- **Threshold / ROI tuning is done on the test set**, so those figures are optimistic; cost
  assumptions are illustrative.
- Possible information overlap between features and the target-construction variables was handled by
  exclusion but not formally audited.

## License

MIT, see [LICENSE](LICENSE). NHANES data is a U.S. government work in the public domain.
