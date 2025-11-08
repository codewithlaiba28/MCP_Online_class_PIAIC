from agents import Agent, ModelSettings, OpenAIChatCompletionsModel, AsyncOpenAI, RunConfig, Runner, function_tool
from dataclasses import dataclass
import os
import asyncio
from dotenv import load_dotenv
from agents.mcp import MCPServerStreamableHttp, MCPServerStreamableHttpParams, create_static_tool_filter

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
    
    static_filtering = create_static_tool_filter(blocked_tool_names=[], allowed_tool_names=["special_greeting"])
    async with MCPServerStreamableHttp(params=params_config, tool_filter=static_filtering, cache_tools_list= True) as mcp_hello_server:
        
        mcp_hello_server.invalidate_tools_cache()
        base_agent:Agent = Agent(
            name="WeatherAgent",
            instructions="You are a helpful assistant.",
            model=model,
            mcp_servers=[mcp_hello_server]
        )

        res = await Runner.run(base_agent, "Greet Junaid")
        print(res.final_output)
        res = await Runner.run(base_agent, "What is Sir Qasim mood")

        print(res.final_output)



if __name__ == "__main__":
    asyncio.run(main())    
