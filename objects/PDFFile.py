import base64
import io
import json
import os
from typing import Optional, Tuple
from nodes.NodeEnum import NodeEnum
from nodes.Paragraph import Paragraph
from nodes.Table import Table
from nodes.Image import Image as Img
from nodes.Node import Node
import fitz
import openai
from PIL import Image
from google import genai
from google.genai import types

from objects.PageRouter import PageRouterParameters
from objects.filters.ContentTypeFilter import ContentTypeFilter
from objects.filters.CustomFilter import CustomFilter
from objects.filters.KeywordFilter import KeywordFilter
from objects.filters.PageNumberFilter import PageNumberFilter
from objects.filters.PageOrientationFilter import PageOrientationFilter


def encode_image_to_base64(image: bytes):
    return base64.b64encode(image).decode("utf-8")


class PDFFile:
    def __init__(self, filepath: str):
        self.document = fitz.open(filepath)
        self.filepath = filepath

    def get_nodes(self) -> list[NodeEnum]:
        client = genai.Client(api_key=os.environ['GEMINI_API_KEY'])

        # TODO edit this prompt
        prompt = (
            f"Return all the content in the following pdf file."
            "Return a JSON object containing all the information in the pdf file."
        )

        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=[types.Part.from_bytes(
                data=self.document.write(),
                mime_type='application/pdf',
            ), prompt],
            config=types.GenerateContentConfig(
                temperature=0.0,
                candidate_count=1,
                response_mime_type='application/json',
            )
        )

        return response.text

    def filter_by_page_number(self, f: PageNumberFilter):
        pages_to_filter = set(f.pages)
        include = f.include
        total_pages = self.document.page_count

        if include:
            selected_pages = [p for p in range(
                total_pages) if p in pages_to_filter]
        else:
            selected_pages = [p for p in range(
                total_pages) if p not in pages_to_filter]

        if not selected_pages:
            self.document = None
            return

        self.document.select(selected_pages)

    def filter_by_page_orientation(self, f: PageOrientationFilter):
        include = f.include
        target_orientation = f.orientation.lower()
        selected_pages = []

        for page_num in range(self.document.page_count):
            page = self.document[page_num]
            rect = page.rect

            page_orientation = "landscape" if rect.width > rect.height else "portrait"

            if (include and page_orientation == target_orientation) or (not include and page_orientation != target_orientation):
                selected_pages.append(page_num)

        if not selected_pages:
            self.document = None
            return

        self.document.select(selected_pages)

    def filter_by_keywords(self, f: KeywordFilter):
        client = genai.Client(api_key=os.environ['GEMINI_API_KEY'])
        keywords = f.keywords
        include = f.include
        selected_pages = []
        total_pages = self.document.page_count

        for page_num in range(total_pages):
            page = self.document[page_num]
            new_doc = fitz.open()
            new_doc.insert_pdf(self.document, from_page=page_num,
                               to_page=page_num)

            # TODO edit this prompt
            prompt = (
                f"Does the following text contain any of these keywords: {keywords}? "
                "Answer only in JSON format with a key 'contains' having the value true or false.\n\n"
            )

            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=[types.Part.from_bytes(
                    data=new_doc.write(),
                    mime_type='application/pdf',
                ), prompt],
                config=types.GenerateContentConfig(
                    temperature=0.0,
                    candidate_count=1,
                    response_mime_type='application/json',
                    response_schema={
                        'type': 'object',
                        'properties': {
                            'contains': {
                                'type': 'boolean',
                                'description': "Either true or false"
                            }
                        },
                        'required': ['contains']
                    }
                )
            )

            try:
                print(response.text)
                json_response = json.loads(response.text)
                contains = json_response.get("contains", "")
            except json.JSONDecodeError:
                contains = False

            if (include and contains) or (not include and not contains):
                selected_pages.append(page_num)

        self.document.select(selected_pages)

    def filter_by_content_type(self, f: ContentTypeFilter):
        client = genai.Client(api_key=os.environ['GEMINI_API_KEY'])
        keywords = f.content_types
        include = f.include
        selected_pages = []
        total_pages = self.document.page_count

        for page_num in range(total_pages):
            page = self.document[page_num]
            new_doc = fitz.open()
            new_doc.insert_pdf(self.document, from_page=page_num,
                               to_page=page_num)

            # TODO edit this prompt
            prompt = (
                f"Does the following text contain any of these media types: {keywords}? "
                "Answer only in JSON array having table, image, text or hyperlink.\n\n"
            )

            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=[types.Part.from_bytes(
                    data=new_doc.write(),
                    mime_type='application/pdf',
                ), prompt],
                config=types.GenerateContentConfig(
                    temperature=0.0,
                    candidate_count=1,
                    response_mime_type='application/json',
                    response_schema={
                        "type": "array",
                        "items": {
                            "type": "string",
                            "description": "Either table, image, text or hyperlink"
                        }
                    }
                )
            )

            try:
                print(response.text)
                json_response = json.loads(response.text)
                contains = set(json_response)
            except json.JSONDecodeError:
                contains = set()

            config = set(f.content_types)
            if (include and contains.intersection(config)) or (not include and not contains.intersection(config)):
                selected_pages.append(page_num)

        self.document.select(selected_pages)

    def filter_by_custom_requirement(self, f: CustomFilter):
        client = genai.Client(api_key=os.environ['GEMINI_API_KEY'])
        query = f.query
        include = f.include
        selected_pages = []
        total_pages = self.document.page_count

        for page_num in range(total_pages):
            page = self.document[page_num]
            new_doc = fitz.open()
            new_doc.insert_pdf(self.document, from_page=page_num,
                               to_page=page_num)

            # TODO edit this prompt
            prompt = (
                f"Is the following text relevant to the this query: {query}? "
                "Answer only in JSON format with a key 'contains' having the value true or false.\\n\n"
            )

            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=[types.Part.from_bytes(
                    data=new_doc.write(),
                    mime_type='application/pdf',
                ), prompt],
                config=types.GenerateContentConfig(
                    temperature=0.0,
                    candidate_count=1,
                    response_mime_type='application/json',
                    response_schema={
                        'type': 'object',
                        'properties': {
                            'contains': {
                                'type': 'boolean',
                                'description': "Either true or false"
                            }
                        },
                        'required': ['contains']
                    }
                )
            )

            try:
                print(response.text)
                json_response = json.loads(response.text)
                contains = json_response.get("contains", "")
            except json.JSONDecodeError:
                contains = False

            if (include and contains) or (not include and not contains):
                selected_pages.append(page_num)

        self.document.select(selected_pages)
