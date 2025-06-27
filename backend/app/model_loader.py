import os
import xgboost as xgb

# Define paths
BASIC_MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "model_basic.json")
MACRO_MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "model_macro.json")

# Load models using load_model
_basic_model = xgb.XGBClassifier()
_basic_model.load_model(BASIC_MODEL_PATH)

_macro_model = xgb.XGBClassifier()
_macro_model.load_model(MACRO_MODEL_PATH)

# Return model based on use_macro flag
def get_model(use_macro: bool = False):
    return _macro_model if use_macro else _basic_model
