const dotenv =  require("dotenv")
const {GoogleGenerativeAI} = require("@google/generative-ai")

dotenv.config()

const genAI = new GoogleGenerativeAI(process.env.API_KEY)

async function main(){
    try{
        const model = genAI.getGenerativeModel({model: "gemini-1.5-flash"})
        const response = await model.generateContent("What is life")
        const output = response.response.text();
        console.log(output);
    }
    catch(e){
        console.log(e);
    }
}

main()