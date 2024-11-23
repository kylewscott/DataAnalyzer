import React, { useState } from "react";
import "./App.css";

function App() {
    const [explanation, setExplanation] = useState('');
    const [graphUrl, setGraphUrl] = useState('')
    const [chatHistory, setChatHistory] = useState([])
    const [prompt, setPrompt] = useState('')

    const handleSubmit = async (event) => {
        event.preventDefault();

        setChatHistory((previousHistory) => [
            ...previousHistory,
            { sender: 'User', text: prompt },
            { sender: 'bot', text: 'result', graphUrl: 'graphUrl' }
        ])
        setPrompt('')
        setExplanation('explenation')
        setGraphUrl(`graphUrl`)

        // const response =  await fetch(`/api/data?param=${prompt}`);

        // if(response.ok) {
        //     const result = await response.json();
        //     setChatHistory((previousHistory) => [
        //         ...previousHistory,
        //         { sender: 'User', text: prompt },
        //         { sender: 'bot', text: result.explanation, graphUrl: result.graphUrl }
        //     ])
        //     setPrompt('')
        //     setExplanation(result.explanation)
        //     setGraphUrl(`http://localhost:5000${result.graphUrl}?t=${new Date().getTime()}`)
        // } 
    };

    return (
        <div className="App">
            <header className="App-header">
                <h1>Graph Generation</h1>
                <div className="chat-history">
                    {chatHistory.map((message, index) => (
                        <div
                            key={index}
                            className={`chat-message ${
                                message.sender === "User" ? "user-message" : "bot-message"
                            }`}
                        >
                            <p>{message.text}</p>
                            {message.graphUrl && (
                                <img
                                    src={`http://localhost:5000${message.graphUrl}?t=${new Date().getTime()}`}
                                    alt="graph"
                                />
                            )}
                        </div>
                    ))}
                </div>
                <form onSubmit={handleSubmit}>
                    <input
                        type="text"
                        name="prompt"
                        placeholder="Ask a question"
                        value={prompt}
                        onChange={(e) => setPrompt(e.target.value)}
                        required
                    />
                    <button type="submit">↑</button>
                </form>
            </header>
        </div>
    );
}

export default App;