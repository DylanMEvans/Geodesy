from numpy import radians, sin, cos, arccos

"""
dist_scaler is equivalent to Earth's radius in miles
- Earth's radius (spherical approximation): 3443.8985 nautical miles
- 1852 meters per nautical mile
- 1609.344 meters per mile
"""
dist_scaler = 3443.8985 * 1852 / 1609.344

# returns the great-circle distance, in miles
def dist(lat1, lon1, lat2, lon2):
	lat1r = radians(lat1)
	lon1r = radians(lon1)
	lat2r = radians(lat2)
	lon2r = radians(lon2)

	return arccos(
			sin(lat1r) * sin(lat2r)
			+ cos(lat1r) * cos(lat2r) 
			* cos(lon2r - lon1r)
		) * dist_scaler