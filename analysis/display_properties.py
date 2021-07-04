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
print("Screen X Size:", SCREEN_XSIZE_INCH)
print("Screen Y Size:", SCREEN_YSIZE_INCH)
# pixels per inch
SCREEN_PPI = SCREEN_XSIZE_PIX / SCREEN_XSIZE_INCH

# Plot specifications
""" Dots per inch """
FIG_DPI = SCREEN_PPI
print("FIgure DPI", FIG_DPI)
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

""""Unit length in inches"""
CARTESIAN_UNIT_LENGTH_IN_INCH = FIG_XSIZE_INCH / (CARTESIAN_PLOT_LIMITS["x"][1] - CARTESIAN_PLOT_LIMITS["x"][0])
CARTESIAN_UNIT_LENGTH_IN_PIX = CARTESIAN_UNIT_LENGTH_IN_INCH * SCREEN_PPI
CARTESIAN_UNIT_LENGTH_IN_CM = CARTESIAN_UNIT_LENGTH_IN_INCH * 2.54
print("Cartesian Unit len (inches)", CARTESIAN_UNIT_LENGTH_IN_INCH)
print("Cartesian Unit len (cm)", CARTESIAN_UNIT_LENGTH_IN_CM)

# fix limits of y axis in cartesian system so it takes up the untire screen height
CARTESIAN_PLOT_LIMITS["y"][1] = 1.25 + FIG_YSIZE_INCH / CARTESIAN_UNIT_LENGTH_IN_INCH / 2
CARTESIAN_PLOT_LIMITS["y"][0] = 1.25 - FIG_YSIZE_INCH / CARTESIAN_UNIT_LENGTH_IN_INCH / 2

POLAR_UNIT_LENGTH_IN_INCH = (FIG_YSIZE_INCH / 2) / (POLAR_PLOT_LIMITS["y"][1] - POLAR_PLOT_LIMITS["y"][0])
POLAR_UNIT_LENGTH_IN_PIX = POLAR_UNIT_LENGTH_IN_INCH * SCREEN_PPI
POLAR_UNIT_LENGTH_IN_CM = POLAR_UNIT_LENGTH_IN_INCH * 2.54
print("Polar Unit len (inches)", POLAR_UNIT_LENGTH_IN_INCH)
print("Polar Unit len (cm)", POLAR_UNIT_LENGTH_IN_CM)

# https://stackoverflow.com/questions/57657419/how-to-draw-a-figure-in-specific-pixel-size-with-matplotlib
# linewidth of matplotlib plots is in points, where one point is:
# point = figure.dpi / 72
# https://stackoverflow.com/questions/14827650/pyplot-scatter-plot-marker-size/47403507#47403507
# here is says: "The standard size of points in matplotlib is 72 points per inch (ppi)"
LINEWIDTH_IN_POINTS = 1  # the linewidth property on plots (it is set to 1)
# in our case FIG_DPI is equal to SCREEN_PPI, so points and pixels are the same size
LINEWIDTH_IN_PIX =  LINEWIDTH_IN_POINTS * FIG_DPI / 72
LINEWIDTH_IN_INCH = LINEWIDTH_IN_PIX / SCREEN_PPI
LINEWIDTH_IN_CM = LINEWIDTH_IN_INCH * 2.54
print("Linewidth in inches:", LINEWIDTH_IN_INCH)
print("Linewidth in centimeters:", LINEWIDTH_IN_CM)