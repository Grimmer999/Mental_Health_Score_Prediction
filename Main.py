import joblib
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Literal
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
model = joblib.load('Model/Mental_Health_Model.pkl')

top_countries = ['Other','India','USA','Canada','Australia','UK','Germany','Mexico','Turkey','France']

class PredictionResponse(BaseModel):
    predicted_mental_health: float


class StudentData(BaseModel):
    Study_Hours: float = Field(..., ge=0, le=24)
    Age: int = Field(..., ge=10, le=100)
    Avg_Daily_Usage_Hours: float = Field(..., ge=0, le=24)
    Daily_Unlocks: int = Field(..., ge=0)
    Physical_Activity_Hours: float = Field(..., ge=0, le=24)
    Sleep_Hours_Per_Night: float = Field(..., ge=0, le=24)

    Stress_Level: Literal["Low", "Medium", "High", "Very High"]
    Gender: Literal["Male", "Female"]
    Academic_Level: Literal["High School", "Undergraduate", "Graduate"]

    Most_Used_Platform: Literal[
        "Facebook",
        "LinkedIn",
        "Instagram",
        "Snapchat",
        "Twitter",
        "YouTube",
        "TikTok",
        "LINE",
        "KakaoTalk",
        "VKontakte",
        "WhatsApp",
        "WeChat"
    ]

    Purpose_Of_Use: Literal[
        "Networking",
        "Education",
        "Entertainment",
        "News"
    ]

    Country: str


    
@app.get("/")
def greet():
    return {"message": "Welcome to the Mental Health Prediction API!"}
@app.post("/predict", response_model=PredictionResponse)
def predict_mental_health(data: StudentData):
    country_group = data.Country if data.Country in top_countries else "Other"
    input_row = pd.DataFrame([{
        'Age': data.Age,
        'Study_Hours': data.Study_Hours,
        'Country': data.Country,

        'Avg_Daily_Usage_Hours': data.Avg_Daily_Usage_Hours,
        'Daily_Unlocks': data.Daily_Unlocks,
        'Physical_Activity_Hours': data.Physical_Activity_Hours,
        'Sleep_Hours_Per_Night': data.Sleep_Hours_Per_Night,
        'Stress_Level': data.Stress_Level,
        'Gender': data.Gender,
        'Academic_Level': data.Academic_Level,
        'Most_Used_Platform': data.Most_Used_Platform,
        'Purpose_Of_Use': data.Purpose_Of_Use,
        'Grouped_Country': country_group
    }])
    prediction = model.predict(input_row)[0]


    return PredictionResponse(predicted_mental_health=round(float(prediction), 2))




