
type ApplicationListItem = {
    id: number
    job_posting_id: number
    job_title: string
    company: string
    applied_at: string
    how_applied: ApplicationMethod
    status: ApplicationStatus
    last_response_at: string | null
}


export type ApplicationDetail = {
    id: number
    job_posting_id: number
    job_title: string
    company: string
    url: string | null
    saved_at: string
    location: string | null
    salary: string | null
    note: string | null
    cover_letter_required: boolean
    applied_at: string
    how_applied: ApplicationMethod
    status: ApplicationStatus
    last_response_at: string | null
}


export type PaginatedApplicationResponse = {
    items: ApplicationListItem[]
    page: number
    page_size: number
    total: number
}


type ApplicationStatus = 
    | "applied"
    | "invited_to_test"
    | "interview"
    | "offer"
    | "rejected"
    | "withdrawn"

type ApplicationMethod = 
    | "email"
    | "company_website"
    | "LinkedIn"
    | "referral"
    | "other"


export const fetchApplications = async (page: number = 1, pageSize: number = 25): Promise<PaginatedApplicationResponse> => {
    const baseUrl = "http://localhost:8000"
    const url = `${baseUrl}/applications?page=${page}&page_size=${pageSize}`;

    const response = await fetch(url);

    if (!response.ok) {
        throw new Error(`HTTP error. Status: ${response.status}`);
    }

    const data = (await response.json()) as PaginatedApplicationResponse;
    return data;
}


export const fetchApplication = async (applicationId: number): Promise<ApplicationDetail> => {
    const baseUrl = "http://localhost:8000"
    const url = `${baseUrl}/applications/${applicationId}`;

    const response = await fetch(url);

    if (!response.ok) {
        throw new Error(`HTTP error. Status: ${response.status}`, {cause: response.status});
    }

    const data = (await response.json()) as ApplicationDetail;
    return data;
}
