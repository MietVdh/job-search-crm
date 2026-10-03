import { useState, useEffect } from 'react'
import { fetchApplications } from './api/applications'
import { Link, useSearchParams } from 'react-router'
import type { PaginatedApplicationResponse } from './api/applications'


function ApplicationsPage() {
  const [isLoading, setIsLoading] = useState(true)
  const [response, setResponse] = useState<PaginatedApplicationResponse | null>(null)
  const [error, setError] = useState<Error | null>(null)
  const [page, setPage] = useState(1);
  const [searchParams, setSearchParams] = useSearchParams();

  const hasData = response !== null && response.total > 0;
  const totalPages = response
    ? Math.ceil(response.total / response.page_size)
    : 0;

  const isValidPageParam = (Number.isInteger(searchParams.get("page")) 
                        && Number(searchParams.get("page")) > 0 
                        && Number(searchParams.get("page")) <= totalPages);

  let pageParam: number = isValidPageParam ? Number(searchParams.get("page")) : 1;
   
  
  const handlePreviousClick = () => {
    // setSearchParams({ page: (pageParam - 1).toString()});
    // pageParam -= 1;
    setPage(page -1);
  }

  const handleNextClick = () => {
    // setSearchParams({ page: (pageParam + 1).toString()});
    // pageParam += 1;
    setPage(page + 1);
  }

  // useEffect(() => {
  //   // Normalize URL 
  //   if (searchParams.get("page") === null) {
  //       setSearchParams({});
  //       pageParam = 1;
  //   } else if (isValidPageParam) {
  //       pageParam = Number(searchParams.get("page"));
  //       setSearchParams({page: pageParam.toString()});
  //   } else {
  //       setSearchParams({});
  //   }
  // }, [isValidPageParam]);


  useEffect(() => {

    fetchApplications(page)
    .then((response) => {
      setResponse(response);
      setError(null);
      setIsLoading(false);
    //   setSearchParams({page: pageParam.toString()});
    })
    .catch((error) => {
      setError(error);
      setIsLoading(false);
      setResponse(null);
      setSearchParams({});
    })

  }, [page]);

  return (
    <main className="max-w-3xl m-auto py-8">
      <h1 className="text-center text-2xl font-bold my-5">Applications</h1>
      <p>{isLoading ? "Loading..." : ""}</p>
      <p>{error ? error.message : ""}</p>
      <p>{response?.total === 0 ? "No applications found" : ""}</p>
      {hasData && <table className="w-full">
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
      }
      {hasData && <div className="py-6 m-auto max-w-lg text-center">
        <button 
          className="bg-blue-500 text-white font-bold py-2 px-4 rounded hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50" 
          disabled={page === 1} 
          onClick={handlePreviousClick}
        >Previous</button>
        <span className="px-8">Page {pageParam} of {totalPages}</span>
        <button 
          className="bg-blue-500 text-white font-bold py-2 px-4 rounded hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50"
          disabled={page === totalPages} 
          onClick={handleNextClick}
        >Next</button>
      </div>}
    </main>
  )
}

export default ApplicationsPage;