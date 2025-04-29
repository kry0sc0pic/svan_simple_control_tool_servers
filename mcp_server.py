# server.py
from fastmcp import FastMCP
import requests
import time

# Create an MCP server
mcp = FastMCP("SvanControl")
SIM = True
if SIM:
    SVAN_BASE = "http://127.0.0.1:8888"
else:
    SVAN_BASE = "http://10.42.4.9:8888"


def constrain_value(value, minimum: float = -1.0, maximum: float = 1.0):
    return max(minimum, min(value, maximum))


@mcp.tool()
def set_operation_mode(mode: int):
    """Set operation mode for the SVAN quadruped robot

    Args:
        mode: an integer value corresponding to a certain model.
            AVAILABLE MODES:
                - 1 (STOP)
                - 2 (TWIRL)
                - 3 (PUSH UP)
    """
    print(f"Receieved mode: {mode}")
    if 1 <= mode <= 4:
        requests.post(SVAN_BASE + "/mode", json={'operation_mode': mode})
    else:
        print("Invalid Mode")


@mcp.tool()
def set_movement(x_vel: float, y_vel: float, duration=5):
    """Set movement velocity for the SVAN quadruped robot

    Args:
        x_vel: float velocity in x-axis (-1.0 to 1.0). positive x-axis is to the right side of the robot
        y_vel: float velocity in y-axis (-1.0 to 1.0). positive y-axis is to the front of the robot.
        duration: float time for execution of movement in seconds. default to 5 seconds
    """
    set_operation_mode(mode=4)  # switch to trot
    requests.post(SVAN_BASE + "/movement", json={
        "vel_x": constrain_value(x_vel),
        "vel_y": constrain_value(y_vel),
    })
    time.sleep(duration)
    requests.post(SVAN_BASE + "/movement", json={
        "vel_x": 0.0,
        "vel_y": 0.0,
    })
    time.sleep(0.1)
    set_operation_mode(mode=1)  # stop


@mcp.tool()
def set_roll(roll: float = 0.0):
    """Sets the roll value of the SVAN quadruped robot.

    Args:
        roll: float value (-1.0 to 1.0) - positive roll is towards the right
    """
    requests.post(SVAN_BASE + "/roll", json={
        "roll": constrain_value(roll),
    })


@mcp.tool()
def set_pitch(pitch: float = 0.0):
    """Sets the pitch of the SVAN quadruped robot.

    Args:
        pitch: float value (-1.0 to 1.0) - positive pitch is forwards.
    """
    requests.post(SVAN_BASE + "/pitch", json={
        "pitch": constrain_value(pitch),
    })


@mcp.tool()
def set_yaw(yaw: int = 2):
    """Sets the yaw direction of the robot

    Args:
        yaw: integer value corresponding to yaw angle presets
            0 - YAW LEFT
            1 - YAW RIGHT
            2 - NO YAW
    """
    if yaw in [0, 1, 2]:
        requests.post(SVAN_BASE + "/yaw", json={"yaw": yaw})