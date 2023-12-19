from lamini.runners.base_runner import BaseRunner

DEFAULT_SYSTEM_PROMPT = """\
You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe.  Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.

If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information."""


class LlamaV2Runner(BaseRunner):
    """A class for running and training a Llama V2 model, using system and user prompts"""

    def __init__(
        self,
        model_name: str = "meta-llama/Llama-2-7b-chat-hf",
        system_prompt: str = None,
        prompt_template="<s>[INST] <<SYS>>\n{system}\n<</SYS>>\n{user} [/INST]",
        api_key=None,
        url=None,
        config={},
    ):
        super().__init__(
            config=config,
            system_prompt=system_prompt or DEFAULT_SYSTEM_PROMPT,
            model_name=model_name,
            prompt_template=prompt_template,
            api_key=api_key,
            url=url,
        )
