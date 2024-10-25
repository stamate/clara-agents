import sys
import warnings

import autogen
import autogen.runtime_logging

import actions.agent_actions
from agents import clara_agents, code_agents, text_agents
from agents.text_agents import (
    task_coordinator_agent,
)
from utils.logs import print_usage_statistics
from utils.shared_config import clean_working_directory


def init_agents():
    # Disable logging User warnings - better for demos
    # Suppress UserWarnings
    warnings.filterwarnings("ignore", category=UserWarning)

    # Clean working directories
    clean_working_directory("/clara")
    clean_working_directory("/pdf")
    clean_working_directory("/code")

    # Register tools
    text_agents.register_tools()
    clara_agents.register_tools()
    code_agents.register_tools()


def retrieve_agent(agent_name):
    if agent_name == "clara_agent":
        return clara_agents.clara_agent
    elif agent_name == "internet_agent":
        return text_agents.internet_agent
    elif agent_name == "text_analyst_agent":
        return text_agents.text_analyst_agent
    elif agent_name == "cmd_exec_agent":
        return code_agents.cmd_exec_agent
    else:
        return None


def run_scenario(scenario_name):
    init_agents()

    scenario_agents = []
    scenario_messages = []

    scenario_tasks = []

    if scenario_name in actions.agent_actions.scenarios.keys():
        scenario_action_names = actions.agent_actions.scenarios[scenario_name]

        for scenario_action_name in scenario_action_names:
            for scenario_action in actions.agent_actions.actions[
                scenario_action_name
            ]:
                scenario_agents.append(scenario_action["agent"])
                scenario_messages.append(scenario_action["message"])

                scenario_task = {
                    "recipient": retrieve_agent(scenario_action["agent"]),
                    "message": scenario_action["message"],
                    "silent": False,
                }

                if "clear_history" in scenario_action:
                    scenario_task["clear_history"] = scenario_action["clear_history"]
                else:
                    scenario_task["clear_history"] = True

                if "summary_prompt" in scenario_action:
                    scenario_task["summary_prompt"] = scenario_action["summary_prompt"]

                if "summary_method" in scenario_action:
                    scenario_task["summary_method"] = scenario_action["summary_method"]

                if "carryover" in scenario_action:
                    scenario_task["carryover"] = scenario_action["carryover"]

                scenario_tasks.append(scenario_task)

    if scenario_messages:
        logging_session_id = autogen.runtime_logging.start(config={"dbname": "logs.db"})
        task_coordinator_agent.initiate_chats(scenario_tasks)
        autogen.runtime_logging.stop()
        print_usage_statistics(logging_session_id)
    else:
        print("Scenario not found, exiting")


if __name__ == "__main__":

    # Check if a scenario is provided
    if len(sys.argv) < 2:
        print(
            "Please provide a scenario to run. Example: python %s DETECT_EDR"
            % sys.argv[0]
        )
        sys.exit()

    scenario_to_run = sys.argv[1]
    run_scenario(scenario_to_run)
