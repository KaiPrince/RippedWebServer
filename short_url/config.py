"""
* Project Name: Short_Url
* File Name: config.py
* Programmer: Kai Prince
* Date: Mon, Mar 1, 2021
* Description: This file contains configuration settings.
"""
import os
from dotenv import load_dotenv

load_dotenv()

mongo_url = os.environ.get("MONGO_URL")
