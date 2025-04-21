const dotenv = require("dotenv")
const {GoogleGenerativeAI} = require("@google/generative-ai")

dotenv.config()

const genAI = new GoogleGenerativeAI(process.env.API_KEY)

async function main(){
    try{
        const model = genAI.getGenerativeModel({model: "gemini-1.5-flash"})
        const chat = model.startChat({
            history: [
                {
                    role: "user",
                    parts: [{text: "Hello"}]
                },
                {
                    role: "model",
                    parts: [{text: "Hello fork, what's up"}]
                }
            ],
            systemInstruction: {
                role: "system",
                parts: [{ text: "You are a friendly chatbot that solves programming queries in short responses." }]
            }
        })

        const res = await chat.sendMessage("How you can help me?");
        const out = res.response.text();
        console.log(out);
        
    }
    catch(e){
        console.log("Error - ", e);
        
    }
}

main()
