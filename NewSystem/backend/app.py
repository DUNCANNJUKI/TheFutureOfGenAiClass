from fastapi import FastAPI

app = FastAPI(title="NewSystem Backend")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/hello")
def hello():
    return {"message": "Hello from NewSystem backend"}
