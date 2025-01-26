from fastapi import FastAPI
from models import api_response
from models.requests.predict_request import PredictRequest
from services.ml_service import MlService

app = FastAPI()
service = MlService()


@app.get("/", response_model=api_response.ApiResponse[str])
def example_endpoint():
    return {
        "message": "Hello, World!",
        "success": True,
        "data": None
    }


@app.get("/train")
def train():
  service.train()
  return {"message": "Model trained successfully", "success": True, "data": None}


@app.post("/predict")
def predict(request: PredictRequest):
  return {"message": "Prediction successful", "success": True, "data": service.predict(request.text)}