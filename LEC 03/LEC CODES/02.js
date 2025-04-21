const { GoogleGenerativeAI } = require("@google/generative-ai");
const dotenv = require("dotenv");

dotenv.config({ path: "../.env" });

const genAI = new GoogleGenerativeAI(process.env.API_KEY);

async function main() {
    const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });

    const prompt = `
        You are an AI assistant who is expert in breaking down complex problems and then resolve the user query.

        For the given user input, analyse the input and break down the problem step by step.
        At least think 5-6 steps on how to solve the problem before solving it down.

        The steps are:
            - analyse
            - think
            - output
            - validate
            - result

        Rules:
            1. Follow strict JSON output: { "step": "string", "content": "string" }
            2. Always perform one step at a time and wait for the next input.
            3. Carefully analyse the user query.

        Example:
            Input: What is 2 + 2.
            Output: { "step": "analyse", "content": "Alright! The user is interested in a maths query and he is asking a basic arithmetic operation." }
            Output: { "step": "think", "content": "To perform the addition I must go from left to right and add all the operands." }
            Output: { "step": "output", "content": "4" }
            Output: { "step": "validate", "content": "Seems like 4 is the correct answer for 2 + 2." }
            Output: { "step": "result", "content": "2 + 2 = 4 and that is calculated by adding all numbers." }

        Now let's solve: What is 3 + 4 * 5.
    `;

    try {
        const result = await model.generateContent(prompt);
        const response = await result.response;
        const text = response.text();

        console.log(text);
    } catch (err) {
        console.error("Fatal error:", err.message);
    }
}

main();
