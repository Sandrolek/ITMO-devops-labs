from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def read_root():
    html_content = """
    <html>
        <head>
            <title>App</title>
        </head>
        <body>
            <h1>App 1</h1>
        </body>
    </html>
    """
    return html_content
