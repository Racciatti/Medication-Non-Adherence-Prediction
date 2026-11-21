"""Helpers to load NHANES 2013-2014 (cycle H) SAS transport (.xpt) modules.

The data directory defaults to ``./data/`` and can be overridden with the
``NHANES_DATA_DIR`` environment variable. Raw files are fetched with
``python data/download.py``.
"""
import os

import pandas as pd

base_path = os.environ.get('NHANES_DATA_DIR', './data/')

# Human-readable module name -> NHANES file name.

MODULE_FILENAMES = {
    'alcohol'               :   'ALQ_H.xpt', 
    'blood_pres_chol'       :   'BPQ_H.xpt',
    'consumer_behavior'     :   'CBQ_H.xpt',
    'demographics'          :   'DEMO_H.xpt',
    'diabetes'              :   'DIQ_H.xpt',
    'disability'            :   'DLQ_H.xpt',
    'dietary_1'             :   'DR1TOT_H.xpt',
    'dietary_2'             :   'DR2TOT_H.xpt',
    'dietary_sup_1'         :   'DS1TOT_H.xpt',
    'dietary_sup_2'         :   'DS2TOT_H.xpt',
    'access_to_care'        :   'HUQ_H.xpt',
    'ostheoporosis'         :   'OSQ_H.xpt',
    'income'                :   'INQ_H.xpt',
    'medical_conditions'    :   'MCQ_H.xpt',
    'physical_activity'     :   'PAQ_H.xpt',
    'physical_functioning'  :   'PFQ_H.xpt',
    'prescription'          :   'RXQ_RX_H.xpt',
    'sleep_disorders'       :   'SLQ_H.xpt',
}

# Variables kept from each module (SEQN is the respondent id used to merge).
SELECTED_VARS_PER_MODULE = {
    'alcohol' : [
        'SEQN', 'ALQ120Q', 'ALQ120U', 'ALQ130', 'ALQ141U', 'ALQ141Q'
    ],
    'blood_pres_chol' : [
        'SEQN', 'BPQ100D','BPQ090D','BPQ080','BPQ060','BPQ050A','BPQ040A','BPQ030','BPQ020','BPD058','BPD035'

    ],
    'consumer_behavior': [
        'SEQN', 'CBD120', 'CBD070'
    ],
    'demographics' : [
        'SEQN', 'DMDEDUC2', 'DMDHREDU', 'DMDHSEDU', 'DMDFMSIZ', 'DMDHHSIZ', 
        'DMDHHSZA', 'DMDHHSZB', 'DMDHHSZE', 'DMDHRAGE', 'RIDAGEYR', 'DMDHRGND', 
        'RIAGENDR', 'DMDHRMAR', 'DMDMARTL', 'INDFMIN2', 'INDHHIN2'
    ],
    'diabetes' : [
        'SEQN', 'DIQ260U','DIQ180','DIQ070','DIQ050','DID250','DID060','DID040','DIQ010'

    ],
    'dietary_1' : [
        'SEQN', 'DR1_320Z', 'DR1DRSTZ', 'DR1TALCO', 'DR1TCAFF', 'DR1TKCAL', 
        'DR1TPROT', 'DR1TSUGR', 'DR1TTFAT', 'DRQSDIET'] + 'DRQSDT91 DRQSDT9 DRQSDT8 DRQSDT7 DRQSDT6 DRQSDT5 DRQSDT4 DRQSDT3 DRQSDT2 DRQSDT12 DRQSDT11 DRQSDT10 DRQSDT1'.split() 
    ,
    'dietary_2' : [
        'SEQN', 'DR2_320Z', 'DR2DRSTZ', 'DR2TALCO', 'DR2TCAFF', 'DR2TKCAL', 
        'DR2TPROT', 'DR2TSUGR', 'DR2TTFAT'
    ],
    'dietary_sup_1' : [
        'SEQN', 'DS1TCALC','DS1TCAFF'

    ],
    'dietary_sup_2' : [
        'SEQN', 'DS2TCALC','DS2TCAFF'
    ],
    'access_to_care' : [
        'SEQN', 'HUQ061', 'HUQ051'

    ],
    'ostheoporosis' : [
        'SEQN', 'OSQ072', 'OSQ060'
    ],
    'disability' : [
        'SEQN', 'DLQ010', 'DLQ020', 'DLQ040', 'DLQ050'
    ],
    'medical_conditions' : [
        'SEQN', 'MCQ084'
    ],
    'physical_activity' : [
        'SEQN', 'PAD645', 'PAD660', 'PAD675', 'PAQ635', 'PAQ640', 'PAQ650', 
        'PAQ655', 'PAQ665', 'PAQ670', 'PAD680', 'PAQ731', 'PAQ715', 'PAQ710', 
        'PAQ706', 'PAQ679', 'PAQ678', 'PAQ677'
    ],
    'physical_functioning' : [
        'SEQN', 'PFQ059', 'PFQ057', 'PFQ054', 'PFQ061H', 'PFQ061I', 'PFQ061P', 
        'PFQ061J', 'PFQ061K'
    ],
    'sleep_disorders' : [
        'SEQN', 'SLD010H'
    ],
    'income' : [
        'SEQN', 'INQ244', 'IND235', 'IND247'
    ],
    'prescription' : [
        'SEQN', 'RXDCOUNT'
    ]
}

def load_module(module_name: str) -> pd.DataFrame:
    """Load a module from its SAS xport file, given its human-readable name.

    Raises:
        ValueError: if ``module_name`` is not a key of ``MODULE_FILENAMES``.
    """
    if module_name not in MODULE_FILENAMES:
        raise ValueError(f"Module '{module_name}' is not mapped.")
    filepath = os.path.join(base_path, MODULE_FILENAMES[module_name])
    return pd.read_sas(filepath)

def verify_variables(df: pd.DataFrame, module_name: str, verbose=True) -> bool:
    """Check that every selected variable of a module exists in ``df``.

    Returns True if all are present; otherwise prints the missing ones and
    returns False. ``verbose`` controls the success message.
    """
    expected_vars = SELECTED_VARS_PER_MODULE.get(module_name, [])
    missing_vars = [var for var in expected_vars if var not in df.columns]
    
    if missing_vars:
        print(f"[{module_name}] Missing variables: {missing_vars}")
        return False
    else:
        if verbose:
            print(f"[{module_name}] All {len(expected_vars)} selected variables are present.")
        return True

def load_and_verify(module_name: str, verbose=True) -> pd.DataFrame:
    """Load a module and verify its selected variables (see ``verify_variables``)."""
    df = load_module(module_name)
    verify_variables(df, module_name, verbose)
    return df
