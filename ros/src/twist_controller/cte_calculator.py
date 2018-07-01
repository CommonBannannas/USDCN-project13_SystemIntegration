import numpy as np

def get_xy_from_waypoints(waypoints):

    return list(map(lambda waypoint: [waypoint.pose.pose.position.x, waypoint.pose.pose.position.y], waypoints))


def get_cross_track_error(final_waypoints, current_pose):

    origin = final_waypoints[0].pose.pose.position

    waypoints_matrix = get_xy_from_waypoints(final_waypoints)


    shifted_matrix = waypoints_matrix - np.array([origin.x, origin.y])


    offset = 15
    angle = np.arctan2(shifted_matrix[offset, 1], shifted_matrix[offset, 0])
    rotation_matrix = np.array([
            [np.cos(angle), -np.sin(angle)],
            [np.sin(angle), np.cos(angle)]
        ])

    rotated_matrix = np.dot(shifted_matrix, rotation_matrix)


    degree = 3
    coefficients = np.polyfit(rotated_matrix[:, 0], rotated_matrix[:, 1], degree)

    # Transform the current pose of the car to be in the car's coordinate system
    shifted_pose = np.array([current_pose.pose.position.x - origin.x, current_pose.pose.position.y - origin.y])
    rotated_pose = np.dot(shifted_pose, rotation_matrix)

    expected_y_value = np.polyval(coefficients, rotated_pose[0])
    actual_y_value = rotated_pose[1]

    return expected_y_value - actual_y_value
