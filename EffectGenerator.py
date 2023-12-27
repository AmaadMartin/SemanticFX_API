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
                In addition you have the abiity to set the order of the effects with the setOrder function. \
                And you could set the number of effects with the setNumEffects function which will cause only the first [NumEffects] effects to be used from the order. \
                You should create the effect with the given parameters. You shouldn't expect any response from the user. Once you set all of the parameters give a description of what was done. Make sure to think step by step to get the closest to the desired effect.",
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
                        "required": ["roomSize", "damping", "wetLevel", "dryLevel"]
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
                                            "description": "The threshold of the compressor"},
                            "ratio": { "type": "number",
                                            "description": "The ratio of the compressor"},
                            "attack": { "type": "number",
                                            "description": "The attack of the compressor"},
                            "release": { "type": "number",
                                            "description": "The release of the compressor"},
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
                                            "description": "The delay of the delay line"},
                            "setMaximumDelayInSamples": { "type": "number",
                                            "description": "The maximum delay of the delay line"},
                        },
                        "required": ["delay", "setMaximumDelayInSamples"]
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
                                            "description": "The rate of the phaser"},
                            "depth": { "type": "number",    
                                            "description": "The depth of the phaser"},
                            "centreFrequency": { "type": "number",
                                            "description": "The centre frequency of the phaser"},
                            "feedback": { "type": "number",
                                            "description": "The feedback of the phaser"},
                            "mix": { "type": "number",
                                            "description": "The mix of the phaser"},
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
                                            "description": "The rate of the phaser"},
                            "depth": { "type": "number",    
                                            "description": "The depth of the phaser"},
                            "centreFrequency": { "type": "number",
                                            "description": "The centre frequency of the phaser"},
                            "feedback": { "type": "number",
                                            "description": "The feedback of the phaser"},
                            "mix": { "type": "number",
                                            "description": "The mix of the phaser"},
                        },
                        "required": ["rate", "depth", "centerFrequency", "feedback", "mix"]
                    }
                }
            }, {
            "type": "function",
                "function": {
                    "name": "setOrder",
                    "description": "Sets the order of the effects",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "order": {
                                "type": "array",
                                "items": {
                                    "type": "integer"
                                }}
                        }
                    }

                }
            }, {
            "type": "function",
                "function": {
                    "name": "setNumEffects",
                    "description": "Sets the number of effects",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "numEffects": {"type": "integer"}
                        }
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
                "wetLevel": 0
            },
            "compressor": {
                "threshold": 0,
                "ratio": 0,
                "attack": 0,
                "release": 0
            },
            "delayLine": {
                "delay": 0,
                "feedback": 0,
                "wetLevel": 0
            },
            "phaser": {
                "frequency": 0,
                "depth": 0,
                "feedback": 0,
                "wetLevel": 0
            },
            "chorus": {
                "frequency": 0,
                "depth": 0,
                "feedback": 0,
                "wetLevel": 0
            },
            "order": [0, 1, 2, 3, 4, 5],
            "numEffects": 6
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
                    if toolCall.function.name == "addEQBand":
                        args = json.loads(toolCall.function.arguments)
                        print(args)
                        self.parameters["eqEffect"].append(args)
                        toolOutputs.append({
                            "tool_call_id": toolCall.id,
                            "output": "success"
                        })
                    elif toolCall.function.name == "setReverbParameters":
                        args = json.loads(toolCall.function.arguments)
                        print(args)
                        self.parameters["reverb"] = args
                        toolOutputs.append({
                            "tool_call_id": toolCall.id,
                            "output": "success"
                        })
                    elif toolCall.function.name == "setCompressorParameters":
                        args = json.loads(toolCall.function.arguments)
                        print(args)
                        self.parameters["compressor"] = args
                        toolOutputs.append({
                            "tool_call_id": toolCall.id,
                            "output": "success"
                        })
                    elif toolCall.function.name == "setDelayLineParameters":
                        args = json.loads(toolCall.function.arguments)
                        print(args)
                        self.parameters["delayLine"] = args
                        toolOutputs.append({
                            "tool_call_id": toolCall.id,
                            "output": "success"
                        })
                    elif toolCall.function.name == "setPhaserParameters":
                        args = json.loads(toolCall.function.arguments)
                        print(args)
                        self.parameters["phaser"] = args
                        toolOutputs.append({
                            "tool_call_id": toolCall.id,
                            "output": "success"
                        })
                    elif toolCall.function.name == "setChorusParameters":
                        args = json.loads(toolCall.function.arguments)
                        print(args)
                        self.parameters["chorus"] = args
                        toolOutputs.append({
                            "tool_call_id": toolCall.id,
                            "output": "success"
                        })
                    elif toolCall.function.name == "setOrder":
                        args = json.loads(toolCall.function.arguments)
                        print(args)
                        self.parameters["order"] = args["order"]
                        toolOutputs.append({
                            "tool_call_id": toolCall.id,
                            "output": "success"
                        })
                    elif toolCall.function.name == "setNumEffects":
                        args = json.loads(toolCall.function.arguments)
                        print(args)
                        self.parameters["numEffects"] = args["numEffects"]
                        toolOutputs.append({
                            "tool_call_id": toolCall.id,
                            "output": "success"
                        })

                run = self.client.beta.threads.runs.submit_tool_outputs(
                    thread_id= threadId,
                    run_id= run.id,
                    tool_outputs= toolOutputs
                )

        print(self.client.beta.threads.messages.list(threadId))
        self.client.beta.threads.delete(threadId)
    




                                                            