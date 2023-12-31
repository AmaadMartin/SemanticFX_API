import os
# set OPENAI_API_KEY to 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
os.environ['OPENAI_API_KEY'] = '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'

from openai import OpenAI
import json

class GPT:
    def __init__(self):
        self.client = OpenAI()
        self.PromptEngineer = self.client.beta.assistants.create(
            name="Effect Generator",
            instructions="Given a description of a vst effect you are tasked with creating it by combining several low level effects out of the following:                 - filter                 - reverb                 - compressor                -delayLine                 - phaser                 - chorus                 You have functions to add each of these effects.                 The order of effects is dependent on the order you add them in. You don't have to use every effect and you could use effects multiple times. Your encouraged to make unique and high quality effects. You shouldn't expect any response from the user. ",
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
        self.thread = self.client.beta.threads.create()
        self.parameters = {
            "effects": []
        }

    def engineerPrompt(self, query):
        thread = self.client.beta.threads.create()
        threadId = thread.id

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
        print(run)
        
        # retrieve status of run
        while run.status == "queued" or run.status == "in_progress" or run.status == "requires_action":
            run = self.client.beta.threads.runs.retrieve(
                thread_id=threadId,
                run_id=run.id
            )
            print(run.status)
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
                                self.parameters["effects"].append({
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
                                self.parameters["effects"].append({
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
                                self.parameters["effects"].append({
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
                                self.parameters["effects"].append({
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
                                self.parameters["effects"].append({
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
                                self.parameters["effects"].append({
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
                                self.parameters["effects"].append({
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
                                self.parameters["effects"].append({
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

        print(self.client.beta.threads.messages.list(threadId))
        self.client.beta.threads.delete(threadId)
    
    def reset(self):
        self.parameters = {
            "effects": []
        }




                                                            