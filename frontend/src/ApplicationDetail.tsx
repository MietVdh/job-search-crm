import { Link, useParams } from 'react-router';
import { useState, useEffect } from 'react'
import { fetchApplication } from './api/applications'
import type { ApplicationDetail } from './api/applications'

function ApplicationDetail() {

    const [isLoading, setIsLoading] = useState(true)
    const [application, setApplication] = useState<ApplicationDetail | null>(null)
    const [error, setError] = useState<Error | null>(null)
    

    const params = useParams();
    const applicationId = Number(params.applicationId);

    const isValidApplicationId = Number.isInteger(applicationId) && applicationId > 0;

    let status;

    switch (application?.status) {
        case "applied":
            status = "Applied";
            break;
        case "interview":
            status = "Interview";
            break;
        case "invited_to_test":
            status = "Invited to test";
            break;
        case "offer":
            status = "Offer";
            break;
        case "rejected":
            status = "Rejected";
            break;
        case "withdrawn":
            status = "Withdrawn";
            break;
        default:
            status = "—";
            break;
    }

    let applicationMethod;

    switch (application?.how_applied) {
        case "LinkedIn":
            applicationMethod = "LinkedIn";
            break;
        case "company_website":
            applicationMethod = "Company website";
            break;
        case "email":
            applicationMethod = "Email";
            break;
        case "referral":
            applicationMethod = "Referral";
            break;
        case "other":
            applicationMethod = "Other";
            break;
        default:
            applicationMethod = "—";
            break; 
    }
   

    useEffect(() => {
        if (!isValidApplicationId) {
            return;
        }
    
        fetchApplication(applicationId)
        .then((response) => {
          setApplication(response);
          setError(null);
          setIsLoading(false);
        })
        .catch((error) => {
          setError(error);
          setIsLoading(false);
          setApplication(null);
        })
    
      }, [applicationId]);

    if (!isValidApplicationId) {
        return (
        <div className="max-w-3xl m-auto py-6">
            <h1>Invalid Application ID</h1>
            <Link to="/applications">Back to Applications</Link>
        </div>)
    }

    if (error){
        if (error.cause === 404) {
            return (
                <div className="max-w-3xl m-auto py-6">
                    <h2>Application not found</h2>
                    <Link to="/applications">Back to Applications</Link>
                </div>
            );
        } else {
            return (
                <div className="max-w-3xl m-auto py-6">
                    <h2>{error.message}</h2>
                    <Link to="/applications">Back to Applications</Link>
                </div>
            )
        }
    }

    if (isLoading) {
        return (
            <main className="max-w-3xl m-auto py-6">
                <h2>Loading...</h2>
            </main>
        )
    }

    if (!application) {
        return (
            <main className="max-w-3xl m-auto py-6">
                <h2>Application not found</h2>
                <Link to="/applications">Back to Applications</Link>
            </main>
        )
    }

    return (
        <main className="max-w-3xl m-auto py-6">
            <h1 className="text-left text-2xl font-bold my-5">{application.job_title} at {application.company} </h1>
            <section className="pb-4">
                <h2 className="font-bold mb-2">Job Posting</h2>
                <dl className="grid grid-cols-[12rem_1fr] gap-y-2 gap-x-4">
                    <dt className="font-medium">Job Title</dt>
                    <dd>{application.job_title}</dd>
                    <dt className="font-medium">Company</dt>
                    <dd>{application.company}</dd>
                    <dt className="font-medium">Posting URL</dt>
                    <dd>{application.url 
                        ? <a className="text-blue-600 hover:text-blue-800" href={application.url} target="_blank" rel="noopener noreferrer">View job posting ↗</a> 
                        : "—"}</dd>
                    <dt className="font-medium">Date Saved</dt>
                    <dd>{application.saved_at}</dd>
                    <dt className="font-medium">Location</dt>
                    <dd>{application.location ?? "—"}</dd>
                    <dt className="font-medium">Salary</dt>
                    <dd>{application.salary ?? "—"}</dd>
                    <dt className="font-medium">Notes</dt>
                    <dd>{application.note ?? "—"}</dd>
                    <dt className="font-medium">Cover Letter Required</dt>
                    <dd>{application.cover_letter_required ? "Yes" : "No"}</dd>
                </dl>
            </section>
            <section className="pb-4">
                <h2 className="font-bold mb-2">Application</h2>
                <dl className="grid grid-cols-[12rem_1fr] gap-y-2 gap-x-4">
                    <dt className="font-medium">Date Applied</dt>
                    <dd>{application.applied_at}</dd>
                    <dt className="font-medium">How Applied</dt>
                    <dd>{applicationMethod}</dd>
                    <dt className="font-medium">Status</dt>
                    <dd>{status}</dd>
                    <dt className="font-medium">Last Response</dt>
                    <dd>{application.last_response_at ?? "—"}</dd>
                </dl>
            </section>
            <Link to="/applications">Back to Applications</Link>
        </main>
    )
}

export default ApplicationDetail