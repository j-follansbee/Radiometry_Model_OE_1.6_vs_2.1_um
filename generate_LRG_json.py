import json
import numpy as np



visibilities = ['23km', '5km', 'haze']
wvls = {'SWIR':1.6*pow(10,-6), 'eSWIR':2.1*pow(10,-6)}
laser_attenuation = {"SWIR":{"23km":0.9613, "5km":0.8373, "haze":0.67}, "eSWIR":{"23km":0.9649, "5km":0.8844, "haze":0.721}}

backscatter_coeff = {'SWIR':5*pow(10, -8), 'eSWIR':1*pow(10, -8)} # [1/m/sr]
read_noise = {'SWIR':40, 'eSWIR':80} # [e-]
dark_current = {'SWIR':24240, 'eSWIR':24240} # [e-/pix/s]

# targets
targets = list()
targets.append(["drone", 0.1, { "SWIR":0.74, "eSWIR":0.2 } ])
targets.append(["steel", 0.292, { "SWIR":0.7, "eSWIR":0.75 } ])
targets.append(["aluminum", 0.47, { "SWIR":0.97, "eSWIR":0.98 } ])

for vis in visibilities:
    for band in wvls:
        for target in targets:

            output_data = dict()

            name = band + "_" + target[0] + "_" + vis
            output_data["Wavelength [m]"] = wvls[band]
            output_data["Target Size [m]"] = target[1]
            output_data["Target Reflectivity"] = target[2][band]
            output_data["Atmospheric Attenuation [1/km]"] = laser_attenuation[band][vis]

            output_data["Run Name"] = "./LRG_output_csvs/" + name + ".csv"
            output_data["Filename"] = "./LRG_input_jsons/" + name + ".json"
            output_data["Range Start [m]"] = 200
            output_data["Range End [m]"] = 15000
            output_data["Laser Pulse Energy [J]"] = 0.2
            output_data["Laser Pulse Duration [s]"] = 4 * pow(10, -9)
            output_data["Laser Divergence Angle [rad]"] = 0.0022
            output_data["Baseline Distance [m]"] = 0.05
            output_data["Background Reflectivity [n/a]"] = 0
            output_data["Aperture Diameter [m]"] = 0.1
            output_data["Optics Transmission [n/a]"] = 0.9
            output_data["Focal Length [m]"] = 0.4
            output_data["Detector Size [m]"] = 5 * pow(10, -6)
            output_data["Integration Time"] = 1 * pow(10, -7)
            output_data["Detector QE [e-/photon]"] = 0.70
            output_data["Sensor Gain [DN/e-]"] = 1
            output_data["Dark Current Gain [DN/e-]"] = 1
            
            output_data["Dark Current [e-/s]"] = dark_current[band]
            output_data["Read Noise [e-]"] = read_noise[band]
            output_data["Beta [1/sr/m]"] = backscatter_coeff[band]

            focal_plane_format = 640
            
            fov = np.arctan(focal_plane_format* output_data["Detector Size [m]"] / output_data["Focal Length [m]"])
            output_data["R Near [m]"] = output_data["Baseline Distance [m]"] / (np.tan( fov/2 ) + np.tan( output_data["Laser Divergence Angle [rad]"]/2))

            print(output_data["R Near [m]"])

            with open(output_data["Filename"], 'w') as f_out:
                json.dump(output_data, f_out)



