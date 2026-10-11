
export type JobPostingCreate = {
    title: string
    company: string
    url?: string
    location?: string
    salary?: string
    note?: string
    cover_letter_required: boolean
}


export type JobPostingResponse = {
    id: number
    title: string
    company: string
    url: string | null
    saved_at: string
    location: string | null
    salary: string | null
    note: string | null
    cover_letter_required: boolean
}

export interface CreateJobPostingLocationState {
    from: string
}


export const createJobPosting = async (jobPosting: JobPostingCreate): Promise<JobPostingResponse> => {
    const baseUrl = "http://localhost:8000"
    const url = `${baseUrl}/job-postings`;

    const response = await fetch(url, { 
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(jobPosting),
    });

    if (!response.ok) {

        throw new Error(`HTTP Error. Status: ${response.status}`, {cause: response.status});
    }

    const data: JobPostingResponse = await response.json();
    return data;
}