import os.path

import geopandas as gpd
import requests
import overpy
from shapely import Point, Polygon, GeometryCollection
from pprint import pprint
import time


class OpenStreetMap:
    def __init__(self):
        self.api = overpy.Overpass()
        self.max_retries = 10

    def perform_overpass_query(query):
        overpass_url = "https://overpass-api.de/api/interpreter"
        response = requests.get(overpass_url, params={"data": query})
        return response.json()

    def download_water_polygons(self, bbox, output_dir, name):
        output_fp = os.path.join(output_dir, f"water_{name}.gpkg")
        if not os.path.exists(output_fp):
            # Define the Overpass QL query to retrieve water ways within the specified bounding box
            query_ways = f"""
                   way({bbox})["water"];
                   (._;>;);
                    out geom;
               """
            retry_count = 0
            while retry_count < self.max_retries:
                try:
                    result_ways = self.api.query(query_ways)
                    # Break out of the retry loop if successful
                    break
                except Exception as e:
                    retry_count += 1
                    if retry_count < self.max_retries:
                        time.sleep(5)

            features = []
            for way in result_ways.ways:
                feature = {}
                for key in way.tags:
                    feature[key] = way.tags.get(key, "n/a")
                nodes = []
                for node in way.nodes:
                    nodes.append([float(node.lon), float(node.lat)])
                    # p = Point(node.lon, node.lat)
                    # nodes.append(p)
                    # print("    Lat: %f, Lon: %f" % (node.lat, node.lon))
                if len(nodes) >= 4:
                    feature["geom"] = Polygon(nodes)
                else:
                    feature["geom"] = GeometryCollection()
                # final_result.append(res)
                features.append(feature)
            if len(features) > 0:
                gdf = gpd.GeoDataFrame(features, geometry="geom")
                gdf.to_file(output_fp, driver="GPKG")
        # print(f"download completed at {output_fp}")


if __name__ == "__main__":
    # Specify the bounding box (format: south, west, north, east)
    bounding_box = "35.0,-130.0,40.0,-120.0"
    # boundin
    # Specify the output GeoJSON file
    output_geojson_file = "water_polygons.geojson"

    # Download water polygons and save them to the GeoJSON file
    OpenStreetMap.download_water_polygons(bounding_box, output_geojson_file)

    print(f"Water polygons downloaded and saved to {output_geojson_file}")
