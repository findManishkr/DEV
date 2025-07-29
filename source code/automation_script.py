

#____________________Kochi_____________________#

import cdsapi

client = cdsapi.Client()

dataset = "reanalysis-era5-pressure-levels"

# Month day mapping (2021 is not a leap year)
months = {
    "01": ("January", 31),
    "02": ("February", 28),
    "03": ("March", 31),
    "04": ("April", 30),
    "05": ("May", 31),
    "06": ("June", 30),
    "07": ("July", 31),
    "08": ("August", 31),
    "09": ("September", 30),
    "10": ("October", 31),
    "11": ("November", 30),
    "12": ("December", 31),
}

# Coordinates for Kochi bounding box (North, West, South, East)
# Approximate bounding box for Kochi:
# North latitude: 10.05
# South latitude: 9.85
# West longitude: 76.15
# East longitude: 76.35

common_request = {
    "product_type": ["reanalysis"],
    "variable": [
        "divergence",
        "fraction_of_cloud_cover",
        "geopotential",
        "ozone_mass_mixing_ratio",
        "potential_vorticity",
        "relative_humidity",
        "specific_cloud_ice_water_content",
        "specific_cloud_liquid_water_content",
        "specific_humidity",
        "specific_rain_water_content",
        "specific_snow_water_content",
        "temperature",
        "u_component_of_wind",
        "v_component_of_wind",
        "vertical_velocity",
        "vorticity"
    ],
    "year": ["2021"],
    "time": [f"{i:02d}:00" for i in range(24)],
    "pressure_level": ["950"],
    "data_format": "netcdf",
    "download_format": "unarchived",
    "area": [10.05, 76.15, 9.85, 76.35]  # Kochi bounding box (North, West, South, East)
}

# Loop through each month
for month_num, (month_name, last_day) in months.items():
    for part, day_range in [("1_to_16", range(1, 17)), ("17_to_end", range(17, last_day + 1))]:
        if not day_range:
            continue  # Skip empty ranges

        # Build request
        request = common_request.copy()
        request["month"] = [month_num]
        request["day"] = [f"{day:02d}" for day in day_range]

        filename = f"kochi_2021_{month_name}_{part}.nc"

        print(f"Downloading {filename} ...")
        client.retrieve(dataset, request).download(filename)
        print(f"{filename} downloaded successfully.")
