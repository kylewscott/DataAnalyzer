import React, { useEffect, useState } from "react";
import "./App.css";

function App() {
    const [chatHistory, setChatHistory] = useState([]);
    const [prompt, setPrompt] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);

    useEffect(() => {
        const clearGraphs = async () => {
            try {
                const response = await fetch('http://localhost:8000/cleanup', { method: 'GET' });
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

        const response = await fetch("http://localhost:8000/analyze", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ prompt }),
        });

        if (response.ok) {
            const result = await response.json();

            setChatHistory((previousHistory) => [
                ...previousHistory,
                { sender: 'User', text: prompt },
                { sender: 'bot', text: result.response.explanation, graph_path: result.response.graph_path },
            ]);
            setPrompt('');
        }

        setIsSubmitting(false);
    };

    const handleInputChange = (event) => {
        setPrompt(event.target.value);
    };

    const download = e => {
        console.log(e.target.href);
        fetch(e.target.href, {
          method: "GET",
          headers: {}
        })
          .then(response => {
            response.arrayBuffer().then(function(buffer) {
              const url = window.URL.createObjectURL(new Blob([buffer]));
              const link = document.createElement("a");
              link.href = url;
              link.setAttribute("download", "image.png"); 
              document.body.appendChild(link);
              link.click();
            });
          })
          .catch(err => {
            console.log(err);
          });
      };

    return (
        <div className="App">
            <header className="App-header">
                <h1>Data Analyzer</h1>
                <p style={{ fontSize: '22px' }}>Ask for explanations about the data and graph generations</p>
                <p></p>
                <div className="chat-history">
                    {chatHistory.map((message, index) => 
                    (
                        <div
                            key={index}
                            className={`chat-message ${
                                message.sender === "User" ? "user-message" : "bot-message"
                            }`}
                        >
                            <p>{message.text}</p>
                            {message.graph_path && (
                                <div>
                                    <img
                                        src={`http://localhost:8000/${message.graph_path}`}
                                        alt="graph"
                                        className="graph-image"
                                    />
                                    <a
                                        href={`http://localhost:8000/${message.graph_path}`}
                                        download
                                        onClick={e => {
                                            e.preventDefault()
                                            download(e)
                                        }}
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
