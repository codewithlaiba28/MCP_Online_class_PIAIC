from agents import Agent, ModelSettings, OpenAIChatCompletionsModel, AsyncOpenAI, RunConfig, Runner, function_tool
from dataclasses import dataclass
import os
import asyncio
from dotenv import load_dotenv
from agents.mcp import MCPServerStreamableHttp, MCPServerStreamableHttpParams, ToolFilterContext

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=client
)



async def main():
    params_config = MCPServerStreamableHttpParams(
        url="http://localhost:8000/mcp/",)
    
    async with MCPServerStreamableHttp(params=params_config) as mcp_hello_server:
        prompts = await mcp_hello_server.list_prompts()
        print("\nAvailable Prompts:\n", prompts)
        greeting_prompt = await mcp_hello_server.get_prompt("general_chat", arguments={"user_name": "Junaid"})
        print("\nGreeting Prompt:\n", greeting_prompt.messages[0].content.text)
        base_agent:Agent = Agent(
            name="WeatherAgent",
            instructions=greeting_prompt.messages[0].content.text,
            model=model,
            mcp_servers=[mcp_hello_server]
        )

        res = await Runner.run(base_agent, "Greet Junaid")
        print(res.final_output)
        res = await Runner.run(base_agent, "What is Sir Qasim mood")

        print(res.final_output)



if __name__ == "__main__":
    asyncio.run(main())    
