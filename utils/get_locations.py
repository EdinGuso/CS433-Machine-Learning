from geopy.geocoders import Nominatim
import argparse
import os
import json

HEALTH_FACILITY_NAMES = {
    # Project: RCA-1, Batangafo
    1 : "OPD de l'hôpital",
    2 : "OPD de l'hôpital",
    
    # Project: RCA-1, Batangafo
    3 : "Kambakota",
    
    # Project: RCA-2, Kabo
    801 : "OPD de l'hôpital",
    802 : "Moyenne Sido",
    
    # Project: Niger-1, Diffa
    101 : "Garin Wanzam",
    102 : "Garin Wanzam",
    103 : "Garin Wanzam",
    
    # Project: Niger-2, Diffa
    601 : "Kintchandi",
    602 : "Kintchandi",
    603 : "Kintchandi",
    
    # Project: Nigeria-1, No detailed info is available
    201 : "Nigeria",
    
    # Project: Nigeria-2, No detailed info is available
    202 : "Nigeria",
    
    # Project: Tanzania-1, Nduta
    301 : "HP",
    302 : "HP",
    303 : "HP",
    304 : "HP",
    305 : "HP",
    306 : "HP",
    
    # Project: Mali-1, Ansongo
    401 : "Hourara",

    # Project: Mali-2, Douentza
    411 : "Boni",
    412 : "Hombori",
    413 : "Boni",

    # Project: Mali-3, Kidal
    421 : "Central",
    422 : "Abeibara",

    # Project: Mali-4, Koutiala
    431 : "Bobola Zangasso",
    432 : "Konina",
    433 : "Djitamana",
    
    # Project: Tchad-1, No detailed info is available
    501 : "Tchad",
    502 : "Tchad",
    
    # Project: Kenya-1, Dagahaley
    701 : "HP4",
    702 : "HP7",
    
}

HEALTH_FACILITY_TOWNS = {
    # Project: RCA-1, Batangafo
    1 : "Batangafo",
    2 : "Batangafo",
    
    # Project: RCA-1, Batangafo
    3 : "Kambakota",
    
    # Project: RCA-2, Kabo
    801 : "Kabo",
    802 : "Moyenne Sido",
    
    # Project: Niger-1, Diffa
    101 : "Garin Wanzam",
    102 : "Garin Wanzam",
    103 : "Garin Wanzam",
    
    # Project: Niger-2, Diffa
    601 : "Diffa", # Kintchandi isn't recognized by the geopy API so use Diffa instead
    602 : "Diffa", # Kintchandi isn't recognized by the geopy API so use Diffa instead
    603 : "Diffa", # Kintchandi isn't recognized by the geopy API so use Diffa instead
    
    # Project: Nigeria-1, No detailed info is available
    201 : "Nigeria",
    
    # Project: Nigeria-2, No detailed info is available
    202 : "Nigeria",
    
    # Project: Tanzania-1, Nduta
    301 : "Nduta",
    302 : "Nduta",
    303 : "Nduta",
    304 : "Nduta",
    305 : "Nduta",
    306 : "Nduta",
    
    # Project: Mali-1, Ansongo
    401 : "Hourara",

    # Project: Mali-2, Douentza
    411 : "Boni",
    412 : "Hombori",
    413 : "Boni",

    # Project: Mali-3, Kidal
    421 : "Kidal",
    422 : "Abeibara",

    # Project: Mali-4, Koutiala
    431 : "Bobola Zangasso",
    432 : "Konina",
    433 : "Djitamana",
    
    # Project: Tchad-1, No detailed info is available
    501 : "Tchad",
    502 : "Tchad",
    
    # Project: Kenya-1, Dagahaley
    701 : "Dagahaley",
    702 : "Dagahaley",
    
}

COUNTRIES_TOWNS = {
    "CAR" : [ # RCA
        "Batangafo",
        "Kambakota",
        "Kabo",
        "Moyenne Sido",
    ],
        
    "Niger" : [
        "Garin Wanzam",
        "Diffa", # Kintchandi isn't recognized by the geopy API so use Diffa instead
    ],

    "Nigeria" : [
        "Nigeria",
    ],
    
    "Tanzania" : [
        "Nduta",
    ],
    
    "Mali" : [
        "Hourara",
        "Boni",
        "Hombori",
        "Boni",
        "Kidal",
        "Abeibara",
        "Bobola Zangasso",
        "Konina",
        "Djitamana",
    ],
    
    "Tchad" : [
        "Tchad",
    ],
        
    "Kenya" : [
        "Dagahaley",
    ]

}

def GetLocations(output_dir):
    gps_coordiantes_hf = {}

    geolocator = Nominatim(user_agent="MLProject2")

    for country, town_list in COUNTRIES_TOWNS.items():
        for town in town_list:
            query = f"{town} {country}"
            location = geolocator.geocode(query)
            gps_coordiantes_hf[town] = [location.latitude, location.longitude]

    filename = 'gps_coordinates.json'
    output_path = os.path.join(output_dir, filename)
    with open(output_path, 'w') as file:
        json.dump(gps_coordiantes_hf, file, indent=4)

if __name__ == "__main__":

    arg_parser = argparse.ArgumentParser(
        description='Get GPS coordinates of health centers using geopy API'
    )

    arg_parser.add_argument(
        '-o', '--save_path', 
        dest='save_path',
        required=False,
        default='./',
        help='Path for storing gps coordinates. If no path is provided, file will be dumb the current directory.'
    )

    args = arg_parser.parse_args()
    output_dir = args.save_path


    GetLocations(output_dir)