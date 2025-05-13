
#!/usr/bin/env python
import os
import sys
from dotenv import load_dotenv
from os.path import join, dirname

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

AZURE_OPENAI_API_KEY=os.environ.get("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_API_VERSION=os.environ.get("AZURE_OPENAI_API_VERSION") 
AZURE_OPENAI_ENDPOINT=os.environ.get("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT_NAME=os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME")

# SSMP Configuration
SSMP_URL= os.environ.get("SSMP_URL")