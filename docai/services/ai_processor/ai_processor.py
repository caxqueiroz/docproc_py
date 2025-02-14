from openai import OpenAI
from ...config.settings import settings

class AIProcessor:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def enhance_extraction(self, original_text: str, file_type: str) -> str:
        prompt = f"""
        Please analyze and enhance the following extracted text from a {file_type} file.
        If there are any obvious OCR errors or unclear sections, please correct them.
        Maintain the original structure but improve clarity and readability.
        
        Original text:
        {original_text}
        """

        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a document text extraction enhancement assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1500
        )

        return response.choices[0].message.content.strip()
