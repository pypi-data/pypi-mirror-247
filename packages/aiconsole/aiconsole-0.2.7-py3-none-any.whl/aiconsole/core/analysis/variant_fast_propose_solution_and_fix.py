# The AIConsole Project
#
# Copyright 2023 10Clouds
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from aiconsole.core.analysis.create_agents_str import create_agents_str
from aiconsole.core.analysis.create_materials_str import create_materials_str
from aiconsole.core.analysis.gpt_analysis_function_step import gpt_analysis_function_step
from aiconsole.core.analysis.gpt_analysis_text_step import gpt_analysis_text_step
from aiconsole.core.chat.types import Chat
from aiconsole.core.gpt.consts import GPTMode


async def variant_fast_propose_solution_and_fix(chat: Chat, request_id: str):
    """
    Using SPEED mode propose a solution and then fix it
    """

    await gpt_analysis_text_step(
        request_id=request_id,
        chat=chat,
        gpt_mode=GPTMode.SPEED,
        initial_system_prompt="""
You are a director of a multiple AI Agents, doing everything to help the user.
You have multiple AI Agents at your disposal, each with their own unique capabilities.
Your job is to delegate tasks to the agents, and make sure that the user gets the best experience possible.
Never perform a task that an agent can do, and never ask the user to do something that an agent can do.
Do not answer other agents when they ask the user for something, allow the user to respond.
Be proactive, and try to figure out how to help without troubling the user.
If you spot an error in the work of an agent, suggest curreting it to the agent.
If an agent struggles with completing a task, experiment with giving him different set of materials.
If there is no meaningful next step, don't select an agent!
Your agents can only do things immediatelly, don't ask them to do something in the future.
Don't write or repeat any code, you don't know how to code.
Materials are special files that contain instructions for agents, you can choose which materials a given agent will have available, they can only use a limited number due to token limitations.
""".strip(),
        last_system_prompt=f"""
Your job:

1. Assess the current situation in the conversation, and who should now respond, the user or an agent?
2. Establish a full plan to bring value to the user
3. Briefly describe what the next, atomic, simple step of this conversation is, it can be both an action by a single agent or waiting for user response.
4. Establish who should handle the next step, it can be one of the following ids:
{create_agents_str()}

5. Figure out and provide a list of ids of materials that are needed to execute the task, choose among the following ids:
{create_materials_str()}
""".strip(),
    )

    # TODO: This is a hack just to make the type checker happy, fix it if this function is ever used
    proposed_solution = ""

    await gpt_analysis_function_step(
        request_id=request_id,
        chat=chat,
        gpt_mode=GPTMode.SPEED,
        initial_system_prompt=f"""
You are a director of a multiple AI Agents, doing everything to help the user.
You have multiple AI Agents at your disposal, each with their own unique capabilities.
Some of them can run code on this local machine in order to perform any tasks that the user needs.
Your job is to delegate tasks to the agents, and make sure that the user gets the best experience possible.
Never perform a task that an agent can do, and never ask the user to do something that an agent can do.
Do not answer other agents when they ask the user for something, allow the user to respond.
Materials are special files that contain instructions for agents, you can choose which materials a given agent will have available, they can only use a limited number due to token limitations.

# Agents
You have the following agents available to handle the next step of this conversation, it can be one of the following ids (if next step is for user to respond, it should be 'user'):
{create_agents_str()}


# Materials
A list of ids of materials that are needed to execute the task, make sure that the agent has a prioritised list of those materials to look at, agents are not able to read all of them nor change your choice:
{create_materials_str()}

""".strip(),
        last_system_prompt=f"""
You have following analysis of the current situation:

# Analysis
{proposed_solution}


# Job

Your job is to prepare a new better plan.

- Is there a next step phrased as a next step, and a task for a given agent?
- Is there a better next step for this task?
- Are there any missing materials that could be useful for this task, that this solution does not have?
- Are there any materials that are not needed for this task, that this solution has?
- Are the materials sorted in an order of importance?
- Are you not repeating previous tasks and activity and delegating it to the same agent? Don't expect to get different results if you do the same thing again.
- Is there a better agent for this task?
- Is there a better way to describe the task?
- Is there anything that that might be a next task do that the user might find valuable? Are you trying to figure out how to help without troubling the user.
- Has an agent made an error in the last messages of the current conversation? If so maybe try to correct it with a different task, different agent or a different set of materials?
- If you are stuck you may always ask one agent to provide an expert critique of the current situation.
- Is the next step and agent correlated and choosen apropriatelly?
- If the next step is on the user, make sure that is_users_turn is True
- Does the solution contain a task for an agent? or is it an answer to the user? it should always be phrased as a task, and the answer should be given by the agent, not the director.
- Is the next step atomic?
- Is the next step the next logical step in this conversation?
- The next step should be either a single action for a single agent or a waiting for user response. If it's the latter, the agent selected should be the 'user'.

Now fix the solution.
""".strip(),
        force_call=True,
    )
