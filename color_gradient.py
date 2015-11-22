# System library imports
from PyQt4.QtGui import QColor

def green_red_percentile(percentile, alpha_channel=127):
    if percentile > 100:
        percentile = 100
    elif percentile < 0:
        percentile = 0

    r = (255 * percentile) / 100
    g = (255 * (100 - percentile)) / 100
    b = 0

    return QColor(r, g, b, alpha_channel)