
import joblib

model_path = "models/NEXORA_RF_Explainable_Model.pkl"

artifact = joblib.load(model_path)

print("Model loaded successfully!")

print("\nStored objects:")
print(artifact.keys())

model = artifact["model"]
preprocessor = artifact["preprocessor"]

print("\nModel type:")
print(type(model).__name__)

print("\nPreprocessor type:")
print(type(preprocessor).__name__)

print("\nOriginal input columns:")
print(preprocessor.feature_names_in_)

print("\nTransformed feature count:")
print(len(artifact["feature_names"]))




print("\nModel classes:")
print(model.classes_)

print("\nExpected input feature count:")
print(len(preprocessor.feature_names_in_))

print("\nPrediction methods available:")
print(hasattr(model, "predict"))
print(hasattr(model, "predict_proba"))

