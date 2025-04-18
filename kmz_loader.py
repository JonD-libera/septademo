import xml.etree.ElementTree as ET
from zipfile import ZipFile

def load_stations_from_kmz(file_path):
    with ZipFile(file_path) as kmz:
        with kmz.open("doc.kml") as f:
            tree = ET.parse(f)
            root = tree.getroot()

            ns = {"kml": "http://www.opengis.net/kml/2.2"}

            placemarks = root.findall(".//kml:Placemark", ns)
            stations = []

            for placemark in placemarks:
                name = placemark.find("kml:name", ns)
                point = placemark.find(".//kml:Point/kml:coordinates", ns)

                if point is not None and name is not None:
                    coords = point.text.strip().split(",")
                    if len(coords) >= 2:
                        stations.append({
                            "name": name.text.strip(),
                            "lat": float(coords[1]),
                            "lon": float(coords[0])
                        })

            return stations
