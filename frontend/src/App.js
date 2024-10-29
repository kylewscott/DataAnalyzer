import React, { useState } from "react";
import "./App.css";

function App() {
    const [explanation, setExplanation] = useState('');
    const [graphUrl, setGraphUrl] = useState('')
    const [prompt, setPrompt] = useState('')

    const handleSubmit = async (event) => {
        event.preventDefault();

        const response =  await fetch(`/api/data?param=${prompt}`);
        if(response.ok) {
            const result = await response.json();
            setExplanation(result.explanation)
            setGraphUrl(`http://localhost:5000${result.graphUrl}?t=${new Date().getTime()}`)
        }
    };

    return (
        <div className="App">
            <header className="App-header">
                <h1>Graph Generation</h1>
                <form onSubmit={handleSubmit} method="post">
                    <input type="text" name="prompt" placeholder="Enter your prompt" value={prompt} onChange={(e) => setPrompt(e.target.value)} required />
                    <input type="submit" value="Generate Graph" />
                </form>
                <p>{explanation}</p>
                {explanation &&
                    <img src={graphUrl} alt="graph"></img>
                }
            </header>
        </div>
    );
}

export default App;