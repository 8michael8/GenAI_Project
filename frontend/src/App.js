import React, { useState} from 'react';
import './App.css';

function App() {
    const [question, setQuestion] = useState("");
    const [messages, setMessages] = useState([]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!question){
            return;
        }
        setQuestion(question.trim())
        setMessages((prev) => [
            ...prev,
            {sender: "user", text: question}
        ]);
        setQuestion("");

        try {
            const response = await fetch("/api/query", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({question: question})
            });
            const {results} = await response.json();

            setMessages((prev) => [
                ...prev,
                ...results.map((r) => ({
                    sender: "bot",
                    title: `${r.section} - ${r.title}`,
                    text:  `${r.content}`,
                    citation: r.citation
                }))
            ]);
        } catch (err) {
            console.log(err);
        }
    }

    return (
        <div className = "chatBot">
            <div className = "chat">
                <div className = "messages">
                    {messages.map((m, i) => (
                        <div key = {i} className = {`message ${m.sender}`}>
                            <h3>{m.title}</h3>
                            <p className = "message_output">{m.text}</p>
                            {m.sender === "user" && (
                                <p className = "out_notice">Here's What I can Find:</p>
                            )}
                            {m.sender === "bot" && (
                                <a href={m.citation} target="_blank" rel="noreferrer">
                                    CITATION
                                </a>
                            )}
                        </div>
                    ))}
                </div>
                <div className = "questionSearch">
                    <form onSubmit={handleSubmit} className = "search_bar">
                        <input
                            type = "text"
                            value = {question}
                            onChange ={(e) => setQuestion(e.target.value)}
                            placeholder = "What Would You Like to Know about Washington State Legislature?"
                        />
                        <button type = "submit">SUBMIT</button>
                    </form>
                </div>
            </div>
        </div>
    );
}

export default App;