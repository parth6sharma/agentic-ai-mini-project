import os

from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI

if load_dotenv("./.env"):
    print("Environment variables loaded from .env file")


model = AzureChatOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT") or os.getenv("AZURE_AI_ENDPOINT"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION")
    or os.getenv("AZURE_AI_API_VERSION"),
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    or os.getenv("AZURE_AI_MODEL_NAME"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY") or os.getenv("AZURE_AI_API_KEY"),
    streaming=True,
    verbose=True,
)
