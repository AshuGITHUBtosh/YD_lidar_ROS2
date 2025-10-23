import ctypes
import numpy as np
import matplotlib.pyplot as plt
import time

# --------------------------
# SDK Setup
# --------------------------

# Load the SDK shared library
# Adjust the path if necessary
ydlidar = ctypes.CDLL('/home/ashutosh/Desktop/lidar_ws/src/YDLidar-SDK/build/libydlidar_sdk.so')

# Define necessary C types
ydlidar.ydlidarInit.restype = ctypes.c_bool
ydlidar.ydlidarTurnOn.restype = ctypes.c_bool
ydlidar.ydlidarGrab.restype = ctypes.c_bool

# Create a handle
handle = ctypes.c_void_p()

# --------------------------
# LiDAR Settings
# --------------------------
port = b"/dev/ttyUSB0"
baudrate = 230400
lidar_type = 6  # TYPE_TRIANGLE
frame_id = b"laser_frame"

# Initialize the LiDAR
if not ydlidar.ydlidarInit(handle, port, baudrate, lidar_type):
    print("Failed to initialize LiDAR")
    exit(1)

if not ydlidar.ydlidarTurnOn(handle):
    print("Failed to turn on LiDAR")
    exit(1)

print("LiDAR initialized and running!")

# --------------------------
# Live Plot Setup
# --------------------------
plt.ion()
fig, ax = plt.subplots(figsize=(6,6))
scatter = ax.scatter([], [], s=5)
ax.set_xlim(-64, 64)
ax.set_ylim(-64, 64)
ax.set_xlabel("X (m)")
ax.set_ylabel("Y (m)")
ax.set_title("YDLiDAR X2 Live Scan")
ax.set_aspect('equal')

# --------------------------
# Main Loop
# --------------------------
NUM_POINTS = 269

# Prepare ctypes arrays for scan data
distances = (ctypes.c_float * NUM_POINTS)()
angles = (ctypes.c_float * NUM_POINTS)()

try:
    while True:
        # Grab a scan
        if ydlidar.ydlidarGrab(handle, distances, angles, NUM_POINTS):
            xs = np.array([distances[i] * np.cos(angles[i]) for i in range(NUM_POINTS)])
            ys = np.array([distances[i] * np.sin(angles[i]) for i in range(NUM_POINTS)])

            scatter.set_offsets(np.c_[xs, ys])
            fig.canvas.draw()
            fig.canvas.flush_events()
            time.sleep(0.05)
        else:
            print("Failed to grab scan")

except KeyboardInterrupt:
    print("Exiting...")
    ydlidar.ydlidarTurnOff(handle)
