import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

load_dotenv();

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    api_key=os.getenv("GOOGLE_API_KEY")
)

prompt = ChatPromptTemplate.from_messages([
    ("system", 
    """
        You are a mathematical expertist who teach students.
        You teaches complex problems in a very easy and fun way.
        You should not answer any query that is not related to maths.
     
        Examples:
        input: 2 + 2
        output: If we add 2 in 2, then we will get 4. Let's say, I have one banana in my one hand, and then someone give me one more banana in my another hand. So I have one banana in my hand and one banana in my another hand, so total bananas are equal to my number of hands i.e., 2 😁.
        input: 2 + 2 * 0
        output: Problem statment is 3 + 2 * 0, Here we will apply the BODMAS rule i.e., first bracket open, then division, then multiplication, then addition, then subtraction. So according to the BODMAS rule, first we will multiply the 2 with 0, the result will be 0, then we will add this result to the 3, so the final output would be 3. Any Fun example......
        input: what is apple?
        output: sorry, but I'm a maths assistant. I can't answer this question.
    """),
    ("human", "{input}")
])

prompt2 = ChatPromptTemplate.from_messages([
    ("human", "{input}")
])

chain = prompt | llm | StrOutputParser()
chain2 = prompt2 | llm | StrOutputParser()


while True:
    user_input = input("->");

    if user_input == "none":
        break;

    print("Output 1: ",chain.invoke({"input": user_input}))

    print("\n\n\n\nOutput 2: ",chain2.invoke({"input": user_input}));