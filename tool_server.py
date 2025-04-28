from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import time
import requests
app = FastAPI(
    title="Svan Control API",
    version="1.0.0",
    description="Allows control of the SVAN m2 quadruped robot."
)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def constrain_value(value, minimum: float = -1.0, maximum: float = 1.0):
    return max(minimum, min(value, maximum))

SIM = True
if SIM:
    SVAN_BASE = "http://127.0.0.1:8888"
else:
    SVAN_BASE = "http://10.42.4.9:8888"



class SetOperationMode(BaseModel):
    operation_mode: int = Field(...,description="Operation mode integer. (1 - STOP, 2 - TWIRL, 3 - PUSH UP)")

class SetPitch(BaseModel):
    pitch: float = Field(...,description="Normalised float value for pitch. positive pitch is towards the front of the robot.")

class SetRoll(BaseModel):
    roll: float = Field(...,description="Normalised float value for roll. positive roll is towards the right of the robot.")

class SetYaw(BaseModel):
    yaw: int = Field(...,description="Integer value corresponding to preset yaw. (0 - left side yaw, 1 - right side yaw, 2 - no yaw)")

class SetMovement(BaseModel):
    vel_x: float = Field(...,description="Normalised float value for velocity in the x-axis (right side of robot).")
    vel_y: float = Field(...,description="Normalised float value for velocity in the y-axis (front of the robot).")
    duration: float = Field(...,description="Float duration in seconds to execute the velocity command for. Use 5 seconds as the default")


@app.post('/mode',summary="Set Operation Mode for the SVAN M2 robot.")
def set_operation_mode(data: SetOperationMode):
    if data.operation_mode not in [1,2,3,4]:
        return {
            "message": f"Invalid operation mode"
        }
    requests.post(SVAN_BASE+"/mode",json={'operation_mode': data.operation_mode})
    return {
        "message": f"SVAN M2 successfully changed to mode: {data.operation_mode}"
    }

@app.post('/roll')
def set_roll_value(data: SetRoll):
    value = constrain_value(data.roll)
    requests.post(SVAN_BASE+"/roll",json={"roll": value})
    return {
        "message": f"SVAN M2 roll value set to {value}"
    }

@app.post('/pitch')
def set_roll_value(data: SetPitch):
    value = constrain_value(data.pitch)
    requests.post(SVAN_BASE+"/pitch",json={"pitch": value})
    return {
        "message": f"SVAN M2 pitch value set to {value}"
    }


@app.post('/yaw')
def set_roll_value(data: SetYaw):
    if data.yaw not in [0,1,2]:
        return {
            "message": "Invalid yaw value"
        }
    requests.post(SVAN_BASE+"/yaw",json={
        "yaw": data.yaw
    })
    return {
        "message": f"SVAN M2 yaw value set to {data.yaw}"
    }

@app.post('/movement')
def set_movement(data: SetMovement):
    x_value = constrain_value(data.vel_x)
    y_value = constrain_value(data.vel_y)
    requests.post(SVAN_BASE + "/mode", json={
        "operation_mode": 4
    })
    requests.post(SVAN_BASE+"/movement",json={
        "vel_x": x_value,
        "vel_y": y_value
    })
    time.sleep(data.duration)
    requests.post(SVAN_BASE+"/movement",json={
        "vel_x": 0.0,
        "vel_y": 0.0
    }),
    time.sleep(0.1)
    requests.post(SVAN_BASE + "/mode", json={
        "operation_mode": 1
    })
    return {
        "message": f"SVAN M2 velocity set to x: {x_value}, y: {y_value}"
    }

