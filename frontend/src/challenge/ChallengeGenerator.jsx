import React from "react";
import {useState} from "react";

export function ChallengeGenerator(){

    const [challenge, setChallenge] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);
    const [quota, setQuota] = useState(null);
    const [difficulty, setDifficulty] = useState("easy");

    // we need to fetch quota
    const fetchQuota = async () => {
        try {
            const response = await fetch('/api/quota');
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await response.json();
            setQuota(data.quota);
        } catch (error) {
            console.error('Error fetching quota:', error);
            setError('Error fetching quota');
        }
    }

    // fetch challenge
    const generateChallenge = async () => {}

    //next reset time
    const nextResetTime = () => {}


    return (
        <div className = "challenge-container">
            <h2>Coding Challenger Generator</h2>

            <div className="quota-display">
                <p>Challenges remaning today: {quota?.quota_remaining||0}</p>
                {quota?.quota_remaining===0 && (
                        <p>Next reset: {0}</p>
                )}
            </div>


            <div className="difficulty-selector">
                <label htmlFor="difficulty">Select Difficulty: </label>
                <select id = "difficulty" 
                        value = {difficulty} 
                        onChange={(e) => setDifficulty(e.target.value)} 
                        disabled = {isLoading}
                >
                    <option value="easy">Easy</option>
                    <option value="medium">Medium</option>
                    <option value="hard">Hard</option>

                </select>
                
            </div>

            <button
            className="generate-button"
            onClick={generateChallenge} disabled={isLoading || quota?.quota_remaining === 0}
            >{isLoading ? "Generating...." : "Generate Challenge"}</button>

            {error && <div className="error-message"><p>{error}</p></div>}

            {challenge && <MCQChallenge challenge={challenge} />}
        </div>
    );
}