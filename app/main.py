from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.features import create_df_for_person
from app.model import make_prediction

app = FastAPI()


class UserRequest(BaseModel):
    uid: str


@app.post("/predict/")
def predict(request: UserRequest):
    try:
        df = create_df_for_person(request.uid)
        prediction, probability = make_prediction(df)
        message = (
            f"The user is {'a bot' if prediction else 'not a bot'} "
            f"with probability {probability:.2f}"
        )
        return {
            "uid": request.uid,
            "prediction": int(prediction),
            "probability": float(probability),
            "message": message
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health/")
def health_check():
    return {"status": "ok"}
