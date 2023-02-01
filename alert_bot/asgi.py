from fastapi import FastAPI


app = FastAPI


@app.post("/alert")
def post_alert():
    pass
