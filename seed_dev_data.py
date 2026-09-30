from sqlalchemy import select
from datetime import datetime, timedelta
from backend.app.database import SessionFactory
from backend.app.models import Application, JobPosting, ApplicationMethod, ApplicationStatus

with SessionFactory() as session:

    if session.scalar(select(Application)):
        raise RuntimeError("Database already contains applications")

    companies = [
        "Northstar Systems",
        "Acme Software",
        "Bluebird Technologies",
        "Lemon Inc.",
        "Aurora Financial Services",
        "City of Angels",
        "University of Sometown",
        "Six-Seven Systems",
        "Consumer Products Inc."
    ]

    titles = [
        "Backend Developer",
        "Software Engineer",
        "Full Stack Developer",
        "Junior Developer",
        "Software Developer",
        "Backend Engineer - New Grad",
        "Junior Backend Developer",
        "Backend Developer - Intern"
    ]

    application_methods = list(ApplicationMethod)
    statuses = list(ApplicationStatus)

    for i in range(30):
        company = companies[i % len(companies)]
        title = titles[i % len(titles)]
        applied_at = datetime.now() - timedelta(days=i * 2)
        how_applied = application_methods[i % len(application_methods)]
        status = statuses[i % len(statuses)]

        job_posting = JobPosting(
            title=title,
            company=company,
        )

        application = Application(
            job_posting=job_posting,
            applied_at=applied_at,
            how_applied=how_applied,
            status=status
        )

        session.add(job_posting)
        session.add(application)

    session.commit()