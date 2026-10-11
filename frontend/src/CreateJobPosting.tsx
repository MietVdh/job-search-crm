// import { useState, useEffect, useRef } from 'react'
// import { createJobPosting } from './api/jobPostings';
// import type { JobPostingCreate } from './api/jobPostings';

import { Link, useLocation, useNavigate } from 'react-router';
import type { JobPostingCreate, CreateJobPostingLocationState } from "./api/jobPostings";

function CreateJobPosting() {

    const location = useLocation();
    const navigate = useNavigate();

    const state = location.state as CreateJobPostingLocationState | null;
    const returnTo = state?.from ?? "/applications";

    const handleFormSubmit = (e: React.SubmitEvent) => {
        e.preventDefault();

        const form = e.currentTarget as HTMLFormElement;
        const formData = new FormData(form);

        const getString = (formData: FormData, name: string): string => {
            const value = formData.get(name);

            if (typeof value !== "string") {
                throw new Error(`Expected ${name} to be a string`);
            }

            return value.trim();
        }

        const title = getString(formData, "title");
        const company = getString(formData, "company");
        const cover_letter_required = formData.has("cover_letter_required");

        const url = getString(formData, "url");
        const location = getString(formData, "location");
        const salary = getString(formData, "salary");
        const note = getString(formData, "note");

        // Check that title and company are not empty strings after trimming whitespace
        const getInput = (form: HTMLFormElement, name: string): HTMLInputElement => {
            const element = form.elements.namedItem(name);

            if (!(element instanceof HTMLInputElement)) {
                throw new Error(`Expected ${name} to be an input`);
            }

            return element;
        }

        const titleInput = getInput(form, "title");
        const companyInput = getInput(form, "company");

        titleInput.setCustomValidity("");
        companyInput.setCustomValidity("");

        if (!title) {
            titleInput.setCustomValidity("Title cannot be blank.");
            console.log("Title cannot be blank");
        } 

        if (!company) {
            companyInput.setCustomValidity("Company cannot be blank.");
        } 

        if (!title || !company) {
            form.reportValidity();
            console.log("Title and/or company missing");
            return;
        }

        // Create JobPosting
        const jobPosting: JobPostingCreate = {
            title,
            company,
            cover_letter_required,
            ...(url && { url }),
            ...(location && { location }),
            ...(salary && { salary }),
            ...(note && { note })
        };

        // if success
        navigate(returnTo, {
            state: { message: "Job posting created." }
        });
    }


    return (
        <main className="max-w-3xl m-auto py-8">
            <Link to={returnTo}
                className="bg-blue-500 text-white font-bold py-2 px-4 rounded hover:bg-blue-700">
            Go Back
            </Link>

            <form onSubmit={handleFormSubmit}>
                <label htmlFor="title">Title</label>
                <input 
                    id="title"
                    type="text" 
                    name="title" 
                    required
                    onChange={(e) => e.currentTarget.setCustomValidity("")}
                />
                <label htmlFor="company">Company</label>
                <input 
                    id="company" 
                    type="text" 
                    name="company" 
                    required
                    onChange={(e) => e.currentTarget.setCustomValidity("")}
                />
                <label htmlFor="url">Posting URL</label>
                <input 
                    id="url"
                    type="url" 
                    name="url" 
                />
                <label htmlFor="location">Location</label>
                <input 
                    id="location"
                    type="text" 
                    name="location" 
                />
                <label htmlFor="salary">Salary</label>
                <input
                    id="salary" 
                    type="text" 
                    name="salary" 
                />
                <label htmlFor="note">Notes
                    <textarea 
                    id="note"
                    name="note"
                    rows={5}
                    cols={50}
                    wrap="hard"
                />
                </label>
                
                <input 
                    id="cover-letter-required"
                    type="checkbox" 
                    name="cover_letter_required"
                    value="true"
                />
                <label htmlFor="cover-letter-required">Cover letter required</label>
                <button className="bg-blue-500 text-white font-bold py-2 px-4 rounded hover:bg-blue-700" type="submit">Create Job Posting</button>
            </form>
        </main>
    
)}

export default CreateJobPosting;

