from flask import Flask, request, jsonify
from EffectGenerator import EffectGeneratorAssistant  # Import your GPT class from your script

app = Flask(__name__)
gpt = EffectGeneratorAssistant()

@app.route('/create-conversation', methods=['POST'])
def create_conversation():
    thread_id = gpt.create_conversation()
    print(thread_id)
    return jsonify(thread_id)

@app.route('/get-params', methods=['POST'])
def get_params():
    print("get-params")
    print(request.data.decode('utf-8'))
    data = request.json
    try:
        thread_id = data['thread_id']
        print(thread_id)
        query = data['query']
        current_state = data['current_state']
    except: 
        return jsonify({'error': 'Invalid request'})
    
    new_query = f"Current State: {current_state}\n\n Query:{query}"
    
    print('starting generator')
    messages, run_parameters = gpt.run_generator(new_query, thread_id)

    # messages = [f"Current State: {current_state}\n\n Query:{query}", "Response 1", "Response 2", "Response 3"]

    # run_parameters = {'effects': [{'type': 'highShelfFilter', 'cutOffFrequency': 8000, 'gainFactor': 0.7, 'Q': 1.41}, {'type': 'lowShelfFilter', 'cutOffFrequency': 500, 'gainFactor': 0.7, 'Q': 1.41}, {'type': 'reverb', 'roomSize': 0.8, 'damping': 0.7, 'wetLevel': 0.6, 'width': 1}]}
    response = {'messages': messages, 'run_parameters': run_parameters}
    print(response)
    return jsonify(response)

@app.route('/delete-conversation', methods=['POST'])
def delete_conversation():
    data = request.json
    try:
        thread_id = data['thread_id']
    except: 
        return jsonify({'error': 'Invalid request'})
    
    gpt.delete_thread(thread_id)
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run()
