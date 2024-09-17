from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    html_content = """
    <html>
        <head>
            <title>App</title>
        </head>
        <body>
            <h1>App 2</h1>
        </body>
    </html>
    """
    return html_content
