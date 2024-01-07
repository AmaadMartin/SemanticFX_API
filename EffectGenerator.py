import os
# set OPENAI_API_KEY to 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
# os.environ['OPENAI_API_KEY'] = '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'
os.environ['OPENAI_API_KEY'] = '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'

from openai import OpenAI
import json

prompt_instructions = """
You are an expert audio engineer who will serve as a personalized assistant to other audio engineers and producers. They will communicate with you using normal vernacular common with producers, or they will be explicit. Most of their requests and queries will consist of editing equalization, dynamics, and effects for different stems. You are tasked with creating it by combining several low level effects out of the following: 
- filter
- reverb
- compressor
- delayLine
- phaser
- chorus

You will have functions to tweak specific parameters pertaining to each effect , similar to how you would in a traditional plugin in a DAW. The order of effects is dependent on the order you add them in. 

You don't have to use every effect and could use multiple effects multiple times. You are encouraged to make high quality effects. It is your decision on how many and which effects to apply, and the parameters you choose.

Here are some things to keep in mind.
- Reverb sounds much better when an EQ is applied before. Usually, when reverb is needed, apply EQ, then add Reverb. This is because otherwise, it elongates frequencies that weren't cut off. Usually, a good baseline for EQ before reverb is to put a high pass filter on 500hz to make it sound thin/bright, and put a low pass filter on 8khz to make it sound dark/gloomy. 
- For delay, you would put an EQ, then apply effects as necessary, however for the EQ, you choose what you want to pass.
- For chorus, you decide whether or not you want to apply EQ, then you apply Chorus, but something important to understand is the Haas method, where you keep the rate very low around .1hz. 
- For bass you usually only want to hear it in the middle frequencies. 
- Compression is often used for drums, especially kicks.
- People tend to put reverb on snares and high hats

Here are some examples of inputs and what a producer would expect to happen. The format will be {input}: {producer expectations}:
- Make my vocals sound brighter or have more clarity: have a high shelf boost, and compress highs if necessary
- My vocals sound thin, make them more full: Boost low mid on an EQ. 120hz for male and 240hz for female
- Make my vocals have more presence: Boost mid on EQ 2k-4k hz
- I want my vocals to sound spacier: Apply Reverb/delay/chorus
- The bass sounds muddy, make it less muddy: Dip the low mid on an EQ around 150-300hz
- I need more bass there isn't enough bass: Low shelf boost around 50-100hz
- I need more rumble there isn't enough rumble: Low shelf boost behind fundamental (behind hump of frequencies) Most likely 40hz and below.
- I want it to hit harder I want more punch: Compress it / add an EQ boost between 100-200hz. 
- I want the bass to be warmer: compress it, add overdrive (subtle), add an EQ boost between 125-250hz
- I want the bass to feel wider: send it to a bus with chorus on it and an EQ (side setting) with a high pass filter till about 160.
- I want the melody to sound warmer: add overdrive (subtle) add EQ boost between 125-250hz
- I want the melody to sound darker: low pass filter (depends on how dark you want it)
- I want the melody to sound spacier: Apply reverb/delay/chorus
- I want the melody to sound wider: Apply Chorus
- I want the drums to hit harder/punch: Punchy compression subtle overdrive
- I want the drums to be controlled better: Gluey compression
- I want my drums to sound more full: parallel compression
- I want my drums to sound like they are in a room/cathedral/church/{place}:  Reverb
- Make my drums sound less harsh: high shelf cut around 6.3k with an EQ, OR a D-esser with shelf setting around 6.3k should give them the choice
- I want the mix sound warmer: add an EQ boost between 125-250hz, +3 gain max, wide notch
- I want my mix to sound more controlled: gluey compression
- I want my mix to have more life: gluey compression on mix, stereo analyzer (subtle)
- Make my mix sound wider/bigger/full: stereo analyzer (subtle), add EQ boost between 250-500hz, +3 gain max, wide notch.
- Make my mix brighter/more clarity: Add EQ boost between 5k-10k hz, +3 gain max, wide notch. 
- I can't hear instrument X in my mix: find what frequencies x occupies, see which stems/tracks occupies the same frequencies (instrument y), put a wide EQ dip on Y where the frequencies clash, put x's volume a little up as well.
- I can't hear my kick, make it stand out: Dip on the fundamental (50-60hz) on the bass track with a Dynamic EQ. 
- Make my vocals sit better on the mix: Dip on the 6.3k-10k range on the melody and drum track with a Dynamic EQ, cut it lower on the melody track then the drum. 

For each query, for the stem in question, you will be given the current effects applied to the stem, and the current state of their parameters. You will then make a decision on which effects to apply to the stem and change the parameters accordingly. Make sure you think step by step about your answer and review it to ensure a high quality answer. Make sure to explain what you have done to the user so they can understand your answer.
"""

class EffectGeneratorAssistant:
    def __init__(self):
        self.client = OpenAI()
        self.PromptEngineer = self.client.beta.assistants.create(
            name="Effect Generator v1",
            instructions=prompt_instructions,
            tools=[{"type": "code_interpreter"}, {
            "type": "function",
                "function": {
                    "name": "addPeakFilter",
                    "description": "Adds a filter with coefficients for a peak filter centred around a given frequency, with a variable Q and gain. The gain is a scale factor that the centre frequencies are multiplied by, so values greater than 1.0 will boost the centre frequencies, values less than 1.0 will attenuate them.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "centreFrequency": { "type": "number",
                                            "description": "The centreFrequency of the filter"},
                            "gainFactor": { "type": "number",
                                            "description": "The gain of the filter"},
                            "Q": { "type": "number",
                                            "description": "The Q of the filter"},
                        },
                        "required": ["frequency", "gain", "Q"]
                    }
                }
            }, {
            "type": "function",
                "function": {
                    "name": "addLowShelfFilter",
                    "description": "Adds a filter with coefficients for a low-pass shelf filter with variable Q and gain. The gain is a scale factor that the low frequencies are multiplied by, so values greater than 1.0 will boost the low frequencies, values less than 1.0 will attenuate them",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "cutOffFrequency": { "type": "number",
                                            "description": "The cutOffFrequency of the filter"},
                            "gainFactor": { "type": "number",
                                            "description": "The gain of the filter"},
                            "Q": { "type": "number",
                                            "description": "The Q of the filter"},
                        },
                        "required": ["frequency", "gain", "Q"]
                    }
                }
            }, {
            "type": "function",
                "function": {
                    "name": "addHighShelfFilter",
                    "description": "Adds a filter with coefficients for a high-pass shelf filter with variable Q and gain. The gain is a scale factor that the high frequencies are multiplied by, so values greater than 1.0 will boost the high frequencies, values less than 1.0 will attenuate them.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "cutOffFrequency": { "type": "number",
                                            "description": "The cutOffFrequency of the filter"},
                            "gainFactor": { "type": "number",
                                            "description": "The gain of the filter"},
                            "Q": { "type": "number",
                                            "description": "The Q of the filter"},
                        },
                        "required": ["frequency", "gain", "Q"]
                    }
                }
            }, {
            "type": "function",
                "function": {
                    "name": "addReverb",
                    "description": "Adds a reverb with the given parameters",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "roomSize": { "type": "number",
                                            "description": "The room size of the reverb"},
                            "damping": { "type": "number",
                                            "description": "The damping of the reverb"},
                            "wetLevel": { "type": "number",
                                            "description": "The wet level of the chorus ranges from 0-1"},
                            "width": { "type": "number",
                                            "description": "The width of the reverb"},
                        },
                        "required": ["roomSize", "damping", "wetLevel", "width"]
                    }
                }
            }, {
            "type": "function",
                "function": {
                    "name": "addCompressor",
                    "description": "Adds a compressor with the given parameters",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "threshold": { "type": "number",
                                            "description": "the threshold in dB of the compressor"},
                            "ratio": { "type": "number",
                                            "description": "the ratio of the compressor (must be higher or equal to 1)"},
                            "attack": { "type": "number",
                                            "description": "the attack time in milliseconds of the compressor"},
                            "release": { "type": "number",
                                            "description": "the release time in milliseconds of the compressor"},
                        },
                        "required": ["threshold", "ratio", "attack", "release"]
                    }
                }
            }, {
            "type": "function",
                "function": {
                    "name": "addDelayLine",
                    "description": "Adds a delay line with the given parameters",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "delay": { "type": "number",
                                            "description": "the delay in samples"},
                            "maximumDelayInSamples": { "type": "number",
                                            "description": "maximum delay in samples"},
                        },
                        "required": ["delay", "maximumDelayInSamples"]
                    }
                }
            }, {
            "type": "function",
                "function": {
                    "name": "addPhaser",
                    "description": "Adds a phaser with the given parameters",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "rate": { "type": "number",
                                            "description": "the rate (in Hz) of the LFO modulating the phaser all-pass filters"},
                            "depth": { "type": "number",    
                                            "description": "the volume (between 0 and 1) of the LFO modulating the phaser all-pass filters"},
                            "centreFrequency": { "type": "number",
                                            "description": "the centre frequency (in Hz) of the phaser all-pass filters modulation"},
                            "feedback": { "type": "number",
                                            "description": "the feedback volume (between -1 and 1) of the phaser"},
                            "mix": { "type": "number",
                                            "description": "the amount of dry and wet signal in the output of the phaser (between 0 for full dry and 1 for full wet)"},
                        },
                        "required": ["rate", "depth", "centerFrequency", "feedback", "mix"]
                    }
                }
            }, {
            "type": "function",
                "function": {
                    "name": "addChorus",
                    "description": "Adds a chorus with the given parameters",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "rate": { "type": "number",
                                            "description": "the rate (in Hz) of the LFO modulating the chorus delay line"},
                            "depth": { "type": "number",    
                                            "description": "the volume of the LFO modulating the chorus delay line (between 0 and 1)"},
                            "centreDelay": { "type": "number",
                                            "description": "the centre delay in milliseconds of the chorus delay line modulation"},
                            "feedback": { "type": "number",
                                            "description": "the feedback volume (between -1 and 1) of the chorus delay line"},
                            "mix": { "type": "number",
                                            "description": "the amount of dry and wet signal in the output of the chorus (between 0 for full dry and 1 for full wet)"},
                        },
                        "required": ["rate", "depth", "centreDelay", "feedback", "mix"]
                    }
                }
            }],
            model="gpt-4"
        )

    def create_conversation(self):
        thread = self.client.beta.threads.create()
        threadId = thread.id
        return threadId

    def run_generator(self, query, threadId):
        # create message with effect description
        message = self.client.beta.threads.messages.create(
            thread_id=threadId,
            content=query,
            role="user",
        )

        # create run for assistant
        run = self.client.beta.threads.runs.create(
            thread_id= threadId,
            assistant_id=self.PromptEngineer.id
        )

        run_parameters = {
            "effects": []
        }


        
        # retrieve status of run
        while run.status == "queued" or run.status == "in_progress" or run.status == "requires_action":
            run = self.client.beta.threads.runs.retrieve(
                thread_id=threadId,
                run_id=run.id
            )
            if run.status == "requires_action" and run.required_action.type == "submit_tool_outputs":
                toolCalls = run.required_action.submit_tool_outputs.tool_calls
                toolOutputs = []
                print(toolCalls)

                for toolCall in toolCalls:
                    try:
                        if toolCall.function.name == "addPeakFilter":
                            if toolCall.function.arguments:
                                args = json.loads(toolCall.function.arguments)
                                print(args)
                                run_parameters["effects"].append({
                                    "type": "peakFilter",
                                    "centreFrequency": args["centreFrequency"],
                                    "gainFactor": args["gainFactor"],
                                    "Q": args["Q"]
                                })
                                toolOutputs.append({
                                    "tool_call_id": toolCall.id,
                                    "output": "success"
                                })
                            else:
                                toolOutputs.append({
                                    "tool_call_id": toolCall.id,
                                    "output": "no arguments provided"
                                })
                        elif toolCall.function.name == "addLowShelfFilter":
                            if toolCall.function.arguments:
                                args = json.loads(toolCall.function.arguments)
                                print(args)
                                run_parameters["effects"].append({
                                    "type": "lowShelfFilter",
                                    "cutOffFrequency": args["cutOffFrequency"],
                                    "gainFactor": args["gainFactor"],
                                    "Q": args["Q"]
                                })
                                toolOutputs.append({
                                    "tool_call_id": toolCall.id,
                                    "output": "success"
                                })
                            else:
                                toolOutputs.append({
                                    "tool_call_id": toolCall.id,
                                    "output": "no arguments provided"
                                })
                        elif toolCall.function.name == "addHighShelfFilter":
                            if toolCall.function.arguments:
                                args = json.loads(toolCall.function.arguments)
                                print(args)
                                run_parameters["effects"].append({
                                    "type": "highShelfFilter",
                                    "cutOffFrequency": args["cutOffFrequency"],
                                    "gainFactor": args["gainFactor"],
                                    "Q": args["Q"]
                                })
                                toolOutputs.append({
                                    "tool_call_id": toolCall.id,
                                    "output": "success"
                                })
                            else:
                                toolOutputs.append({
                                    "tool_call_id": toolCall.id,
                                    "output": "no arguments provided"
                                })
                        elif toolCall.function.name == "addReverb":
                            if toolCall.function.arguments:
                                args = json.loads(toolCall.function.arguments)
                                print(args)
                                run_parameters["effects"].append({
                                    "type": "reverb",
                                    "roomSize": args["roomSize"],
                                    "damping": args["damping"],
                                    "wetLevel": args["wetLevel"],
                                    "width": args["width"]
                                })
                                toolOutputs.append({
                                    "tool_call_id": toolCall.id,
                                    "output": "success"
                                })
                            else:
                                toolOutputs.append({
                                    "tool_call_id": toolCall.id,
                                    "output": "no arguments provided"
                                })
                        elif toolCall.function.name == "addCompressor":
                            if toolCall.function.arguments:
                                args = json.loads(toolCall.function.arguments)
                                print(args)
                                run_parameters["effects"].append({
                                    "type": "compressor",
                                    "threshold": args["threshold"],
                                    "ratio": args["ratio"],
                                    "attack": args["attack"],
                                    "release": args["release"]
                                })
                                toolOutputs.append({
                                    "tool_call_id": toolCall.id,
                                    "output": "success"
                                })
                            else:
                                toolOutputs.append({
                                    "tool_call_id": toolCall.id,
                                    "output": "no arguments provided"
                                })
                        elif toolCall.function.name == "addDelayLine":
                            if toolCall.function.arguments:
                                args = json.loads(toolCall.function.arguments)
                                print(args)
                                run_parameters["effects"].append({
                                    "type": "delayLine",
                                    "delay": args["delay"],
                                    "maximumDelayInSamples": args["maximumDelayInSamples"]
                                })
                                toolOutputs.append({
                                    "tool_call_id": toolCall.id,
                                    "output": "success"
                                })
                            else:
                                toolOutputs.append({
                                    "tool_call_id": toolCall.id,
                                    "output": "no arguments provided"
                                })
                        elif toolCall.function.name == "addPhaser":
                            if toolCall.function.arguments:
                                args = json.loads(toolCall.function.arguments)
                                print(args)
                                run_parameters["effects"].append({
                                    "type": "phaser",
                                    "rate": args["rate"],
                                    "depth": args["depth"],
                                    "centreFrequency": args["centreFrequency"],
                                    "feedback": args["feedback"],
                                    "mix": args["mix"]
                                })
                                toolOutputs.append({
                                    "tool_call_id": toolCall.id,
                                    "output": "success"
                                })
                            else:
                                toolOutputs.append({
                                    "tool_call_id": toolCall.id,
                                    "output": "no arguments provided"
                                })
                        elif toolCall.function.name == "addChorus":
                            if toolCall.function.arguments:
                                args = json.loads(toolCall.function.arguments)
                                print(args)
                                run_parameters["effects"].append({
                                    "type": "chorus",
                                    "rate": args["rate"],
                                    "depth": args["depth"],
                                    "centreDelay": args["centreDelay"],
                                    "feedback": args["feedback"],
                                    "mix": args["mix"]
                                })
                                toolOutputs.append({
                                    "tool_call_id": toolCall.id,
                                    "output": "success"
                                })
                            else:
                                toolOutputs.append({
                                    "tool_call_id": toolCall.id,
                                    "output": "no arguments provided"
                                })
                    except Exception as e:
                        toolOutputs.append({
                            "tool_call_id": toolCall.id,
                            "output": str(e)
                        })

                run = self.client.beta.threads.runs.submit_tool_outputs(
                    thread_id= threadId,
                    run_id= run.id,
                    tool_outputs= toolOutputs
                )
        
        messages = self.client.beta.threads.messages.list(
            thread_id=threadId,
            order="asc"
        )
        
        messages = list(map(lambda x: {"role": x.role, "value": x.content[0].text.value}, messages.data))
        for message in messages:
            if message["role"] == "user":
                message["value"] = message["value"].split("Query:")[1]

        return messages, run_parameters
        
    def delete_thread(self, threadId):
        self.client.beta.threads.delete(threadId)

                                                            