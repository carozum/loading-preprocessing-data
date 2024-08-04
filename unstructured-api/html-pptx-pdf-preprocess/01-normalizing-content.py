import sys
import os
from Utils import Utils
from unstructured.staging.base import dict_to_elements, elements_to_json
from unstructured.partition.pptx import partition_pptx
from unstructured.partition.html import partition_html
from unstructured_client.models.errors import SDKError
from unstructured_client.models import shared
from unstructured_client import UnstructuredClient
from IPython.display import JSON
from IPython.display import Image
import warnings
import json


# Warning control
warnings.filterwarnings('ignore')

# Détermine le répertoire du script actuel
script_dir = os.path.dirname(os.path.abspath(__file__))


# Unstructured client
utils = Utils()

DLAI_API_KEY = utils.get_dlai_api_key()
DLAI_API_URL = utils.get_dlai_url()

s = UnstructuredClient(
    api_key_auth=DLAI_API_KEY,
    server_url=DLAI_API_URL,
)
print(s)

##########################################################
# Example Document: Medium Blog HTML Page¶

Image(
    filename=os.path.join(script_dir, 'images', 'HTML_demo.png'),
    height=600,
    width=600)

filename = os.path.join(script_dir, "example_files", "medium_blog.html")
elements = partition_html(filename=filename)

element_dict = [el.to_dict() for el in elements]
example_output = json.dumps(element_dict[11:15], indent=2)
print(example_output)

#########################################################
# Example Doc: MSFT PowerPoint on OpenAI

Image(
    filename=os.path.join(script_dir, "images", "pptx_slide.png"),
    height=600,
    width=600)
