from numpy import radians, degrees, pi, sin, cos, tan, arctan2, sqrt
from numpy.testing import assert_allclose

# Computes the midpoint, along a great-circle, between two points on a sphere.
# Returns the midpoint's latitude (deg), longitude (deg), and azimuth (deg)
def spherical_midpoint(lat1, lon1, lat2, lon2):
    lat1r = radians(lat1)
    lon1r = radians(lon1)
    lat2r = radians(lat2)
    lon2r = radians(lon2)

    lon12 = lon2r - lon1r
    if lon12 < -pi:
        lon12 += (2*pi)
    elif lon12 > pi:
        lon12 -= (2*pi)
        
    # This is the angle of the great-circle, relative to north, where it intersects p1 (lat1, lon1).
    initial_course = arctan2(
                        cos(lat2r)*sin(lon12),
                        cos(lat1r)*sin(lat2r) - sin(lat1r)*cos(lat2r)*cos(lon12)
                    )
    central_angle = arctan2(
                        sqrt((cos(lat1r)*sin(lat2r) - sin(lat1r)*cos(lat2r)*cos(lon12))**2 + (cos(lat2r)*sin(lon12))**2), 
                        sin(lat1r)*sin(lat2r) + cos(lat1r)*cos(lat2r)*cos(lon12)
                    )

    # The node is the location where the great circle crosses the equator in the northward direction.
    # The azimuth is the angle that the great circle crosses the equator, relative to north.
    node_azimuth = arctan2(
                        sin(initial_course)*cos(lat1r),
                        sqrt(cos(initial_course)**2 + (sin(initial_course)*sin(lat1r))**2)
                    )
    # angular distances along the great circle from the node to the two points
    angle01 = arctan2(tan(lat1r), cos(initial_course))
    angle02 = angle01 + central_angle
    node_lon = lon1r - arctan2(sin(node_azimuth)*sin(angle01), cos(angle01))

    # angular distance along great circle from node to midpoint
    midpoint_angle = (angle01 + angle02) / 2

    midpoint_lat = arctan2(
                        cos(node_azimuth)*sin(midpoint_angle),
                        sqrt(cos(midpoint_angle)**2 + (sin(node_azimuth)*sin(midpoint_angle))**2)
                    )
    midpoint_lon = node_lon + arctan2(sin(node_azimuth)*sin(midpoint_angle), cos(midpoint_angle))
    if midpoint_lon > pi:
        midpoint_lon -= 2*pi
    elif midpoint_lon < -pi:
        midpoint_lon += 2*pi
    midpoint_azimuth = arctan2(tan(node_azimuth), cos(midpoint_angle))

    return degrees(midpoint_lat), degrees(midpoint_lon), degrees(midpoint_azimuth)

def test_midpoint():
    p1 = (2, 30)
    p2 = (4, -150)
    expected_results = [89, 30, 0]
    actual_results = spherical_midpoint(*p1, *p2)
    assert_allclose(actual_results, expected_results, atol=1e-8)
    p1 = (0, 47)
    p2 = (0, -59)
    expected_results = [0, -6, -90]
    actual_results = spherical_midpoint(*p1, *p2)
    assert_allclose(actual_results, expected_results, atol=1e-8)
    p1 = (0.01, 0.01)
    p2 = (-0.01, -0.01)
    expected_results = [0, 0, -135]
    actual_results = spherical_midpoint(*p1, *p2)
    assert_allclose(actual_results, expected_results, atol=1e-8)

test_midpoint()
