import icoscp_core.sites as sites
from typing import List, Dict, Union


def get_sites_stations_list(inactive_stations_ids=["TRS"])->List(Dict[str, Union[str, int, float]]):
    """
    Retrieves a list of stations from the ICOS-CP API and compiles their details into a list of dictionaries.
    The function allows specifying which stations should be marked as 'inactive'.

    Args:
        inactive_stations_ids (list of str, optional): A list of station IDs that should be marked as 'inactive'. 
            Default is ["TRS"].

    Returns:
        List[Dict[str, Union[str, float]]]: A list of dictionaries, each containing details of a station. 
        The keys in the dictionary are 'id', 'name', 'status', 'latitude', 'longitude', and 'uri'.

    Raises:
        ConnectionError: If there is an issue connecting to the ICOS-CP API.
        ValueError: If the data returned from the API is not in the expected format.

    Note:
        - The function assumes the existence of 'sites.meta.list_stations()' method from the ICOS-CP API.
        - It's important to handle potential errors to prevent the application from crashing due to unforeseen issues.
    """
    stations = []

    try:
        # Attempt to get the list of stations from the ICOS-CP API
        station_data = sites.meta.list_stations()
    except Exception as e:
        raise ConnectionError(f"Error connecting to the ICOS-CP API: {e}")

    for dobj in station_data:
        try:
            # Check for expected attributes in each station object
            if not all(hasattr(dobj, attr) for attr in ['id', 'name', 'lat', 'lon', 'uri']):
                raise ValueError(f"Station object is missing one or more required attributes: {dobj}")

            # Determine the status of the station
            status = 'inactive' if dobj.id in inactive_stations_ids else 'active'

            # Append station details to the list
            stations.append({
                'id': dobj.id, 
                "name": dobj.name, 
                'status': status, 
                "latitude": dobj.lat, 
                "longitude": dobj.lon, 
                "uri": dobj.uri
            })
        except ValueError as ve:
            # Optionally log the error or handle it as needed
            print(f"Data format error: {ve}")
            continue  # Skip this station and continue with the next one

    return stations
