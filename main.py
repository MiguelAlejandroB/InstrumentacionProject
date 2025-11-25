from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from db import SessionLocal, SensorData
app = FastAPI()

API_KEY = "tu_api_key_segura"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="API Key inválida")

@app.post("/sensor")
def receive_data(sensor1: float, sensor2: float, sensor3: float, db: Session = Depends(get_db), _: str = Depends(verify_api_key)):
    new_data = SensorData(sensor1=sensor1, sensor2=sensor2, sensor3=sensor3)
    db.add(new_data)
    db.commit()
    return {"message": "Datos guardados correctamente"}
