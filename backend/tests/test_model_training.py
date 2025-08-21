# import os
# import pytest
# import pandas as pd

# from backend.Machine_Learning_Model.retrain_model import retrain_rent_model
# from backend.Machine_Learning_Model.rental_price_model import load_model


# def test_mockdata_exists():
    # """Ensure the dataset file exists before retraining."""
    # path = os.path.join("backend", "data_processing", "MockData.xlsx")
    # assert os.path.exists(path), "MockData.xlsx not found"


# def test_model_retrain_success():
    # """Check if retraining returns the expected success message."""
    # result = retrain_rent_model()
    # assert result.startswith("Model retrained and saved successfully"), f"Unexpected result: {result}"


# def test_model_file_created():
    # """Verify that the model file was saved to disk."""
    # model_path = os.path.join("backend", "Machine_Learning_Model", "rental_model.pkl")
    # assert os.path.exists(model_path), "Model file was not created"


# def test_model_can_be_loaded():
    # """Ensure the saved model can be loaded without errors."""
    # model = load_model()
    # assert model is not None, "Model could not be loaded"
