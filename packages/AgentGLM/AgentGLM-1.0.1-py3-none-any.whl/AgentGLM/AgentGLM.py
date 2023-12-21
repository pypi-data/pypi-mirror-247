from transformers import AutoTokenizer, AutoModel
import uvicorn
import torch

# CLASSIFIER
PROMPT_CLASSIFIER_HEAD_1 = "意图集合:{"
PROMPT_CLASSIFIER_HEAD_2 = "}\n理解用户问题意图后进行回复，回复选项在提供的意图集合内选择，最后输出对应意图:\n"
# GET ALL
PROMPT_GET = "提取{}:\n"
# CHAT
PROMPT_CHAT = "\n\n注意: 回复长度必须小于512个TOKEN"
PROMPT_SPC = "不好意思，不太理解你在说的内容"


class AgentGLM:
    model = None
    tokenizer = None

    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer

    def model_chat(self, prompt, history=[], max_length=1024, top_p=0.7, temperature=0.1):
        if '#' in prompt:
            head, body = prompt.split("#")
            prompt = PROMPT_GET.format(head) + body

        response, history = self.model.chat(self.tokenizer, prompt, history=history, max_length=max_length, top_p=top_p, temperature=temperature)
        return response, history

    def intent_chat(self, prompt="拨打电话，打开应用，问答聊天", symbol=False):
        head, body = prompt.split("#")
        classifier_head = PROMPT_CLASSIFIER_HEAD_1 + head + PROMPT_CLASSIFIER_HEAD_2
        result = classifier_head + body
        response, history = self.model.chat(self.tokenizer, result, history=[], max_length=1024, top_p=0.7, temperature=0.1)
        return response
