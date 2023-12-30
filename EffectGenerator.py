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
            instructions="You are the Effect Parameter Finder. Given a description of a vst effect you are tasked with creating it. \
            You have 6 low level effects: \
                0. EQEffect eqEffect (A data structure holds a list of eq peaks filters that could be added to with the addEQBand function) \
                1. juce::dsp::Reverb reverb (A juce dsp reverb with parameters that could be set with setReverbParameters) \
                2. juce::dsp::Compressor<float> compressor (A juce dsp compressor with parameters that could be set with setCompressorParameters) \
                3. juce::dsp::DelayLine<float, juce::dsp::DelayLineInterpolationTypes::Linear> delayLine (A juce dsp delay line with parameters that could be set with setDelayLineParameters) \
                4. juce::dsp::Phaser<float> phaser (A juce dsp phaser with parameters that could be set with setPhaserParameters) \
                5. juce::dsp::Chorus<float> chorus (A juce dsp chorus with parameters that could be set with setChorusParameters) \
                The order of effects is the order you set them in.\
                You should create the effect with the given parameters. You shouldn't expect any response from the user. \
                Make sure to think step by step to get the closest to the desired effect. \
                Start by describing the effect in greater detail to get fully understand it. \
                In addition, describe the thought process before each step. \
                Once you set all of the parameters give a description of what was done. ",
            tools=[{"type": "code_interpreter"}, {
            "type": "function",
                "function": {
                    "name": "addEQBand",
                    "description": "Adds an EQ peak according to the given frequency and gain",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "frequency": { "type": "number",
                                            "description": "The frequency of the peak filter"},
                            "gain": { "type": "number",
                                            "description": "The gain of the peak filter"},
                        },
                        "required": ["frequency", "gain"]
                    }
                }
            }, {
            "type": "function",
                "function": {
                    "name": "setReverbParameters",
                    "description": "Sets the parameters of the reverb",
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
                    "name": "setCompressorParameters",
                    "description": "Sets the parameters of the compressor",
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
                    "name": "setDelayLineParameters",
                    "description": "Sets the parameters of the delay line",
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
                    "name": "setPhaserParameters",
                    "description": "Sets the parameters of the phaser",
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
                    "name": "setChorusParameters",
                    "description": "Sets the parameters of the chorus",
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
            "eqEffect": [],
            "reverb": {
                "roomSize": 0,
                "damping": 0,
                "wetLevel": 0,
                "width": 0
            },
            "compressor": {
                "threshold": 0,
                "ratio": 0,
                "attack": 0,
                "release": 0
            },
            "delayLine": {
                "delay": 0,
                "maximumDelayInSamples": 0,
            },
            "phaser": {
                "rate": 0,
                "depth": 0,
                "centerFrequency": 0,
                "feedback": 0,
                "mix": 0
            },
            "chorus": {
                "rate": 0,
                "depth": 0,
                "centreDelay": 0,
                "feedback": 0,
                "mix": 0
            },
            "order": [0, 1, 2, 3, 4, 5],
            "numEffects": 0
        }
        self.numEffects = 0
        self.orderDict = {}

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
                    if toolCall.function.name == "addEQBand":
                        if toolCall.function.arguments:
                            if 0 not in self.orderDict:
                                self.orderDict[0] = self.numEffects
                                self.numEffects += 1
                            args = json.loads(toolCall.function.arguments)
                            print(args)
                            self.parameters["eqEffect"].append(args)
                            toolOutputs.append({
                                "tool_call_id": toolCall.id,
                                "output": "success"
                            })
                        else:
                            toolOutputs.append({
                                "tool_call_id": toolCall.id,
                                "output": "no arguments provided"
                            })
                    elif toolCall.function.name == "setReverbParameters":
                        if toolCall.function.arguments:
                            self.orderDict[1] = self.numEffects
                            self.numEffects += 1
                            args = json.loads(toolCall.function.arguments)
                            print(args)
                            self.parameters["reverb"] = args
                            toolOutputs.append({
                                "tool_call_id": toolCall.id,
                                "output": "success"
                            })
                        else:
                            toolOutputs.append({
                                "tool_call_id": toolCall.id,
                                "output": "no arguments provided"
                            })
                    elif toolCall.function.name == "setCompressorParameters":
                        if toolCall.function.arguments:
                            self.orderDict[2] = self.numEffects
                            self.numEffects += 1
                            args = json.loads(toolCall.function.arguments)
                            print(args)
                            self.parameters["compressor"] = args
                            toolOutputs.append({
                                "tool_call_id": toolCall.id,
                                "output": "success"
                            })
                        else:
                            toolOutputs.append({
                                "tool_call_id": toolCall.id,
                                "output": "no arguments provided"
                            })
                    elif toolCall.function.name == "setDelayLineParameters":
                        if toolCall.function.arguments:
                            self.orderDict[3] = self.numEffects
                            self.numEffects += 1
                            args = json.loads(toolCall.function.arguments)
                            print(args)
                            self.parameters["delayLine"] = args
                            toolOutputs.append({
                                "tool_call_id": toolCall.id,
                                "output": "success"
                            })
                        else:
                            toolOutputs.append({
                                "tool_call_id": toolCall.id,
                                "output": "no arguments provided"
                            })
                    elif toolCall.function.name == "setPhaserParameters":
                        if toolCall.function.arguments:
                            self.orderDict[4] = self.numEffects
                            self.numEffects += 1
                            args = json.loads(toolCall.function.arguments)
                            print(args)
                            self.parameters["phaser"] = args
                            toolOutputs.append({
                                "tool_call_id": toolCall.id,
                                "output": "success"
                            })
                        else:
                            toolOutputs.append({
                                "tool_call_id": toolCall.id,
                                "output": "no arguments provided"
                            })
                    elif toolCall.function.name == "setChorusParameters":
                        if toolCall.function.arguments:
                            self.orderDict[5] = self.numEffects
                            self.numEffects += 1
                            args = json.loads(toolCall.function.arguments)
                            print(args)
                            self.parameters["chorus"] = args
                            toolOutputs.append({
                                "tool_call_id": toolCall.id,
                                "output": "success"
                            })
                        else:
                            toolOutputs.append({
                                "tool_call_id": toolCall.id,
                                "output": "no arguments provided"
                            })

                run = self.client.beta.threads.runs.submit_tool_outputs(
                    thread_id= threadId,
                    run_id= run.id,
                    tool_outputs= toolOutputs
                )

        print(self.orderDict)

        newOrder = [0] * 6
        print(newOrder)
        for i in range(6):
            if i in self.orderDict:
                newOrder[self.orderDict[i]] = i

        self.parameters["order"] = newOrder
        self.parameters["numEffects"] = self.numEffects
        self.numEffects = 0
        self.orderDict = {}

        print(self.client.beta.threads.messages.list(threadId))
        self.client.beta.threads.delete(threadId)
    




                                                            