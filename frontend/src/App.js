import React, { useEffect, useState } from "react";
import "./App.css";

function App() {
    const [explanation, setExplanation] = useState('');
    const [graphUrl, setGraphUrl] = useState('');
    const [chatHistory, setChatHistory] = useState([]);
    const [prompt, setPrompt] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);

    useEffect(() => {
        const clearGraphs = async () => {
            try {
                const response = await fetch('/api/clear_graphs', { method: 'POST' });
                if (!response.ok) {
                    console.error('Failed to clear graph directory:', await response.text());
                }
            } catch (error) {
                console.error('Error clearing graph directory:', error);
            }
        };

        clearGraphs();
    }, []);

    const handleSubmit = async (event) => {
        event.preventDefault();

        // Prevent further submission if already submitting
        if (isSubmitting) return;

        setIsSubmitting(true);

        const response = await fetch(`/api/data?param=${prompt}`);
        if (response.ok) {
            const result = await response.json();

            setChatHistory((previousHistory) => [
                ...previousHistory,
                { sender: 'User', text: prompt },
                { sender: 'bot', text: result.explanation, graphUrl: result.graphUrl },
            ]);
            setPrompt('');
            setExplanation(result.explanation);

            // Store the graph URL without the changing timestamp in the URL
            setGraphUrl(result.graphUrl);
        }

        setIsSubmitting(false);
    };

    const handleInputChange = (event) => {
        setPrompt(event.target.value);
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
                                <div>
                                    <img
                                        src={`http://localhost:5000${message.graphUrl}`}
                                        alt="graph"
                                        className="graph-image"
                                    />
                                    <a
                                        href={message.graphUrl}
                                        download={`graph_${index}.png`}
                                        className="download-link"
                                    >
                                        Download Graph
                                    </a>
                                </div>
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
                        onChange={handleInputChange}
                        required
                    />
                    <button type="submit" disabled={isSubmitting}>↑</button>
                </form>
            </header>
        </div>
    );
}

export default App;
