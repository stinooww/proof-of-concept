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
        if  perc["GAS_LPG"] <= 1:
           return  os.system('/usr/bin/push.sh "gevaar LPG"')
        elif  perc["CO"] <= 10000:
           return  os.system('/usr/bin/push.sh "gevaar CO"')
	elif  perc["SMOKE"] <= 3000:
           return  os.system('/usr/bin/push.sh "gevaar smoke"')
        return 0

except:
    print("\nAbort by user")
