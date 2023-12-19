"""
Gradient Descent module written by https://github.com/edf1101/ for my
University Computer Science Degree

This submodule is used for creating sets of random points and for displaying
them using matplotlib, ie mainly for demo purposes.

## External Modules needed
- Random library for generating random points / offsets
- If you want to use any of the graph plotting features you need matplotlib imported
  in the code where you call the functions
"""

import random
from typing import Any
import gradient_descent as gd


def create_points(coefficients: list[float], point_count: int = 100,
                  offset_range: float = 0.5) -> list[tuple[float, float]]:
    """
    Creates a set of random points that follow a line with (optionally) a slight offset

    :param coefficients: The coefficients of the line to follow
    :param point_count: how many points to generate (default = 100)
    :param offset_range: How big you want the offset to be from actual line
    :return: Array of points
    """

    points = []
    for _ in range(point_count):
        x_coordinate = random.uniform(-10, 10)  # random x position between -10 - 10
        y_coordinate = gd.line(
            x_coordinate, coefficients
        )  # calculate correct y position from that

        # add offsets then append point to the list
        offset_x = random.uniform(-1.0, 1) * offset_range
        offset_y = random.uniform(-1.0, 1) * offset_range
        point = (x_coordinate + offset_x, y_coordinate + offset_y)
        points.append(point)
    return points


def train_test_split(points: list[tuple[float, float]], test_size: float = 0.3):
    """
    Split the points dataset up into a train test split set

    :param points: The points to split up
    :param test_size: How big the test size should be
    :return: 2 arrays ( train set, test set)
    """
    random.shuffle(points)
    split = int(len(points) * test_size)  # if array is 100 long this will be 30
    train = points[split:]
    test = points[:split]
    return train, test


def get_scatter_points(points: list[tuple[float, float]],
                       plotter: Any, color: str = "b") -> Any:
    """
    Plots a scatter graph of points

    :param points: points to plot
    :param plotter: reference to the matplotlib class in the script
    this gets called from (usually 'plt)
    :param color: Colour of the scatter points
    :return: The plotted graph (not very useful)
    """
    return plotter.scatter(
        gd.get_coordinates_x(points), gd.get_coordinates_y(points), c=color
    )


def draw_line(coefficients: list[float], plotter: Any, color: str = "r") -> Any:
    """
    Plots a line graph

    :param coefficients: The coefficients of curve to plot
    :param plotter: reference to the matplotlib class in the script this gets
     called from (usually 'plt)
    :param color: Colour of the line
    :return: The plotted graph (not very useful)
    """

    new_points = []
    ranges = [-10, 10]

    # create uniformly distributed points in range of -10,10
    for i in range(ranges[0], ranges[1]):
        x_coordinate = i
        y_coordinate = gd.line(x_coordinate, coefficients)
        point = (x_coordinate, y_coordinate)
        new_points.append(point)

    new_x_coordinates = [i[0] for i in new_points]
    new_y_coordinates = [i[1] for i in new_points]

    return plotter.plot(new_x_coordinates, new_y_coordinates, c=color)
