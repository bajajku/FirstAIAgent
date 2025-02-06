from langchain_huggingface import HuggingFaceEndpoint

class LLM:

    def __init__(self, repo_id: str, api_token: str, **kwargs):
        """
        Initialize the Hugging Face API client with custom parameters.
        
        Args:
            repo_id (str): The Hugging Face model repository ID.
            api_token (str): The Hugging Face Hub API token.
            **kwargs: Additional parameters for Hugging Face configuration.
        """
        self.repo_id = repo_id
        self.api_token = api_token
        self.config = {
            'max_new_tokens': kwargs.get('max_new_tokens', 512),
            'top_k': kwargs.get('top_k', 10),
            'top_p': kwargs.get('top_p', 0.95),
            'typical_p': kwargs.get('typical_p', 0.95),
            'temperature': kwargs.get('temperature', 0.2),
            'repetition_penalty': kwargs.get('repetition_penalty', 1.03),
            'streaming': kwargs.get('streaming', True)
        }
        self.client = self.create_llm()

    def create_llm(self):
        """Set up the Hugging Face API endpoint."""
        return HuggingFaceEndpoint(
            **self.config,
            repo_id=self.repo_id,
            huggingfacehub_api_token=self.api_token
        )