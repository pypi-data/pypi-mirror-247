from lamini.runners.base_runner import BaseRunner

DEFAULT_SYSTEM_PROMPT = "Always assist with care, respect, and truth. Respond with utmost utility yet securely. Avoid harmful, unethical, prejudiced, or negative content. Ensure replies promote fairness and positivity."


class MistralRunner(BaseRunner):
    def __init__(
        self,
        model_name="mistralai/Mistral-7B-Instruct-v0.1",
        system_prompt: str = None,
        prompt_template="<s>[INST] {system} {user} [/INST]",
        api_key=None,
        config={},
    ):
        super().__init__(
            config=config,
            system_prompt=system_prompt or DEFAULT_SYSTEM_PROMPT,
            model_name=model_name,
            prompt_template=prompt_template,
            api_key=api_key,
        )
