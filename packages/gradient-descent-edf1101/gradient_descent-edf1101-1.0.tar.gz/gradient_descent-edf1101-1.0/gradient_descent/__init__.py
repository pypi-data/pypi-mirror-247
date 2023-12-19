"""
Gradient Descent module written by https://github.com/edf1101/
for my University Computer Science Degree

## Info
Modules Used
- Matplotlib (if you want to visualise)
- Random (If you want to create random set of training data / train-test-split)

Learning Parameters (for OK results)
- Quartic - learning = 0.0000000003
- Cubic - learning = 0.00000003
- Quadratic - learning = 0.000001
- Linear - learning = 0.0003
In general for each extra polynomial term you add it should be ~100x smaller.
Smaller learning rates may get better results but you will need to have more
 attempts to reach it since it learns slower
"""


def line(x_coordinate: float, coefficients: list[float]) -> float:
    """
    Returns the y-value of a function with given coefficients for any value x

    :param x_coordinate: the x value we're using
    :param coefficients: Coefficients of the line
    :return: y value
    """
    y_coordinate = 0
    for i in range(len(coefficients)):
        y_coordinate += coefficients[-i - 1] * (x_coordinate**i)

    return y_coordinate


def get_coordinates_x(points: list[tuple[float, float]]) -> list[float]:
    """
    For a list of points in the form [ [x1,y1],[x2,y2]...] it returns all the x coordinates

    :param points: A list of all the points to get x coordinates from
    :return: A list of the x coordinates
    """
    return [i[0] for i in points]


def get_coordinates_y(points: list[tuple[float, float]]) -> list[float]:
    """
    For a list of points in the form [ [x1,y1],[x2,y2]...] it returns all the y coordinates

    :param points: A list of all the points to get y coordinates from
    :return: A list of the y coordinates
    """
    return [i[1] for i in points]


def sum_of_squared_residuals(
    coefficients: list[float], points: list[tuple[float, float]]
) -> float:
    """
    The loss function for we are using, in this case the sum of squared residuals function

    :param coefficients: The coefficients of the line to Test
    :param points: A list of points in the dataset
    :return: the value of the loss function
    """

    result = 0
    for x_coordinate, y_coordinate in zip(get_coordinates_x(points), get_coordinates_y(points)):

        # add on the squared difference between the real value and predicted
        result += (y_coordinate - line(x_coordinate, coefficients)) ** 2

    return result


def get_rss_dif(
    coefficients: list[float], points: list[tuple[float, float]], respect_to: int) -> float:
    """
    Get the derivative of the RSS curve at a specific point to calcualte the step needed

    :param coefficients: The coefficients we're trying
    :param points: The points in the dataset
    :param respect_to: What parameter we're differentiating with respect to
    :return: the gradient
    """

    # given the derivative is calculated as a sum we can just use a sum of smaller
    # derivatives to make it more readable
    derivative = 0

    for point in points:  # Go through each point in the dataset
        # calculate the derivative of the RSS graph that this points adds
        mult = -2 * (point[0] ** (len(coefficients) - respect_to - 1))
        calc = point[1] - line(point[0], coefficients)
        part_derivative = mult * calc

        derivative += part_derivative  # add it on to the total derivative

    return derivative


def gradient_descent(
    coefficient_count: int,
    points: list[tuple[float,float]],
    learning_rate: float = -1,
    attempts: int = 50000,
    debug: bool = False,
) -> list[float]:
    """
    This algorithm iterates the predicted parameters according to the dataset of points

    :param coefficient_count: how many coefficients we want to try and map this to
    :param points: The points to train from
    :param learning_rate: Default -1 -> it will automatically choose if less than quintic,
     otherwise specify it here
    :param attempts: Max attempts before it gives up
    :param debug: Print debug messages about how the algorithm is going
    :return: array of predicted parameters
    """

    temp_coeff = [
        0 for i in range(coefficient_count)
    ]  # array of predicted coefficients (all start at 0)

    temp_steps = [
        0 for i in range(coefficient_count)
    ]  # array of next step size for all coefficients (all start at 0)

    # If learning rate = -1 then assign it a learning rate that will be OK
    # (not perfect) as long as below 5th degree

    if learning_rate == -1:
        match coefficient_count:
            case 0:
                # cant have no coefficients
                raise ValueError(
                    "Cant have no coefficients must be 1 ≤ coefficient_count"
                )

            case 1:
                # finding horizontal line boring
                learning_rate = 0.0003
            case 2:
                learning_rate = 0.00001  # linear
            case 3:
                learning_rate = 0.000001  # quadratic
            case 4:
                learning_rate = 0.00000003  # cubic
            case 5:
                learning_rate = 0.0000000003  # quartic
            case _:
                # We don't have default values for above 5 coefficients
                # so need to specify learning rate
                raise ValueError(
                    "No default values for when coefficent count> 5 please specify learning rate"
                )

    alphabet = "abcdefghijklmnopqrstuvwxyz"  # used for coefficient names when debugging

    for i in range(attempts):  # So it runs out when gets to max attempts
        if debug:  # If debugging print what iteration
            print(f"\niter {i}")

        # For each coefficient calculate its derivative, then step size, then modify coefficient
        for i in range(coefficient_count):
            temp_steps[i] = -learning_rate * get_rss_dif(temp_coeff, points, i)

            if debug:  # Debugging print data
                print(f"{alphabet[i]} = {temp_coeff[i]}")
                print(f"step_{alphabet[i]} = {temp_steps[i]}")

            temp_coeff[i] += temp_steps[i]

        # Used to check if all the coefficients are below the threshold
        # for acceptable step sizes ie if step sizes are all <0.0001 then we have
        # found a happy set of coefficients and can stop
        all_below = True
        for i in temp_steps:
            if abs(i) > 0.0001:
                all_below = False

        if all_below:
            break

    return temp_coeff


def score(points: list[tuple[float, float]], coefficients: list[float]) -> float:
    """
    Should perform an R^2 scoring metric with the points against the estimated parameters

    :param points: List of all points to score against
    :param coefficients: The coefficients to test against
    :return: Score between 0-1  where 0 Is awful correlation & 1 is perfect
    """

    return (sum_of_squared_residuals(coefficients, points) ** 0.5) / len(points)
