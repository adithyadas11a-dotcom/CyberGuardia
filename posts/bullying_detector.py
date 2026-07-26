import pickle
import os

# Load the pre-trained model (Make sure the model file is in the correct directory)
MODEL_PATH = os.path.join(os.path.dirname(__file__), "LinearSVC.pkl")

with open(MODEL_PATH, "rb") as model_file:
    model = pickle.load(model_file)

def predict_bullying(comment_text):
    """Predict whether the given comment is bullying or not."""
    prediction = model.predict([comment_text])  # Assuming the model takes a list
    return prediction[0]  # 1 for bullying, 0 for not bullying
