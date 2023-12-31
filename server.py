from flask import Flask, request, jsonify
from EffectGenerator import GPT  # Import your GPT class from your script

app = Flask(__name__)
gpt = GPT()

@app.route('/get-params', methods=['POST'])
def engineer_prompt():
    data = request.json
    query = data['query']    
    gpt.engineerPrompt(query)

    response = gpt.parameters
    gpt.reset()
    # parameters = {'effects': [{'type': 'delayLine', 'delay': 50, 'maximumDelayInSamples': 8000}, {'type': 'phaser', 'rate': 0.8, 'depth': 0.6, 'centreFrequency': 440, 'feedback': -0.5, 'mix': 1}, {'type': 'compressor', 'threshold': -18, 'ratio': 4, 'attack': 50, 'release': 200}, {'type': 'peakFilter', 'centreFrequency': 3000, 'gainFactor': 1.5, 'Q': 1.0}, {'type': 'chorus', 'rate': 1, 'depth': 0.3, 'centreDelay': 15, 'feedback': 0.2, 'mix': 0.5}, {'type': 'highShelfFilter', 'cutOffFrequency': 5000, 'gainFactor': 0.75, 'Q': 0.7}]}
    return jsonify(response)

if __name__ == '__main__':
    app.run()
