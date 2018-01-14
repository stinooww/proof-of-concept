from ADS import *
import sys, time, os

try:
    print("Press CTRL+C to abort.")
    
    ads = ADS();
    while True:
        perc = ads.ADSPercentage()
        sys.stdout.write("\r")
        sys.stdout.write("\033[K")
        sys.stdout.write("LPG: %g ppm, CO: %g ppm, Smoke: %g ppm" % (perc["GAS_LPG"], perc["CO"], perc["SMOKE"]))
        sys.stdout.flush()
        time.sleep(0.1)

except:
    print("\nAbort by user")
