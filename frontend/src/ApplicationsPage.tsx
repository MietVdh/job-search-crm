import { useState, useEffect } from 'react'
import { Link, useLocation, useNavigate } from 'react-router'
import { fetchApplications } from './api/applications'
import type { CreateJobPostingLocationState } from './api/jobPostings'
import type { PaginatedApplicationResponse } from './api/applications'


function ApplicationsPage() {
  const [isLoading, setIsLoading] = useState(true)
  const [response, setResponse] = useState<PaginatedApplicationResponse | null>(null)
  const [error, setError] = useState<Error | null>(null)
  const [page, setPage] = useState(1);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  
  const location = useLocation();
  const navigate = useNavigate();

  const hasData = response !== null && response.total > 0;
  const totalPages = response
    ? Math.ceil(response.total / response.page_size)
    : 0;

   
  // Button behaviour
  const handlePreviousClick = () => {
    setPage(page -1);
  }

  const handleNextClick = () => {
    setPage(page + 1);
  }

    
  const handleNewPosting = () => {
    const statePayload: CreateJobPostingLocationState = {
      from: location.pathname + location.search + location.hash
    }
    navigate("/job-postings/new", {
      state: statePayload
    });
  }
 

  // Fetch applications
  useEffect(() => {

    fetchApplications(page)
    .then((response) => {
      setResponse(response);
      setError(null);
      setIsLoading(false);
    })
    .catch((error) => {
      setError(error);
      setIsLoading(false);
      setResponse(null);
    })

  }, [page]);


  // If redirect after successfully creating job posting
  const message = location.state?.message;

  useEffect(() => {
    if (!message) {
      return;
    }

    setSuccessMessage(message);

    // Replace current history entry to clear state
    navigate(".", { 
      replace: true, 
      state: null 
    });
  }, [message, navigate]);


  // Display notification
  useEffect(() => {
    if (!successMessage) {
      return;
    }

    const timeoutId = setTimeout(() => {
      setSuccessMessage(null);
    }, 3000);

    return () => {
      clearTimeout(timeoutId);
    }
  }, [successMessage])

  // Rendering 

  if (isLoading) {
    return (
      <main className="max-w-3xl m-auto py-6">
          <h2>Loading...</h2>
      </main>
    )
  }


  if (error) {
    return (
      <div className="max-w-3xl m-auto py-6">
          <h2>{error.message}</h2>
          <Link to="/applications">Back to Applications</Link>
      </div>
    )
  }

  if (response?.total === 0 || !hasData) {
    return (
      <div className="max-w-3xl m-auto py-6">
          <h2>No applications found</h2>
          <Link to="/applications">Back to Applications</Link>
      </div>
    )
  }


  return (
    <main className="max-w-3xl m-auto py-8">
      <h1 className="text-center text-2xl font-bold my-5">Applications</h1>
      <button 
        className="bg-blue-500 text-white font-bold py-2 px-4 rounded hover:bg-blue-700" 
        onClick={handleNewPosting}
      >
        Add job posting
      </button>
      {successMessage && <h2 className="text-center text-lg font-bold my-5">{successMessage}</h2>}

      <table className="w-full">
        <thead className="font-bold text-left border-b">
          <tr>
            <th className="pb-2 px-3">Job Title</th>
            <th className="pb-2 px-3">Company</th>
            <th className="pb-2 px-3">Applied</th>
            <th className="pb-2 px-3">Status</th>
          </tr>
        </thead>
        <tbody>
          {response?.items.map((application) => (
            <tr className="border-b border-mist-300" key={application.id}>
              <td className="py-1 px-3">
                <Link to={`/applications/${application.id}`}>
                    {application.job_title}
                </Link>
              </td>
              <td className="py-1 px-3">{application.company}</td>
              <td className="py-1 px-3">{new Intl.DateTimeFormat("en-CA", {month: "short", day: "numeric", year: "numeric"}).format(new Date(application.applied_at))}</td>
              <td className="py-1 px-3">{application.status}</td>
            </tr>
          ))}
        </tbody>
      </table> 
    
      <div className="py-6 m-auto max-w-lg text-center">
        <button 
          className="bg-blue-500 text-white font-bold py-2 px-4 rounded hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50" 
          disabled={page === 1} 
          onClick={handlePreviousClick}
        >Previous</button>
        <span className="px-8">Page {page} of {totalPages}</span>
        <button 
          className="bg-blue-500 text-white font-bold py-2 px-4 rounded hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50"
          disabled={page === totalPages} 
          onClick={handleNextClick}
        >Next</button>
      </div>
    </main>
  )
}

export default ApplicationsPage;