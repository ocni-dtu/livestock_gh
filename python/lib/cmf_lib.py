__author__ = "Christian Kongsgaard"
__license__ = "MIT"

# -------------------------------------------------------------------------------------------------------------------- #
# Imports

# Module imports
import collections
import os

# Livestock imports
import livestock.lib.livestock_csv as csv


# Grasshopper imports


# -------------------------------------------------------------------------------------------------------------------- #
# CMF Component Functions

def load_csv(data_path):
    """Loads a csv file with the retention curve data."""

    units, data = csv.read_csv(data_path)

    return units, data


def load_retention_curve(soil_index, properties_dict={}):
    """
    | Loads the retention curve data and converts it into a order dict.
    | If any property is to be overwritten it is also done in this function.

    """
    data_path = os.getenv('APPDATA') + r'\McNeel\Rhinoceros\5.0\scripts\livestock\data\retention_curves.csv'
    units, data = load_csv(data_path)
    property = collections.OrderedDict([('type', str(data[soil_index][0])),
                                        ('k_sat', float(data[soil_index][1])),
                                        ('phi', float(data[soil_index][2])),
                                        ('alpha', float(data[soil_index][3])),
                                        ('n', float(data[soil_index][4])),
                                        ('m', float(data[soil_index][5])),
                                        ('l', float(data[soil_index][6]))
                                        ])

    # Set modified properties
    for key in properties_dict.keys():
        if properties_dict[key]:
            property[key] = properties_dict[key]

    return property


def load_surface_cover(surface_index, properties_dict={}):
    """
    | Loads the surface cover data and converts it into a order dict.
    | If any property is to be overwritten it is also done in this function.

    """

    data_path = os.getenv('APPDATA') + r'\McNeel\Rhinoceros\5.0\scripts\livestock\data\vegetation_data.csv'
    units, data = load_csv(data_path)
    property = collections.OrderedDict([('name', str(data[surface_index][0])),
                                        ('height', float(data[surface_index][1])),
                                        ('lai', float(data[surface_index][2])),
                                        ('albedo', float(data[surface_index][3])),
                                        ('canopy_closure', float(data[surface_index][4])),
                                        ('canopy_par', float(data[surface_index][5])),
                                        ('canopy_capacity', float(data[surface_index][6])),
                                        ('stomatal_res', float(data[surface_index][7])),
                                        ('root_depth', float(data[surface_index][8])),
                                        ('root_fraction', float(data[surface_index][9])),
                                        ('leaf_width', float(data[surface_index][10])),
                                         ])

    # Set modified properties
    for key in properties_dict.keys():
        if properties_dict[key]:
            property[key] = properties_dict[key]

    return property