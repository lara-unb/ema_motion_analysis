from pyquaternion import Quaternion # http://kieranwynn.github.io/pyquaternion/
import math

def convert_quaternion_to_unit_quaternion_if_needed(quaternion : Quaternion):
    """ Convert a quarternion in a unit quaternion if isn't.

    Args:
        quaternion: Quaternion object
    Returns:
        Unit quaternion
    """
    if(quaternion.is_unit):
        return quaternion
    else:
        return quaternion/quaternion.norm


def calculate_angle_between_quaternions(firstQuaternion : Quaternion, 
                                        secondQuaternion : Quaternion):
    """ Calculate angle between two quaternions

    Args:
        firstQuaternion: Quaternion object
        secondQuaternion: Quaternion object
    Returns:
        Angle between quaternions in degrees
    """
    firstQuaternionObject = Quaternion(firstQuaternion[0], firstQuaternion[1], firstQuaternion[2], firstQuaternion[3])
    secondQuaterionObject = Quaternion(secondQuaternion[0], secondQuaternion[1], secondQuaternion[2], secondQuaternion[3])

    firstQuaternionObject = convert_quaternion_to_unit_quaternion_if_needed(firstQuaternionObject)
    secondQuaterionObject = convert_quaternion_to_unit_quaternion_if_needed(secondQuaterionObject)

    resultantQuaternion = firstQuaternionObject.conjugate * secondQuaterionObject

    angleDegrees = 2 * math.degrees(math.acos(resultantQuaternion[0]))
    return angleDegrees


# Check quaternion operations in isolation
# Source to check: https://www.mathworks.com/matlabcentral/answers/415936-angle-between-2-quaternions
# See for answers!!! 
if __name__ == '__main__':
    resultantQuaternion = calculate_angle_between_quaternions([ 0.968, 0.008, -0.008, 0.252], [ 0.382, 0.605,  0.413, 0.563])
    print(resultantQuaternion)