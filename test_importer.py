import requests

BASE_URL = "http://localhost:5001"


def test_define():
    print("\n--- Testing /define ---")

    request_body = {
        "words": ["apple", "river", "unknownword"]
    }

    response = requests.post(
        f"{BASE_URL}/define",
        json=request_body
    )

    print("Status code:", response.status_code)
    print("Response:", response.json())


def test_parse_csv():
    print("\n--- Testing /parse-csv ---")

    with open("sample.csv", "rb") as csv_file:
        response = requests.post(
            f"{BASE_URL}/parse-csv",
            files={"file": csv_file}
        )

    print("Status code:", response.status_code)
    print("Response:", response.json())


def test_invalid_csv_request():
    print("\n--- Testing invalid CSV request ---")

    response = requests.post(
        f"{BASE_URL}/parse-csv"
    )

    print("Status code:", response.status_code)
    print("Response:", response.json())


def test_define_no_matches():
    print("\n--- Testing /define with no matches ---")

    request_body = {
        "words": ["unknownword", "anotherunknownword"]
    }

    response = requests.post(
        f"{BASE_URL}/define",
        json=request_body
    )

    print("Status code:", response.status_code)
    print("Response:", response.json())


if __name__ == "__main__":
    test_define()
    test_define_no_matches()
    test_parse_csv()
    test_invalid_csv_request()