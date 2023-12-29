from flask import Flask, request, jsonify
from EffectGenerator import GPT  # Import your GPT class from your script

app = Flask(__name__)
gpt = GPT()

@app.route('/engineer_prompt', methods=['POST'])
def engineer_prompt():
    data = request.json
    query = data['query']
    response = gpt.engineerPrompt(query)
    return jsonify(response)

if __name__ == '__main__':
    app.run()
