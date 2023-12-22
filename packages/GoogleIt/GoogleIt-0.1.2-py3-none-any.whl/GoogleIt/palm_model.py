import google.generativeai as palm
import textwrap


class Palm2Model:
    """
    Wrapper class for interacting with the Google Palm 2 language model.

    Attributes:
    - model: The initialized Palm 2 language model.
    """

    def __init__(self) -> None:
        """Initialize the Palm2Model instance."""
        self.model = None

    def init(self, api_key: str) -> None:
        """
        Initialize the Palm 2 language model using the provided API key.

        Parameters:
        - api_key (str): The API key for authentication.
        """
        palm.configure(api_key=api_key)
        models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]

        if not models:
            raise ValueError("No models with text generation support found.")

        self.model = models[0]

    def make_prompt(self, query: str, relevant_passage: str) -> str:
        """
        Generate a prompt for the Palm 2 language model.

        Parameters:
        - query (str): The user's question.
        - relevant_passage (str): The relevant passage for context.

        Returns:
        str: The formatted prompt for the language model.
        """
        escaped = relevant_passage.replace("'", "").replace('"', "").replace("\n", " ")
        prompt = textwrap.dedent(f"""You are a helpful and informative bot that answers questions using text from the reference passage included below. \
            Be sure to respond in a complete sentence, being comprehensive, including all relevant background information. \
            However, you are talking to a non-technical audience, so be sure to break down complicated concepts and \
            strike a friendly and conversational tone. \
            The length of the response should be relevant to the prompt. Provide longer responses only if asked
            If the passage is irrelevant to the answer, you may ignore it.
            QUESTION: '{query}'
            PASSAGE: '{escaped}'

            ANSWER:
            """)

        return prompt

    def query(self, document: str, question: str) -> str:
        """
        Query the Palm 2 language model for an answer.

        Parameters:
        - document (str): The reference document for context.
        - question (str): The user's question.

        Returns:
        str: The generated answer from the language model.
        """
        if self.model is None:
            raise ValueError("The language model is not initialized. Call init() with the API key first.")

        prompt = self.make_prompt(question, document)

        temperature = 0.2
        answer = palm.generate_text(prompt=prompt,
                                    model=self.model,
                                    candidate_count=3,
                                    temperature=temperature,
                                    max_output_tokens=1000)

        return answer.candidates[0]['output']
    
if __name__ == "__main__":
    # palm2 = Palm2Model()
    # palm2.init("AIzaSyAXCVMFirOACW80v3w4lNEruWBAskWbeiw")

    # print(palm2.query("Suresh is a boy", "Who is suresh?"))

    import PIL.Image

    img = PIL.Image.open('download.png')
    img

    palm.configure(api_key="AIzaSyAXCVMFirOACW80v3w4lNEruWBAskWbeiw")

    model = palm.GenerativeModel('gemini-pro')

    response = model.generate_content("I will provide you a dataset. Can you build a model using the data for prediction? Can i just ask for the model accuracy and prediction to you or i need to train the model separately by myself")
    # response.resolve()

    print(response.text)