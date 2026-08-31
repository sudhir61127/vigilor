from fastapi import FastAPI

app = FastAPI(title="VIGIL-OR AI Backend")


@app.get("/")
def root():
    return {"message": "VIGIL-OR AI Backend is running"}
