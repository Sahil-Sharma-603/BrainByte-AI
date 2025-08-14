import React from "react";
import {useState, useEffect} from "react";
import { MCQChallenge } from '../challenge/MCQChallenge'

export function HistoryPanel(){

    const [history, setHistory] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        setIsLoading(true);
        fetchHistory()
    
    }, []);



    // fetch history
    const fetchHistory = async () => {
        setIsLoading(false);
    }

    // if loading then show loading
    if(isLoading){
        return <div className="loading">Loading history...</div>
    }

    // if error then show error
    if(error){
        return <div className="error-message">
            <p>{error}</p>
            <button onClick = {fetchHistory}>Retry</button>
        </div>
    }

    
    return <div className="history-panel">
        <h2>History</h2>
        {/* if there is no history the show no history available else show the list of history */}
        {history.length === 0 ? <p>No history available</p> : 
        <div className="history-list">
            {history.map((challenge) => {
                return <MCQChallenge challenge = {challenge} 
                                     key = {challenge.id}
                                     showExplanation = {true}
                           
                                     />
            })}
        
        </div>
        }
    </div>
}