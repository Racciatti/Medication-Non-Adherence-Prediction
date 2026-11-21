"""Benchmarking of tree-based classifiers (GridSearchCV + hold-out metrics)."""
import time

import pandas as pd
from sklearn.model_selection import StratifiedKFold, GridSearchCV
from sklearn.metrics import (
    roc_auc_score, 
    f1_score, 
    precision_score, 
    recall_score, 
    brier_score_loss,
    confusion_matrix
)
from sklearn.ensemble import RandomForestClassifier  # used by the commented-out grid below

import xgboost as xgb
import lightgbm as lgb

class TreeModelBenchmarker:
    """Fit, cross-validate and benchmark tree-based classifiers.

    Args:
        X_train, y_train: training features / binary target.
        X_test, y_test: hold-out features / binary target.
        scoring_metric: scikit-learn scorer used by GridSearchCV.
        cv_splits: number of stratified folds (seed fixed at 42).

    After ``execute_pipeline()``, ``results`` holds hold-out metrics per model
    and ``best_estimators`` the refit best models.
    """
    def __init__(self, X_train, y_train, X_test, y_test, scoring_metric='roc_auc', cv_splits=5):
        
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test
        self.scoring_metric = scoring_metric
        
        self.cv = StratifiedKFold(n_splits=cv_splits, shuffle=True, random_state=42)
        
        self.models_config = self._define_configurations()
        self.results = {}
        self.best_estimators = {}

    def _define_configurations(self):
        """Define the estimators and hyperparameter grids to search."""
        
        # Positive-class weight, only used by the (commented-out) XGBoost config.
        scale_weight = (len(self.y_train) - sum(self.y_train)) / sum(self.y_train) if sum(self.y_train) > 0 else 1

        return {
            # 'RandomForest': {
            #     'estimator': RandomForestClassifier(random_state=42, class_weight='balanced'),
            #     'param_grid': {
            #         'n_estimators': [100, 300],
            #         'max_depth': [5, 10, None],
            #         'min_samples_split': [2, 5, 10],
            #         'min_samples_leaf': [1, 2, 4],
            #         'max_features': ['sqrt', 'log2']
            #     }
            # },
            # 'XGBoost': {
            #     'estimator': xgb.XGBClassifier(random_state=42, eval_metric='logloss', scale_pos_weight=scale_weight),
            #     'param_grid': {
            #         'n_estimators': [100, 300],
            #         'max_depth': [3, 5, 7],
            #         'learning_rate': [0.01, 0.1],
            #         'subsample': [0.8, 1.0],
            #         'colsample_bytree': [0.8, 1.0],
            #         'reg_alpha': [0, 0.1, 1],   # Regularização L1
            #         'reg_lambda': [1, 10]       # Regularização L2
            #     }
            # },
            'LightGBM': {
                'estimator': lgb.LGBMClassifier(random_state=42, class_weight='balanced', verbose=-1),
                'param_grid': {
                    'n_estimators': [100, 300],
                    'max_depth': [-1],
                    'learning_rate': [0.1],
                    'num_leaves': [63],
                    'subsample': [0.8],
                    'min_child_samples': [20]
                }
            }
        }

    def execute_pipeline(self):
        """Run GridSearchCV per model, then compute hold-out (test) metrics."""
        for model_name, config in self.models_config.items():
            print(f"Iniciando otimização para: {model_name}...")
            start_time = time.time()

            grid_search = GridSearchCV(
                estimator=config['estimator'],
                param_grid=config['param_grid'],
                scoring=self.scoring_metric,
                cv=self.cv,
                n_jobs=-1, 
                verbose=1
            )
            
            grid_search.fit(self.X_train, self.y_train)
            
            best_model = grid_search.best_estimator_
            self.best_estimators[model_name] = best_model
            
            y_pred = best_model.predict(self.X_test)
            y_proba = best_model.predict_proba(self.X_test)[:, 1]
            
            tn, fp, fn, tp = confusion_matrix(self.y_test, y_pred).ravel()
            
            self.results[model_name] = {
                'Best_Params': grid_search.best_params_,
                'ROC_AUC': roc_auc_score(self.y_test, y_proba),
                'F1_Score': f1_score(self.y_test, y_pred),
                'Precision': precision_score(self.y_test, y_pred, zero_division=0),
                'Recall': recall_score(self.y_test, y_pred, zero_division=0),
                'Brier_Score': brier_score_loss(self.y_test, y_proba), # probability calibration
                'True_Positives': tp,
                'False_Positives': fp,
                'True_Negatives': tn,
                'False_Negatives': fn,
                'Training_Time_sec': round(time.time() - start_time, 2)
            }
            print(f"{model_name} concluído em {self.results[model_name]['Training_Time_sec']}s. ROC-AUC: {self.results[model_name]['ROC_AUC']:.4f}\n")

    def get_metrics_report(self):
        """Return hold-out metrics of all models as a DataFrame sorted by ROC-AUC."""
        if not self.results:
            raise ValueError("O pipeline ainda não foi executado. Chame execute_pipeline().")
        
        report_df = pd.DataFrame.from_dict(self.results, orient='index')
        
        report_df = report_df.sort_values(by='ROC_AUC', ascending=False)
        return report_df

    def get_feature_importances(self, feature_names):
        """Return a DataFrame of ``feature_importances_`` (one column per model)."""
        importances_dict = {}
        for model_name, model in self.best_estimators.items():
            if hasattr(model, 'feature_importances_'):
                importances_dict[model_name] = model.feature_importances_
        
        if not importances_dict:
            raise ValueError("Nenhum modelo suporta extração direta de feature_importances_.")
            
        return pd.DataFrame(importances_dict, index=feature_names)
