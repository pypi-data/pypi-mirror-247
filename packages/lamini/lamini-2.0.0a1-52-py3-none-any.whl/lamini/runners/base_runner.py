import jsonlines
import pandas as pd
import os
from typing import List, Optional, Union
from lamini.api.lamini import Lamini


class BaseRunner:
    def __init__(
        self, model_name, system_prompt, prompt_template, api_key, url, config
    ):
        self.config = config
        self.model_name = model_name
        self.lamini_api = Lamini(
            model_name=model_name, api_key=api_key, url=url, config=self.config
        )
        self.prompt_template = prompt_template
        self.system_prompt = system_prompt
        self.data = []

    def call(
        self,
        prompt: Union[str, List[str]],
        system_prompt: Optional[str] = None,
        output_type: Optional[dict] = None,
        max_tokens: Optional[int] = None,
    ):
        input_objects = self.create_final_prompts(prompt, system_prompt)

        return self.lamini_api.generate(
            prompt=input_objects,
            model_name=self.model_name,
            max_tokens=max_tokens,
            output_type=output_type,
        )

    def create_final_prompts(self, prompt: Union[str, List[str]], system_prompt: str):
        if isinstance(prompt, str):
            return self.prompt_template.format(
                system=system_prompt or self.system_prompt, user=prompt
            )

        final_prompts = [
            self.prompt_template.format(
                system=system_prompt or self.system_prompt, user=p
            )
            for p in prompt
        ]

        return final_prompts

    def load_data(
        self,
        data,
        verbose: bool = False,
        user_key: str = "user",
        output_key: str = "output",
    ):
        """
        Load a list of dictionary objects with input-output keys into the LLM
        Each object must have 'user' and 'output' as keys.
        """

        # Get keys
        if not isinstance(data, list) and not isinstance(data[0], dict):
            raise ValueError(
                f"Data must be a list of dicts with keys user_key={user_key} and optionally output_key={output_key}. Or pass in different user_key and output_key"
            )
        try:
            input_output_objects = [
                {
                    "input": self.prompt_template.format(
                        system=self.system_prompt, user=d[user_key]
                    ),
                    "output": d[output_key] if output_key in d else "",
                }
                for d in data
            ]
        except KeyError:
            raise ValueError(
                f"Each object must have user_key={user_key}, and optionally output_key={output_key}, as keys"
            )
        self.data.extend(input_output_objects)
        if verbose:
            if len(input_output_objects) > 0:
                print("Sample added data: %s" % str(input_output_objects[0]))
            print("Loaded %d data pairs" % len(input_output_objects))
            print("Total data pairs: %d" % len(self.data))

    def load_data_from_jsonlines(
        self,
        file_path: str,
        verbose: bool = False,
        user_key: str = "user",
        output_key: str = "output",
    ):
        """
        Load a jsonlines file with input output keys into the LLM.
        Each line must be a json object with 'user' and 'output' as keys.
        """
        data = []
        with open(file_path) as dataset_file:
            reader = jsonlines.Reader(dataset_file)
            data = list(reader)
        self.load_data(data, verbose=verbose, user_key=user_key, output_key=output_key)

    def load_data_from_dataframe(
        self,
        df: pd.DataFrame,
        verbose: bool = False,
        user_key: str = "user",
        output_key: str = "output",
    ):
        """
        Load a pandas dataframe with input output keys into the LLM.
        Each row must have 'user' and 'output' as keys.
        """
        if user_key not in df.columns:
            raise ValueError(
                f"Dataframe must have user_key={user_key} as a column, and optionally output_key={output_key}"
            )
        input_output_objects = []
        try:
            for _, row in df.iterrows():
                input_output_objects.append(
                    [
                        {
                            "input": self.prompt_template.format(
                                system=self.system_prompt, user=row[user_key]
                            )
                        },
                        {"output": row[output_key] if output_key in row else ""},
                    ]
                )
        except KeyError:
            raise ValueError("Each object must have 'user' and 'output' as keys")
        self.data.extend(input_output_objects)

        if verbose:
            if len(input_output_objects) > 0:
                print("Sample added data: %s" % str(input_output_objects[0]))
            print("Loaded %d data pairs" % len(input_output_objects))
            print("Total data pairs: %d" % len(self.data))

    def load_data_from_csv(
        self,
        file_path: str,
        verbose: bool = False,
        user_key: str = "user",
        output_key: str = "output",
    ):
        """
        Load a csv file with input output keys into the LLM.
        Each row must have 'user' and 'output' as keys.
        The 'system' key is optional and will default to system prompt
        if passed during model initiation else to DEFAULT_SYSTEM_PROMPT.
        """
        df = pd.read_csv(file_path)
        self.load_data_from_dataframe(
            df, verbose=verbose, user_key=user_key, output_key=output_key
        )

    def upload_file(
        self,
        file_path,
        user_key: str = "user",
        output_key: str = "output",
    ):
        if os.path.getsize(file_path) > 1e7:
            raise Exception("File size is too large, please upload file less than 10MB")

        # Convert file records to appropriate format before uploading file
        items = []
        if file_path.endswith(".jsonl") or file_path.endswith(".jsonlines"):
            with open(file_path) as dataset_file:
                reader = jsonlines.Reader(dataset_file)
                data = list(reader)

                for row in data:
                    item = [
                        [
                            {
                                "input": self.prompt_template.format(
                                    system=self.system_prompt, user=row[user_key]
                                )
                            },
                            {"output": row[output_key] if output_key in row else ""},
                        ]
                    ]
                    items.append(item)

        elif file_path.endswith(".csv"):
            df = pd.read_csv(file_path).fillna("")
            data_keys = df.columns
            if user_key not in data_keys:
                raise ValueError(
                    f"File must have user_key={user_key} as a column (and optionally output_key={output_key}). You "
                    "can pass in different user_key and output_keys."
                )

            try:
                for _, row in df.iterrows():
                    item = [
                        [
                            {
                                "input": self.prompt_template.format(
                                    system=self.system_prompt, user=row[user_key]
                                )
                            },
                            {"output": row[output_key] if output_key in row else ""},
                        ]
                    ]
                    items.append(item)
            except KeyError:
                raise ValueError("Each object must have 'input' and 'output' as keys")

        else:
            raise Exception(
                "Upload of only csv and jsonlines file supported at the moment."
            )

        self.lamini_api.upload_data(items)

    def clear_data(self):
        """Clear the data from the LLM"""
        self.data = []

    def train(
        self,
        limit=500,
        is_public=False,
        **kwargs,
    ):
        """
        Train the LLM on added data. This function blocks until training is complete.
        """
        if len(self.data) < 2 and not self.lamini_api.upload_file_path:
            raise Exception("Submit at least 2 data pairs to train to allow validation")
        if limit is None:
            data = self.data
        elif len(self.data) > limit:
            data = self.data[:limit]
        else:
            data = self.data

        if self.lamini_api.upload_file_path:
            final_status = self.lamini_api.train_and_wait(
                is_public=is_public,
                **kwargs,
            )
        else:
            final_status = self.lamini_api.train_and_wait(
                data,
                is_public=is_public,
                **kwargs,
            )
        try:
            self.model_name = final_status["model_name"]
            self.job_id = final_status["job_id"]
        except KeyError:
            raise Exception("Training failed")

    def evaluate(self) -> List:
        """Get evaluation results"""
        if self.job_id is None:
            raise Exception("Must train before getting results (no job id))")
        self.evaluation = self.lamini_api.evaluate()
        return self.evaluation

    def get_eval_results(self) -> List:
        return self.evaluate()
