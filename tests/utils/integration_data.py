from tests.test_helpers import read_json

PRE_CONFIGURATION = {
    "_id": "6265b525ab15bc00c4effbd0",
    "name": "pre-config-test-analysis",
    "characteristics": {
        "reliability": {
            "expected_value": 70,
            "weight": 50,
            "subcharacteristics": ["testing_status"],
            "weights": {"testing_status": 100},
        },
        "maintainability": {
            "expected_value": 30,
            "weight": 50,
            "subcharacteristics": ["modifiability"],
            "weights": {"modifiability": 100},
        },
    },
    "subcharacteristics": {
        "testing_status": {
            "weights": {"passed_tests": 100},
            "measures": ["passed_tests"],
        },
        "modifiability": {
            "weights": {"non_complex_file_density": 100},
            "measures": ["non_complex_file_density"],
        },
    },
    "measures": ["passed_tests", "non_complex_file_density"],
}

JSON_FILE = read_json(
    "tests/unit/data/fga-eps-mds-2021-2-MeasureSoftGram-Service-04-12-2022-17-32-35-v1.1.0.json"
)

COMPONENT = {
    "pre_config_id": "6265b525ab15bc00c4effbd0",
    "components": JSON_FILE["components"],
    "language_extension": "py",
}

TEST_PARAMETERS = [
    (
        200,
        "characteristics",
        {
            "maintainability": 0.6000000000000001,
            "reliability": 0.7142857142857143,
        },
    ),
    (
        200,
        "subcharacteristics",
        {
            "modifiability": 0.6000000000000001,
            "testing_status": 0.7142857142857143,
        },
    ),
    (
        200,
        "sqc",
        {"sqc": 0.6596226503208683},
    ),
]


CALCULATE_SUBCHARACTERISTICS_DATA = [
    (
        # Calculate one subcharacteristic
        {
            "subcharacteristics": [
                {
                    "key": "testing_status",
                    "measures": [
                        {
                            "key": "passed_tests",
                            "value": 1.0,
                            "weight": 33
                        },
                        {
                            "key": "test_builds",
                            "value": 0.00178,
                            "weight": 33
                        },
                        {
                            "key": "test_coverage",
                            "value": 0.25,
                            "weight": 34
                        }
                    ]
                }
            ]
        },
        200,
        {
            "subcharacteristics": [
                {
                    "key": "testing_status",
                    "value": 0.5901748671720202
                }
            ]
        }
    ),
    (
        # Calculate multiples subcharacteristics
        {
            "subcharacteristics": [
                {
                    "key": "modifiability",
                    "measures": [
                        {
                            "key": "non_complex_file_density",
                            "value": 0.675,
                            "weight": 70
                        },
                        {
                            "key": "commented_file_density",
                            "value": 0.2275,
                            "weight": 30
                        }
                    ]
                },
                {
                    "key": "testing_status",
                    "measures": [
                        {
                            "key": "test_builds",
                            "value": 0.00178,
                            "weight": 100
                        }
                    ]
                }
            ]
        },
        200,
        {
            "subcharacteristics": [
                {
                    "key": "modifiability",
                    "value": 0.6268617959382247
                },
                {
                    "key": "testing_status",
                    "value": 0.00178
                }
            ]
        }
    ),
    (
        # Invalid request data
        {
            "subcharacteristics": [
                {
                    "key": "testing_status",
                    "value": 0.5
                }
            ]
        },
        422,
        {
            "error": "Failed to validate request",
            "schema_errors": {
                "subcharacteristics": {
                    "0": {
                        "measures": [
                            "Missing data for required field."
                        ],
                        "value": [
                            "Unknown field."
                        ]
                    }
                }
            }
        }
    ),
]
