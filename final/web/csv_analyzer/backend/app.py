import os
import pandas as pd
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS

UPLOAD_FOLDER = '/app/uploads'
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)

def allowed_file(filename):
    """Checks if the file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handles file uploads."""
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return jsonify({"message": "File uploaded successfully", "filename": filename}), 200
    else:
        return jsonify({"error": "Invalid file type. Only CSV is allowed."}), 400

@app.route('/analyze', methods=['GET'])
def analyze_file():
    filename = request.args.get('file')
    if not filename:
        return jsonify({"error": "Missing 'file' parameter"}), 400

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    try:
        df = pd.read_csv(file_path, on_bad_lines='skip')
        num_rows = len(df)

        query_string = "Query could not be generated."
        query_result = "Could not perform dynamic query. Check column data or names."
        query_result_count = 0

        if not df.empty:
            unique_counts = df.nunique()
            query_column = unique_counts.idxmax()
            
            if df[query_column].dtype == 'object':
                query_value = df[query_column].mode()[0]
                query_string = f"`{query_column}` == '{query_value}'"
            else:
                query_value = df[query_column].mean()
                query_string = f"`{query_column}` > {query_value}"

            try:
                query_result_df = df.query(query_string)
                query_result = query_result_df.head().to_json(orient='split')
                query_result_count = len(query_result_df)
            except Exception:
                pass
            
        analysis = {
            "columns": df.columns.tolist(),
            "shape": list(df.shape),
            "data_types": df.dtypes.astype(str).to_dict(),
            "descriptive_stats": df.describe(include='all').to_json(),
            "null_values_per_column": df.isna().sum().to_dict(),
            "head": df.head().to_json(orient='split'),
            "tail": df.tail().to_json(orient='split'),
            "sample": df.sample(n=min(5, num_rows)).to_json(orient='split'),
            "dynamic_query_info": {
                "query_string": query_string,
                "result_count": query_result_count
            },
            "dynamic_query_result": query_result
        }
        return jsonify(analysis)

    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    except Exception as e:
        return jsonify({"error": f"Failed to analyze file: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)