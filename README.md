# LLM based news analyzer

## Overview

A web application built with FastAPI leveraging Large Language Models (LLMs) to analyze and summarize articles from the web. Users can input URLs of articles, and the application will fetch the content, classify it, and provide a summary. This project demonstrates the integration of modern web technologies with AI capabilities.


## Features

- Fetches and processes articles from provided URLs.
- Extracts text content from HTML paragraphs.
- Classifies articles using LLMs.
- Summarizes articles for quick insights.
- User-friendly web interface built with FastAPI and Jinja2.
- Deployed on Cyclic for easy access.


## Technologies Used

- **FastAPI**: A modern web framework for building APIs with Python.
- **google.generativeai**: A framework for working with LLMs.
- **BeautifulSoup**: A library for parsing HTML and XML documents.
- **Uvicorn**: An ASGI server for running FastAPI applications.
- **Cyclic**: A cloud platform for deploying web applications.
- **poetry**: package management.


## Installation

### Prerequisites

Make sure you have Python 3.7 or higher installed on your machine. You also need to have Poetry installed to manage dependencies.

### Clone the Repository

```bash
git clone https://github.com/zahidcseku/llm-news-analyzer.git
cd llm-news-analyzer