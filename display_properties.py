import math
# Device specifications
## Known display stats
SCREEN_XSIZE_PIX = 1920
SCREEN_YSIZE_PIX = 1080
SCREEN_DIAGONAL_INCH = 15.6

## Calculated display stats
SCREEN_RATIO = SCREEN_XSIZE_PIX / SCREEN_YSIZE_PIX
SCREEN_YSIZE_INCH = math.sqrt((SCREEN_DIAGONAL_INCH ** 2) / (SCREEN_RATIO ** 2 + 1))
SCREEN_XSIZE_INCH = SCREEN_RATIO * SCREEN_YSIZE_INCH
# pixels per inch
SCREEN_PPI = SCREEN_XSIZE_PIX / SCREEN_XSIZE_INCH

# Plot specifications
""" Dots per inch """
FIG_DPI = SCREEN_PPI
FIG_XSIZE_INCH = SCREEN_XSIZE_INCH * 0.9
FIG_YSIZE_INCH = SCREEN_YSIZE_INCH

X_RANGE = {
    "start": 0,
    "end": 2 * math.pi
}

CARTESIAN_PLOT_LIMITS = {
    "x": [X_RANGE["start"] - 0.5, X_RANGE["end"] + 0.5],
    "y": [0, 2.5]
}

POLAR_PLOT_LIMITS = {
    "x": [X_RANGE["start"], X_RANGE["end"]],
    "y": [0, 2.5]
}

CARTESIAN_UNIT_LENGTH = FIG_XSIZE_INCH / (CARTESIAN_PLOT_LIMITS["x"][1] - CARTESIAN_PLOT_LIMITS["x"][0])
print("Cartesian Unit len", CARTESIAN_UNIT_LENGTH)

# fix limits of y axis in cartesian system so it takes up the untire screen height
CARTESIAN_PLOT_LIMITS["y"][1] = 1.25 + FIG_YSIZE_INCH / CARTESIAN_UNIT_LENGTH / 2
CARTESIAN_PLOT_LIMITS["y"][0] = 1.25 - FIG_YSIZE_INCH / CARTESIAN_UNIT_LENGTH / 2

POLAR_UNIT_LENGTH = (FIG_YSIZE_INCH / 2) / (POLAR_PLOT_LIMITS["y"][1] - POLAR_PLOT_LIMITS["y"][0])
print("Polar Unit len", POLAR_UNIT_LENGTH)