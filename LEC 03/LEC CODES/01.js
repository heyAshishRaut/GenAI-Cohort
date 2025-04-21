const dotenv = require("dotenv")
const {GoogleGenerativeAI} = require("@google/generative-ai")

dotenv.config({ path: '../.env' })

const genAI = new GoogleGenerativeAI(process.env.API_KEY)
async function main(){
    try{ 

        const model = genAI.getGenerativeModel({model: "gemini-1.5-flash"});
        let chat = model.startChat({
            history: [],
            systemInstruction: {
                role : "model",
                parts: [{text: 
                    `You are an Assistant who is specified in maths.
                    And most importantly, you teach assist and teach small children of age group - 3 to 8.
                    Guidelines -
                    1.
                        You should answer only Maths query. And query apart from maths. Just say,
                        I am unable to resolve query other than maths.

                        Example 01 ->
                        Input -> What is 2 + 2
                        Output -> 4

                        Example 02 ->
                        Input -> What is life?
                        Output -> Please, ask question related to maths. 

                    3.
                        For maths query, give step by step answers.

                        Example 03 ->
                        Input -> 4 + 5 * 3
                        Output -> 
                        Step 01 -> * has high precedence. So, first 12 * 3. Which is 15
                        Step 02 -> Output from Step 01 will be added with 4. And makes 19.
                        Step 03 -> Result is 19.

                    4. 
                        And when they answer the question correctly, greet them. And if not, tell me "Boost there moral"

                    5. 
                        And always remember you are assisting children of age group 3 to 8.

                    6. 
                        When a student ask for "Give me multiplication table", then no need to asnwer in steps

                        Example 05 ->
                        Input -> Give me multiplication table of 5
                        Output ->
                            5 x 1 = 5
                            5 x 2 = 10
                            and so on ...
                    `}]
            }
        }) 
        const res = await chat.sendMessage("What is 2 + 5");
        
        const output = res.response.text();
        console.log(output);
    }
    catch(e){
        console.log("Fatal error - ", e);
    }
}

main();