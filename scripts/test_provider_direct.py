import asyncio
import os
import json
from dotenv import load_dotenv

load_dotenv()

from app.compatibility.hermes_request import VmChatInput, GlobalQueryParameters
from app.orchestrator.vmchat_orchestrator import _call_build_generate_prompt
from app.provider.langchain_provider import LangChainVmChatProvider
from app.provider.fixed_provider import ModelSkillRunInput
from app.resources.resource_loader import ResourceLoader
from app.resources.skill_resource_reader import SkillResourceReader, SkillResourceReaderOptions

async def test_provider_direct():
    loader = ResourceLoader()
    await loader.load()
    resources = loader.get_resources()
    
    input_val = VmChatInput(userMessage="浏览器端到端：股票净敞口时序", globalQueryParameters=GlobalQueryParameters(names=[], nonemptyFlags={}))
    
    sys_prompt, user_prompt = _call_build_generate_prompt(input_val, resources.skill_md)
    
    provider = LangChainVmChatProvider()
    
    reader = SkillResourceReader(resources, SkillResourceReaderOptions(maxContextChars=120000, initialContextChars=0))
    run_input = ModelSkillRunInput(
        system_prompt=sys_prompt,
        user_prompt=user_prompt,
        read_resource=lambda p: reader.read(p),
        signal=None
    )
    
    print("Starting direct stream...")
    count = 0
    try:
        async for chunk in provider.run_skill(run_input):
            count += 1
            print("CHUNK:", repr(chunk))
            if count > 50:
                print("... (more chunks)")
                break
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_provider_direct())
