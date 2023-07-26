# iDum - Intelligent Document Understanding Machine

## Introduction:
iDUM (Intelligent Document Understanding Machine) is an innovative solution that leverages FastAPI, PaddleOCR, and OpenAI to automatically extract key-value information from documents posted via the API endpoint. This blog will explore the functionality and architecture of iDUM, which provides a JSON output with extracted information in a structured and easily accessible format.

## Understanding iDUM:
FastAPI - A Powerful Framework for Web APIs: iDUM utilizes FastAPI, a modern, fast, and web framework for building APIs with Python. FastAPI's high-performance capabilities and intuitive design make it an ideal choice for processing incoming requests and returning responses efficiently.

PaddleOCR - Advanced Optical Character Recognition: PaddleOCR is an advanced OCR model that is capable of recognizing text from both structured and unstructured documents. In iDUM, PaddleOCR plays a crucial role in extracting textual information from uploaded PDFs.

OpenAI - Conversational AI for Text Generation: OpenAI's powerful language model, GPT-3.5, is employed in iDUM to engage in a conversation with users and understand their queries regarding the extracted information. The model's ability to generate human-like responses makes the interaction more natural and user-friendly.

Information Extraction and Formatting: When a PDF document is uploaded via the API, iDUM utilizes PaddleOCR to extract text from each page of the document. The extracted text is then processed and formatted into a JSON structure. The information is organized into key-value pairs for easy retrieval and analysis.

ChatPromptTemplate - Structured Conversation with OpenAI: iDUM uses ChatPromptTemplate to structure conversations with the OpenAI model. The template contains predefined prompts that guide the conversation, ensuring that the extracted information is accurately understood and processed.

Key Information to Extract: iDUM focuses on extracting essential information from the document, such as invoice number, invoice date, invoice title, GSTIN (Goods and Services Tax Identification Number), item details, total amount, GST amount, grand total, ship-to details, and bill-to details.

JSON Output with Camel Casing: The extracted information is converted into a JSON output with camel casing for the keys. Camel casing enhances readability and ensures consistency in the data structure.

## How it Works:
API Endpoint and User Interface: iDUM exposes a user-friendly API endpoint that allows users to upload PDF documents for information extraction. The API endpoint is designed to handle incoming requests and respond with the extracted information in JSON format.

OCR and Image Processing: Upon receiving a PDF document, iDUM uses PaddleOCR to extract text from each page of the document. The OCR model is capable of recognizing text in various languages and can handle both structured and unstructured documents.

JSON Formatting and Key-Value Extraction: The extracted text is processed and organized into a JSON structure with key-value pairs. Each key corresponds to a specific type of information, such as invoice number or GSTIN, while the values represent the extracted data from the document.

Conversation with OpenAI: To enhance the user experience, iDUM engages in a structured conversation with the OpenAI language model. Users can interact with iDUM using natural language, and the model responds with relevant information based on the extracted data.

JSON Output and Response: After processing the document and engaging in a conversation, iDUM returns the extracted information in JSON format. Users can easily access and analyze the information for further use.

## Launch Command:

Before Launching the app in AWS / any cloud instance make sure to install the dependencies in requirement.txt

```
uvicorn api:app
```