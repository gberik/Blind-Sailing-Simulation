def calculate_closest(pos1, vel1, pos2, vel2, time=10, step=.1, allowable_dist=5.0):
    """
    :param pos1: Tuple of Lat, Lon of 1st object, in degrees
    :param vel1: Tuple of Vel, Bearing of 1st object, in m/s and degrees respectively
    :param pos2: Tuple of Lat, Lon of 2st object, in degrees
    :param vel2: Tuple of Vel, Bearing of 2st object, in m/s and degrees respectively
    :param time: Maximum number of seconds to check for. Should not affect calculation time significantly
    unless the objects will not pass their closest point for a long time
    :param step: Step between position calculations, in seconds
    Smaller steps will have greater precision, but take longer to calculate
    :param allowable_dist: Closest approach between objects considered safe, in meters. Default 5.0 meters
    :return: Tuple: whether closest approach < allowable, first time they violate allowable (None if does not happen),
    minimum distance between objects (in meters), time when minimum distance occurs
    """
    # TODO cleanup what this returns
    # TODO If computational time is an issue, replace slow loop with binary search
    end = time / step
    min_dist = 10000000000000.0  # Closest approach
    first_time = None  # Time when they first violate safety bound
    int_time = 1000000000.0  # Time when they reach the closest point
    for x in range(0, end):
        pos_a = calculate_future_pos(pos1, vel1, x * step)
        pos_b = calculate_future_pos(pos2, vel2, x * step)
        distance = VincentyDistance(pos_a, pos_b).meters

        print((pos_a, pos_b))
        if distance < min_dist:  # if it's a new minimum, keep track of it
            min_dist = distance
            int_time = x / step
            if distance < allowable_dist and first_time is None:
                # if no min is set, this is the first unsafe time, so we want to know about it
                first_time = x / step

        if distance > min_dist:
            # Given we are plotting two lines, if they've gotten further apart, we're done
            break

    if min_dist < allowable_dist:
        print((True, first_time, min_dist, int_time))
        return True, first_time, min_dist, int_time
    else:
        print((False, first_time, min_dist, int_time))
        return False, first_time, min_dist, int_time

