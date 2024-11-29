from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from LLM_news_analyzer.output_generator import OutputGenerator
import os
import json

app = FastAPI()

templates = Jinja2Templates(directory="templates")
static_path = os.path.join(os.path.dirname(__file__), 'templates', 'static')
app.mount("/static", StaticFiles(directory=static_path), name="static")

# Initialize the Output geenrator
categories = "politics, sports, finance, technology, entertainment, others"
processor = OutputGenerator(categories)

@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("index.html", 
                                      {"request": request}
                                      )


@app.post("/", response_class=HTMLResponse)
async def process_articles(request: Request, urls: str = Form(...)):
    url_list = [url.strip() for url in urls.split('\n') if url.strip()]
    if url_list:
        results = processor.process(url_list)   
        # Parse the JSON string into a Python object
        results = json.loads(results)    

        return templates.TemplateResponse("results.html", 
                                          {"request": request, 
                                           "results": results}
                                           )
    return templates.TemplateResponse("index.html", 
                                      {"request": request, 
                                       "error": "No valid URLs provided"}
                                       )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)