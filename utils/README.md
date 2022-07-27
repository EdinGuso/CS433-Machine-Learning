# Utilities
This directory has only one script which maps health facility codes to city names and geographic coordinates.

### Directory Files
  - **[get_locations.py](./get_locations.py):** This script contains dictionaries to map health facility numbers to health facility names and the cities they are located in. It also utilizes `geopy` API to get GPS coordinates of those cities and save them in a file called `gps_coordinates.json`.

    Usage
    ``` shell
    python get_coordinates.py --save_path SAVE_DIRECTORY
    ```

      Arguments:
    * `--save_path`: Path for storing gps coordinates. If no path is provided, file will be dumped to the current directory.