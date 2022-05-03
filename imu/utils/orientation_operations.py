from venv import create
import serial_operations as serial_op
import math
import numpy as np

READ_FILT_TARED_QUAT_COMMAND = 0
READ_FILT_QUAT_COMMAND = 6
READ_NORTH_GRAVITY_COMMAND = 12
SET_TARE_QUAT_COMMAND = 97

def calculate_angle(vector0, vector1, vector2=None):
    # The max and min is used to account for possible floating point erro
    dot_product = max(min(np.dot(vector0, vector1), 1.0), -1.0)
    angle = math.acos(dot_product)
    if vector2 is not None:
        axis = normalize_vector(np.cross(vector0, vector1))
        angle = math.copysign(angle, np.dot(vector2, axis))
    return angle

def vector_len(vector):
    return (np.dot(vector, vector))**0.5

def normalize_vector(vector):
    length = vector_len(vector)
    x, y, z = vector
    return [x/length, y/length, z/length]

def create_quaternion(vector, angle):

    x, y, z = vector
    quat = [0.0] * 4
    quat[0] = x * math.sin(angle/2.0)
    quat[1] = y * math.sin(angle/2.0)
    quat[2] = z * math.sin(angle/2.0)
    quat[3] = math.cos(angle/2.0)

    # Normalize quaternion
    qx, qy, qz, qw = quat
    length = (qx * qx + qy * qy + qz * qz + qw * qw)**(0.5)

    quat[0] /= length
    quat[1] /= length
    quat[2] /= length
    quat[3] /= length

    return quat

def multiply_quaternions(quat0, quat1):
    x0, y0, z0, w0 = quat0
    x1, y1, z1, w1 = quat1

    x_cross, y_cross, z_cross = np.cross([x0, y0, z0], [x1, y1, z1])

    w_new = w0 * w1 - np.dot([x0, y0, z0], [x1, y1, z1])
    x_new = x1 * w0 + x0 * w1 + x_cross
    y_new = y1 * w0 + y0 * w1 + y_cross
    z_new = z1 * w0 + z0 * w1 + z_cross

    return [x_new, y_new, z_new, w_new]

def get_offset_quaternion(serial_port, logical_id, gravity=[-1.0, 0.0, 0.0]):
    north_gravity = serial_op.write_command_read_answer(serial_port, 
                                                        [logical_id], 
                                                        READ_NORTH_GRAVITY_COMMAND)
                     
    sensor_gravity = north_gravity[0][6:]
    print("sensor_gravity: ", sensor_gravity)

    filtered_orientation = serial_op.write_command_read_answer(serial_port, 
                                                        [logical_id], 
                                                        READ_FILT_QUAT_COMMAND)[0][3:]
    print("quat: ", filtered_orientation)

    angle = calculate_angle(sensor_gravity, gravity)
    print("angle: ", angle)

    axis = normalize_vector(np.cross(sensor_gravity, gravity))
    print("axis: ", axis)
    
    offset = create_quaternion(axis, -angle)

    tare_data = multiply_quaternions(filtered_orientation, offset)

    serial_op.write_command_read_answer(serial_port, 
                                        [logical_id], 
                                        SET_TARE_QUAT_COMMAND, 
                                        tare_data)

    return offset

def quaternion_vector_multiplication(quat, vector):
    # quat*vect_quat * -quat
    qx, qy, qz, qw = quat
    vx, vy, vz = vector
    vw = 0.0
    neg_qx = -qx
    neg_qy = -qy
    neg_qz = -qz
    neg_qw = qw

    # First
    x_cross, y_cross, z_cross = np.cross([qx, qy, qz], vector)
    w_new = qw * vw - np.dot([qx, qy, qz], vector)
    x_new = vx * qw + qx * vw + x_cross
    y_new = vy * qw + qy * vw + y_cross
    z_new = vz * qw + qz * vw + z_cross

    # Second
    x_cross, y_cross, z_cross = np.cross([x_new, y_new, z_new], [neg_qx, neg_qy, neg_qz])
    w = w_new * neg_qw - np.dot([x_new, y_new, z_new], [neg_qx, neg_qy, neg_qz])
    x = neg_qx * w_new + x_new * neg_qw + x_cross
    y = neg_qy * w_new + y_new * neg_qw + y_cross
    z = neg_qz * w_new + z_new * neg_qw + z_cross

    return [x, y, z]


def calculate_device_vector(serial_port, logical_id, vector_ref, offset_quat):
    data = serial_op.write_command_read_answer(serial_port, 
                                               [logical_id], 
                                               READ_FILT_TARED_QUAT_COMMAND)[0][3:]

    quat =  multiply_quaternions(data, offset_quat)

    vector = quaternion_vector_multiplication(quat, vector_ref)

    return vector

def calculate_roll_pitch_yaw():
    pass