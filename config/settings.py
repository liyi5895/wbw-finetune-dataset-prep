import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Configuration
CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY')

# Rate Limiting Settings
CALLS = 60          # Maximum number of API calls
RATE_LIMIT = 60     # Time window in seconds (1 minute)

# Content Processing Settings
MAX_CHUNK_SIZE = 1024  # Maximum characters per chunk for content splitting

# Model Settings
MODEL_NAME = "claude-3-sonnet-20240620"
MAX_TOKENS_TO_SAMPLE = 1024 