from fastapi import FastAPI


app = FastAPI()


@app.get("/hello")
def hello():
    return {"message": "Hello, Career CRM!"}


@app.get("/job-postings")
def job_postings():
    return [
        {
            "title": "Software Engineer",
            "company": "Acme Corp"
        },
        {
            "title": "Backend Developer",
            "company": "Example Inc."
        }
    ]