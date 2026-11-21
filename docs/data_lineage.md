1. `medications_module.csv`     : The selected variables in the 'prescription module'
2. `filtered_data.csv`          : The original vars selected, filtered for the target of age > 50
3. `further_filtered_data.csv`  : The filtered data, but now with the realistic ~30 features, instead of 100 something of (2)
4. `clean_data.csv`             : Data on (3), with null and invalid values properly handled
5. `factors.csv`                : Data on (4), after variable selection (the features we'll use)
6. `clean_factors.csv`          : The features (4), with OOD values handled
7. `features_df.csv`               : The features ready to be used (encoded, normalized, all numerical)
8. `new_structure.csv`               : Better encoding for tree-based models, one row per patient,condition pair.
9. `final_selection_with_target.csv`               : Final selection of features with the target var as well              : 

