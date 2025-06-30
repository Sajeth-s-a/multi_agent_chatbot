from anthropic import Anthropic
from config.settings import settings

class ClaudeClient:
    """
    A utility class to interact with the Anthropic Claude API.
    """
    def __init__(self):
        # Initialize the Anthropic client with the API key loaded from settings
        self.client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.default_model = "claude-3-opus-20240229" # Or 'claude-3-sonnet-20240229', 'claude-3-haiku-20240307'

    async def get_completion(self, user_message: str, system_message: str = None, model: str = None) -> str:
        """
        Sends a message to the Claude LLM and returns its completion.

        Args:
            user_message (str): The user's input message.
            system_message (str, optional): An optional system message to guide the LLM's persona/behavior.
            model (str, optional): The Claude model to use. Defaults to self.default_model.

        Returns:
            str: The LLM's generated response.
        """
        messages = [{"role": "user", "content": user_message}]
        if system_message:
            messages.insert(0, {"role": "system", "content": system_message})

        if not model:
            model = self.default_model

        try:
            response = await self.client.messages.create(
                model=model,
                max_tokens=1024,
                messages=messages
            )
            return response.content[0].text
        except Exception as e:
            print(f"Error calling Claude API: {e}")
            return f"An error occurred while processing your request: {e}"

# Create a singleton instance for easy import
claude_client = ClaudeClient()