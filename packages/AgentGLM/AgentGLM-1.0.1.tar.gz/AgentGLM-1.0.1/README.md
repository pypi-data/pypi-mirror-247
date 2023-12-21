A library encapsulating an inference engine based on a large language model, supporting both Chinese and English.

For command interpretation:

def intent_chat(self, prompt, symbol=False)
For information retrieval and general conversation:

def model_chat(self, prompt, history=[], max_length=1024, top_p=0.7, temperature=0.1)
These functions handle command interpretation (intent_chat) and facilitate information retrieval and general conversation (model_chat). The library supports both Chinese and English languages.
