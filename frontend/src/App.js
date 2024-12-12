import React, { useEffect, useState } from "react";
import "./App.css";

function App() {
    const [chatHistory, setChatHistory] = useState([]);
    const [prompt, setPrompt] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [selectedFile, setSelectedFile] = useState(null); 
    const [dataFileName, setDataFileName] = useState('')

    //**SWITCH THIS URL WHEN WANTING TO RUN LOCALLY */
    const URL = 'https://dataanalyzer-hkhn.onrender.com' //*LIVE DEPLOY*/
    //const URL = 'http://localhost:8000' //*LOCAL DEVELOPEMENT*/

    useEffect(() => {
        const clearGraphs = async () => {
            try {
                const response = await fetch(`${URL}/cleanup`, { method: 'GET' });
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

        const request_data = {
            prompt, 
            file_name: dataFileName
        }

        const response = await fetch(`${URL}/analyze`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(request_data),
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

    const handleFileUpload = async () => {
        if (!selectedFile) {
            alert("Please select a file to upload.");
            return;
        }

        const formData = new FormData();
        formData.append("file", selectedFile);

        try {
            const response = await fetch(`${URL}/upload`, {
                method: "POST",
                body: formData,
            });
            const result = await response.json();

            if (response.ok) {
                alert(`File uploaded successfully: ${result.file_name}`);
                setDataFileName(result.file_name)

            } else {
                alert(`Error: ${result.detail}`);
            }
        } catch (error) {
            console.error("Upload failed", error);
            alert("An error occurred during upload.");
        }
    };


    const handleFileChange = (event) => {
        setSelectedFile(event.target.files[0]);
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
                <p style={{ fontSize: '22px' }}>Upload a CSV file and ask questions about the data or ask to generate a graph</p>
                <div className="file-upload">
                    <input
                        type="file"
                        onChange={handleFileChange}
                        accept=".csv"
                    />
                    <button onClick={handleFileUpload}>
                        Upload File
                    </button>
                <p></p>
                </div>
                {dataFileName &&
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
                                            src={URL+message.graph_path}
                                            alt="graph"
                                            className="graph-image"
                                        />
                                        <a
                                            href={URL+message.graph_path}
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
                }
                {dataFileName &&
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
                }
            </header>
        </div>
    );
}

export default App;
