// Frontend connecting to backend integration

import {useAuth} from "@clerk/clerk-react"


// Custom hook to make API requests - useApi hook that will allow us to make use 
//of makeRequest function that will send the request to the backend with the token

export const useApi = () => {
    // allow to get token
    const {getToken} = useAuth()

    const makeRequest = async (enpoint, options ={}) =>{
        const token = await getToken()
        const defaultOptions = {
            headers: {
                "Content-type": "application/json",
                "Authorization": `Bearer ${token}`
            }
        }

        // console.log("Token being sent:", token);

        // Now make the request to backend
        const response = await fetch(`http://0.0.0.0:8000/api${enpoint}`,
            {...defaultOptions, ...options}
        )

        if (!response.ok){
            const errorData = await response.json().catch(()=>{null})
            if (response.status === 429){
                throw new Error("Daily Limit exceeded. Please try again tomorrow.")
            }

            throw new Error(errorData?.detail || "Something went wrong")

        }

        return response.json()
    }

    return {makeRequest}
}
