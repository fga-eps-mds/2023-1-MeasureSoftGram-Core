import numpy as np

import core.measures_functions as ems_functions
import core.transformations as transformations
from util.check import Checker


def non_complex_files_density(
    data_frame,
    min_threshold: float = 0,
    max_threshold: float = 10,
):
    """
    Calculates non-complex files density.
    This function calculates non-complex files density measure
    used to assess the changeability quality subcharacteristic.

    This function gets the dataframe metrics
    and returns the non-complex files density measure.
    """
    files_complexity = np.array(data_frame["complexity"])
    files_functions = np.array(data_frame["functions"])

    Checker.check_metric_values(files_complexity, "complexity")
    Checker.check_metric_values(files_functions, "functions")

    if len(files_complexity) == len(files_functions) == 0:
        return 0.0

    Checker.check_threshold(
        min_threshold,
        max_threshold,
        "non_complex_files_density",
    )

    (
        complex_files_density,
        number_of_files,
    ) = ems_functions.get_non_complex_files_density(
        data={
            "complexity": files_complexity,
            "functions": files_functions,
        }
    )

    files_in_thresholds_bool_index = complex_files_density <= max_threshold
    files_functions_gt_zero_bool_index = files_functions > 0
    x = complex_files_density[files_in_thresholds_bool_index * files_functions_gt_zero_bool_index]

    interpretation_function_value = transformations.interpretation_function(
        x=x,
        min_threshold=min_threshold,
        max_threshold=max_threshold,
        gain_interpretation=-1,
    )

    aggregated_and_normalized_measure = transformations.calculate_measure(
        interpretation_function_value, number_of_files
    )
    return aggregated_and_normalized_measure


def commented_files_density(data_frame, min_threshold: float = 10, max_threshold: float = 30):
    """
    Calculates commented files density.

    This function gets the dataframe metrics
    and returns the commented files density measure.
    """
    files_comment_lines_density = data_frame["comment_lines_density"]

    Checker.check_metric_values(files_comment_lines_density, "comment_lines_density")

    if len(files_comment_lines_density) == 0:
        return 0.0

    Checker.check_threshold(min_threshold, max_threshold, "comment_files_density")

    (
        files_comment_lines_density,
        number_of_files,
    ) = ems_functions.get_commented_files_density(
        data={
            "comment_lines_density": files_comment_lines_density,
        }
    )

    x = files_comment_lines_density[
        files_comment_lines_density.between(
            min_threshold,
            max_threshold,
            inclusive="both",
        )
    ]
    interpretation_function_value = transformations.interpretation_function(
        x=x,
        min_threshold=min_threshold,
        max_threshold=max_threshold,
        gain_interpretation=-1,
    )
    aggregated_and_normalized_measure = transformations.calculate_measure(
        interpretation_function_value, number_of_files
    )
    return aggregated_and_normalized_measure


def absence_of_duplications(data_frame, min_threshold: float = 0, max_threshold: float = 5.0):
    """
    Calculates duplicated files absence (em3).

    This function gets the dataframe metrics
    and returns the duplicated files absence measure (em3).
    """
    files_duplicated_lines_density = data_frame["duplicated_lines_density"]  # m5 metric

    Checker.check_metric_values(files_duplicated_lines_density, "duplicated_lines_density")

    if len(files_duplicated_lines_density) == 0:
        return 0.0

    Checker.check_threshold(min_threshold, max_threshold, "absence_of_duplications")

    (
        files_duplicated_lines_density,
        number_of_files,
    ) = ems_functions.get_absence_of_duplications(
        data={"duplicated_lines_density": files_duplicated_lines_density},
    )

    x = files_duplicated_lines_density[files_duplicated_lines_density <= max_threshold]

    interpretation_function_value = transformations.interpretation_function(
        x=x,
        min_threshold=min_threshold,
        max_threshold=max_threshold,
        gain_interpretation=-1,
    )
    aggregated_and_normalized_measure = transformations.calculate_measure(
        interpretation_function_value, number_of_files
    )
    return aggregated_and_normalized_measure


def test_coverage(
    data_frame,
    min_threshold: float = 60,
    max_threshold: float = 100,
):
    """
    Calculates test coverage (em6).

    This function gets the dataframe metrics
    and returns the test coverage measure (em6).
    """
    coverage = data_frame["coverage"]  # m6 metric

    Checker.check_metric_values(coverage, "coverage")

    if len(coverage) == 0:
        return 0.0

    Checker.check_threshold(min_threshold, max_threshold, "test_coverage")

    coverage, number_of_files = ems_functions.get_test_coverage(
        data={"coverage": coverage},
    )
    x = coverage[coverage >= min_threshold]
    interpretation_function_value = transformations.interpretation_function(
        x=x,
        min_threshold=min_threshold,
        max_threshold=max_threshold,
        gain_interpretation=1,
    )
    aggregated_and_normalized_measure = transformations.calculate_measure(
        interpretation_function_value, number_of_files
    )
    return aggregated_and_normalized_measure


def fast_test_builds(data_frame, min_threshold: float = 0, max_threshold: float = 300000):
    """
    Calculates fast test builds (em5)
    This function gets the dataframe metrics
    and returns the fast test builds measure (em5).
    """
    test_execution_time = data_frame["test_execution_time"]
    tests = data_frame["tests"]

    Checker.check_metric_values(test_execution_time, "test_execution_time")
    Checker.check_metric_values(tests, "tests")

    if len(test_execution_time) == len(tests) == 0:
        return 0.0

    Checker.check_threshold(min_threshold, max_threshold, "fast_test_builds")

    (
        execution_time,
        number_of_files,
        number_of_tests,
    ) = ems_functions.get_fast_test_builds(
        data={"test_execution_time": test_execution_time, "tests": tests},
    )

    execution_between_thresholds = execution_time[execution_time <= max_threshold]
    x = np.divide(execution_between_thresholds, number_of_tests)

    interpretation_function_value = transformations.interpretation_function(
        x=x,
        min_threshold=min_threshold,
        max_threshold=max_threshold,
        gain_interpretation=-1,
    )

    aggregated_and_normalized_measure = transformations.calculate_measure(
        interpretation_function_value, number_of_files
    )

    return aggregated_and_normalized_measure


def passed_tests(data_frame, min_threshold: float = 0, max_threshold: float = 1):
    """
    Calculates passed tests (em4)

    This function gets the dataframe metrics
    and returns the passed tests measure (em4).
    """

    tests = data_frame["tests"]  # m6 metrics
    test_errors = data_frame["test_errors"]  # m7 metrics
    test_failures = data_frame["test_failures"]  # m8 metrics

    Checker.check_metric_values(tests, "tests")
    if len(tests) == 0:
        return 0.0
    Checker.check_metric_value(test_failures, "test_failures")
    Checker.check_metric_value(test_errors, "test_errors")

    Checker.check_threshold(min_threshold, max_threshold, "passed_tests")

    number_of_tests, number_of_fail_tests = ems_functions.get_passed_tests(
        data={
            "tests": tests,
            "test_errors": float(test_errors),
            "test_failures": float(test_failures),
        }
    )

    x = np.divide((number_of_tests - number_of_fail_tests), number_of_tests)

    interpretation_function_value = transformations.interpretation_function(
        x=x,
        min_threshold=min_threshold,
        max_threshold=max_threshold,
        gain_interpretation=1,
    )

    aggregated_and_normalized_measure = transformations.calculate_measure(interpretation_function_value)

    return aggregated_and_normalized_measure
