from flask import Flask, request, jsonify
import csv
import io

app = Flask(__name__)

DEFINITIONS = {
    "apple": "A round fruit that grows on an apple tree.",
    "river": "A natural stream of water flowing toward another body of water.",
    "architecture": "The art or practice of designing and constructing buildings.",
    "computer": "An electronic device that processes and stores data.",
    "fragrance": "A pleasant or distinctive smell."
}


def lookup_definition(word):
    return DEFINITIONS.get(word.lower())


def parse_csv_file(file):
    file_text = file.read().decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(file_text))

    if not reader.fieldnames:
        raise ValueError("CSV file must contain a header row.")

    return list(reader)


@app.route("/define", methods=["POST"])
def define_words():
    request_data = request.get_json(silent=True)

    if not request_data or not isinstance(request_data.get("words"), list):
        return jsonify({
            "status": "error",
            "data": [],
            "errors": ["Request must contain a 'words' list."]
        }), 400

    words = request_data["words"]

    print("Received /define request:", words)

    data = []
    errors = []

    for word in words:
        if not isinstance(word, str):
            errors.append({
                "word": str(word),
                "error": "Word must be a string."
            })
            continue

        definition = lookup_definition(word)

        if definition:
            data.append({
                "word": word,
                "definition": definition
            })
        else:
            errors.append({
                "word": word,
                "error": "Definition not found."
            })

    if data and not errors:
        status = "success"
    elif data and errors:
        status = "partial_success"
    else:
        status = "error"

    response = {
        "status": status,
        "data": data,
        "errors": errors
    }

    print("Sending response:", response)

    return jsonify(response), 200


@app.route("/parse-csv", methods=["POST"])
def parse_csv():
    if "file" not in request.files:
        return jsonify({
            "status": "error",
            "data": [],
            "errors": ["No CSV file was provided."]
        }), 400

    uploaded_file = request.files["file"]

    if uploaded_file.filename == "":
        return jsonify({
            "status": "error",
            "data": [],
            "errors": ["No CSV file was selected."]
        }), 400

    print("Received /parse-csv request:", uploaded_file.filename)

    try:
        records = parse_csv_file(uploaded_file)

        response = {
            "status": "success",
            "data": records,
            "errors": []
        }

        print("Sending response:", response)

        return jsonify(response), 200

    except (UnicodeDecodeError, csv.Error, ValueError) as error:
        return jsonify({
            "status": "error",
            "data": [],
            "errors": [str(error)]
        }), 400


if __name__ == "__main__":
    app.run(port=5001)