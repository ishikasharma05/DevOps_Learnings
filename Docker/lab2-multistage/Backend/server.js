const express = require("express");
const cors = require("cors");

const app = express();

app.use(cors());
app.use(express.json());

app.post("/chat", (req, res) => {

    const message = req.body.message;

    const replies = [
        "Interesting!",
        "Tell me more.",
        "I'm learning Docker too 😊",
        "That sounds amazing.",
        "Can you explain that further?",
        "Docker Multi Stage Builds are awesome!"
    ];

    const random =
        replies[Math.floor(Math.random() * replies.length)];

    res.json({
        reply: random
    });

});

app.listen(5000, () => {
    console.log("Server running");
});