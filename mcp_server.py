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


@mcp.tool()
def set_operation_mode(mode: int):
    """Set operation mode for the SVAN quadruped robot

    Args:
        mode: an integer value corresponding to a certain model.
            AVAILABLE MODES:
                - 1 (STOP)
                - 2 (PUSHUP)
                - 3 (TWIRL)
    """
    print(f"Receieved mode: {mode}")
    if 1 <= mode <= 3:
        requests.post(SVAN_BASE + "/mode", json={
            'operation_mode': mode,
        })

    else:
        print("Invalid Mode")


@mcp.tool()
def set_movement(x_vel: float, y_vel: float, duration=None):
    """Set movement velocity for the SVAN quadruped robot

    Args:
        x_vel: float velocity in x-axis (-1.0 to 1.0). positive x-axis is to the right side of the robot'
        y_vel: float velocity in y-axis (-1.0 to 1.0). positive y-axis is to the front of the robot.
        duration: float time for execution of movement in seconds. `None` value will execute the movement infinitely.
    """
    set_operation_mode(mode=3)  # switch to trot
    if duration is None:
        requests.post(SVAN_BASE + "/movement", json={
            "vel_x": max(-1.0, min(x_vel, 1.0)),
            "vel_y": max(-1.0, min(y_vel, 1.0))
        })
    else:
        requests.post(SVAN_BASE + "/movement")
        time.sleep(duration)
        set_operation_mode(mode=1)  # stop


@mcp.tool()
def set_roll(roll: float = 0.0):
    """Sets the roll value of the SVAN quadruped robot.

    Args:
        roll: float value (-1.0 to 1.0) - positive roll is towards the right
    """
    requests.post(SVAN_BASE + "/roll", json={
        "roll": max(-1.0, min(roll, 1.0))
    })


@mcp.tool()
def set_pitch(pitch: float = 0.0):
    """Sets the pitch of the SVAN quadruped robot.

    Args:
        pitch: float value (-1.0 to 1.0) - positive pitch is forwards.
    """
    requests.post(SVAN_BASE + "/pitch", json={
        "pitch": max(-1.0, min(pitch, 1.0))
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
        requests.post(SVAN_BASE + "/yaw", json={
            "yaw": yaw})