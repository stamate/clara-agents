from autogen import ConversableAgent

from agents.text_agents import (
    task_coordinator_agent,
)
from tools.clara_tools import (
    clara_add_abilities_to_adversary_profile,
    clara_api_get_operation_info,
    clara_api_method_details,
    clara_api_request,
    clara_create_adversary_profile,
    clara_execute_command_on_agent,
    clara_service_list,
    clara_swagger_info,
    clara_upload_file_from_agent,
    match_techniques_to_clara_abilities,
)
from utils.shared_config import llm_config

clara_agent = ConversableAgent(
    name="clara_agent",
    llm_config=llm_config,
    human_input_mode="NEVER",
    code_execution_config=False,
    max_consecutive_auto_reply=5,
    is_termination_msg=lambda msg: (
        "terminate" in (msg.get("content") or "").lower() if msg else False
    ),
    description="""A helpful assistant that can interact with Clara agents""",
    system_message="""Append "TERMINATE" to your response when you successfully completed the objective.""",
)


def register_tools():
    # Service List
    clara_agent.register_for_llm(
        name="clara_service_list",
        description="Retrieve the list of all running services on the Clara agent.",
    )(clara_service_list)

    task_coordinator_agent.register_for_execution(name="clara_service_list")(
        clara_service_list
    )

    # Swagger info

    clara_agent.register_for_llm(
        name="clara_swagger_info",
        description="Retrieve the list of all available Clara API methods along with a description of their functionality",
    )(clara_swagger_info)

    task_coordinator_agent.register_for_execution(name="clara_swagger_info")(
        clara_swagger_info
    )

    # Get details on a specific API method

    clara_agent.register_for_llm(
        name="clara_api_method_details",
        description="Retrieve the details on a specific API method in Clara including the parameters it takes and the responses it returns.",
    )(clara_api_method_details)

    task_coordinator_agent.register_for_execution(name="clara_api_method_details")(
        clara_api_method_details
    )

    # Perform an API request to Clara

    clara_agent.register_for_llm(
        name="clara_api_request",
        description="Perform an API request to Clara based on the given API method extracted from the Swagger documentation.",
    )(clara_api_request)

    task_coordinator_agent.register_for_execution(name="clara_api_request")(
        clara_api_request
    )

    # Create an Adversary profile in Clara

    clara_agent.register_for_llm(
        name="clara_create_adversary_profile",
        description="Create an Adversary profile in Clara",
    )(clara_create_adversary_profile)

    task_coordinator_agent.register_for_execution(name="clara_create_adversary_profile")(
        clara_create_adversary_profile
    )

    # Add abilities to an Adversary profile in Clara

    clara_agent.register_for_llm(
        name="clara_add_abilities_to_adversary_profile",
        description="Add abilities to an Adversary profile in Clara",
    )(clara_add_abilities_to_adversary_profile)

    task_coordinator_agent.register_for_execution(name="clara_add_abilities_to_adversary_profile")(
        clara_add_abilities_to_adversary_profile
    )

    # Get the ID of the active Clara Operation

    clara_agent.register_for_llm(
        name="clara_api_get_operation_info",
        description="Get the ID of the active Clara Operation",
    )(clara_api_get_operation_info)

    task_coordinator_agent.register_for_execution(
        name="clara_api_get_operation_info"
    )(clara_api_get_operation_info)

    # Exfiltrate file over FTP

    clara_agent.register_for_llm(
        name="clara_upload_file_from_agent",
        description="Upload a file from the agent to the Clara server using FTP.",
    )(clara_upload_file_from_agent)

    task_coordinator_agent.register_for_execution(
        name="clara_upload_file_from_agent"
    )(clara_upload_file_from_agent)

    # Execute a command on a specific agent

    clara_agent.register_for_llm(
        name="clara_execute_command_on_agent",
        description="Execute a command on a specific agent",
    )(clara_execute_command_on_agent)

    task_coordinator_agent.register_for_execution(
        name="clara_execute_command_on_agent"
    )(clara_execute_command_on_agent)


    # Match techniques to Clara abilities

    clara_agent.register_for_llm(
        name="match_techniques_to_clara_abilities",
        description="Match techniques to Clara abilities",
    )(match_techniques_to_clara_abilities)

    task_coordinator_agent.register_for_execution(name="match_techniques_to_clara_abilities")(
        match_techniques_to_clara_abilities
    )
