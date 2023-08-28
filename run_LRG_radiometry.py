import json, math
import numpy as np
import matplotlib.pyplot as plt
import pprint
import csv
import sys
import glob

def run_LRG_radiometry(input_param_path):

    print("\n")
    #input_param_path = "./LRG_params.json"

    with open(input_param_path, 'r') as f_in:
        input_params = json.load(f_in)


    range_start = input_params["Range Start [m]"]
    range_end = input_params["Range End [m]"]

    wvl = input_params["Wavelength [m]"]
    laser_pulse_energy = input_params["Laser Pulse Energy [J]"]
    laser_pulse_duration = input_params["Laser Pulse Duration [s]"]
    laser_power = laser_pulse_energy / laser_pulse_duration
    laser_div_angle = input_params["Laser Divergence Angle [rad]"]
    tgt_size = input_params["Target Size [m]"] 
    tgt_refl = input_params["Target Reflectivity"]
    bkg_refl = input_params["Background Reflectivity [n/a]"]
    tau_atmos = input_params["Atmospheric Attenuation [1/km]"]
    D_ap = input_params["Aperture Diameter [m]"] 
    tau_optics = input_params["Optics Transmission [n/a]"] 
    f = input_params["Focal Length [m]"]
    d = input_params["Detector Size [m]"]
    t_int = input_params["Integration Time"]
    QE = input_params["Detector QE [e-/photon]"]
    K_sensor = input_params["Sensor Gain [DN/e-]"]
    K_dark = input_params["Dark Current Gain [DN/e-]"]
    I_dark = input_params["Dark Current [e-/s]"] 
    read_noise = input_params["Read Noise [e-]"]

    beta                            = input_params["Beta [1/sr/m]"]
    r_near                          = input_params["R Near [m]"]

    c = 299792458 # [m/s]
    h = 6.626 * pow(10, -34) # [Js]

    conversion_term = K_sensor * t_int * QE * wvl / (h * c) # [DN / W]. Convert power to counts.

    ### Calculate IFOV and unresolved range. Print warning if the target goes unresolved.

    IFOV = math.atan(d / f)
    print("IFOV = ", str(IFOV), " [rad]")

    unresolved_range = tgt_size / IFOV
    print("Unresolved range = ", str(unresolved_range), " [m]")

    hundred_pix_on_target_range = tgt_size / IFOV / 10
    print("100 pixels on ", input_params["Run Name"] , " at ", hundred_pix_on_target_range, " [m]")

    if(unresolved_range < range_end):
        print("The target becomes unresolved at ", str(unresolved_range), " [m], which is closer than the range end ", str(range_end), " [m]. Verify parameters")


    ### Generate the ranges we want to test at.

    ranges = np.arange(range_start, range_end+1, 200)



    ### Compute power of target reflection as a function of range
    P_lrt = dict()
    mu_lrt = dict()

    P_lpt = dict()
    mu_lpt = dict()

    P_lps = dict()
    mu_lps = dict()

    CNR = dict()

    for range in ranges:
        P_lrt[range] = (laser_pulse_energy / t_int) * tgt_refl * (d**2) * (D_ap**2) * pow(tau_atmos, 2*range/1000) * tau_optics / (range**2) / (f**2) / (laser_div_angle**2) / (math.pi)
        mu_lrt[range] = P_lrt[range] * K_sensor * t_int * QE * wvl / (h * c)

        
        # calculate laser backscatter to from start of range-gate to target
        backscatter_ranges = np.arange(range - (c*t_int/4), range, 0.1)
        backscatter_integrand = np.power(tau_atmos, 2*backscatter_ranges/1000) / np.power(backscatter_ranges, 2)
        backscatter_integral = np.trapz(backscatter_integrand, backscatter_ranges)
        
        # print(backscatter_integral)
        P_lpt[range] = laser_power * (d**2) * (D_ap**2) * beta * backscatter_integral / (f**2) / (laser_div_angle**2)
        mu_lpt[range] = P_lpt[range] * conversion_term


        # calculate laser backscatter to end of range-gate by adding to-target backscatter and past-target backscatter
        backscatter_secondary_ranges = np.arange(range, range + (c*t_int/4), 0.1)
        backscatter_secondary_integrand = np.power(tau_atmos, 2*backscatter_secondary_ranges/1000) / np.power(backscatter_secondary_ranges, 2)
        backscatter_secondary_integral = np.trapz(backscatter_secondary_integrand, backscatter_secondary_ranges) + backscatter_integral
        P_lps[range] = laser_power * (d**2) * (D_ap**2) * beta * backscatter_secondary_integral / (f**2) / (laser_div_angle**2)
        mu_lps[range] = P_lps[range] * conversion_term

        CNR[range] = math.sqrt( ( mu_lrt[range] + mu_lpt[range] - mu_lps[range] )**2  + 0 ) / math.sqrt( (K_sensor * mu_lps[range]) + (K_dark**2 * I_dark * t_int) + (K_sensor**2 * read_noise**2) + (1.0/144.0) )


    # set up the ability to plot the CNR curve from the dictionary
    CNR_for_plot = sorted(CNR.items())
    x, y = zip(*CNR_for_plot)

    
    run_name = input_params["Run Name"]
    with open(run_name, 'w', newline ='') as output:
        writer = csv.writer(output)

        writer.writerow(['', run_name.split('/')[-1][0:-4]])

        for key, value in CNR.items():
            writer.writerow([key, value])
    

    """
    plt.figure()
    plt.semilogy(x, y)
    plt.xlabel("Range [m]")
    plt.ylabel("cSNR")
    plt.xlim([0, 15000])
    #plt.ylim([1, 10**5])
    plt.title(input_params["Run Name"])


    plt.figure()
    mu_lrt_for_plot = sorted(mu_lrt.items())
    x, y = zip(*mu_lrt_for_plot)
    plt.semilogy(x, y)

    mu_lpt_for_plot = sorted(mu_lpt.items())
    x, y = zip(*mu_lpt_for_plot)
    plt.semilogy(x, y)

    mu_lps_for_plot = sorted(mu_lps.items())
    x, y = zip(*mu_lps_for_plot)
    plt.semilogy(x, y)

    plt.xlabel("Range [m]")
    plt.ylabel("Counts [DN]")
    plt.xlim([0, 15000])
    plt.title("Counts in each term")
    plt.legend(["LRT", "LPT", "LPS"])
    


    plt.show()
    """
    
    

if __name__ == '__main__':
    print("\n In run_LRG_radiometry main function...")

    input_files = sys.argv[1:]
    print(input_files)



    # if ONLY one argument is passed to the script, check if it uses a filesystem wildcard. If so, use glob to find matching files.
    if "*" in input_files[0] and len(input_files)==1:
        print("Using glob to expand wildcards...")

        # expand * wildcard
        input_file_list = glob.glob(input_files[0])

        print(input_file_list)
        
        exit


    else:
        input_file_list = input_files


    for filename in input_file_list:
        try:
            run_LRG_radiometry(filename)
        except Exception as e:
            print(e)
            print('Error running radiometry for \"', filename, "\". Check this filepath and file for errors.")



    