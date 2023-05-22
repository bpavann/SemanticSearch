import io
import fitz
import json
import openai
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from flask_cors import CORS
from flask import Flask, jsonify, request

app = Flask(__name__)
CORS(app)

cred = credentials.Certificate("sdkKey.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": 'https://semantics-2c7d5-default-rtdb.firebaseio.com'
})

@app.route("/", methods=["POST"])  # Changed the route to /analyze and the method to POST
def analyze():
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file selected.'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected.'})

    # Read the PDF file into memory
    pdf_file = io.BytesIO(file.read())

    # Process the PDF file and get the search result
    with fitz.open(pdf_file) as doc:
        abstract_data = {}
        
        metadata = doc.metadata
        title = metadata.get("title", "")
        author = metadata.get("author", "")
        producer=metadata.get("producer","")

        for page in doc:
            text = page.get_text()
            lines = text.split("\n")
            for i, line in enumerate(lines):
                if line.lower().startswith("abstract"):
                    j = i + 1
                    abstract = ""
                    while j < len(lines) and not lines[j].lower().startswith(("keywords", "introduction")):
                        abstract += lines[j] + " "
                        j += 1
                    abstract_data[page.number] = abstract
                    break
 
        # Save the result to Firebase Realtime Database
        ref = db.reference("/users/Papers")
        ref.push(
            {
                "Title": title,
                "Author": author,
                "Producer": producer,
                "Abstract": abstract
            }
        )

    openai.api_key = "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" 
    prompt = f"Retrieve the links of research papers related to the following abstract in all www.researchgate.net/search/publication and pubmed.ncbi.nlm.nih.gov website:\n\n{abstract}"
    model_engine = "text-davinci-003" 
    response = openai.Completion.create(
         engine=model_engine,
         prompt=prompt,
         temperature=0.7,
         max_tokens=2048,
         n=1,
         stop=None,
    )
    papers_data = response.choices[0].text.strip()
    print("The following links are similar Research papers which are relevant to the given PDF\n", papers_data)
    
    return json.dumps({"result": papers_data})


if __name__ == "__main__":
    app.run(debug=True)
