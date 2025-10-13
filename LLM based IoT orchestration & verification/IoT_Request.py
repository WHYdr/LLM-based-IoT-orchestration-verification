import requests
import os
import pandas as pd
import ollama
import time
from datetime import timedelta

# Configuration settings for IoT verification service
IOT_VERIFIER_IP = '127.0.0.1'  # IoT verifier service IP address
IOT_VERIFIER_PORT = '5000'     # IoT verifier application port (default: 5000)
MODEL_NAME = 'zephyr:7b-beta'  # Model to be used for configuration generation

def request_status():
    """
    Retrieve current IoT topology status from the verification service.
    
    Returns:
        dict: IoT topology information or error message
    """
    try:
        # Make a GET request to the /topology route
        response = requests.get(f"http://{IOT_VERIFIER_IP}:{IOT_VERIFIER_PORT}/topology")

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Return the response content (IoT topology information)
            return response.json()
        else:
            return ("Failed to retrieve IoT topology information. Status code:", response.status_code)
    except Exception as e:
        return ("An error occurred:", str(e))

def send_verification_request(verification_type, config_commands):
    """
    Send configuration verification request to the IoT verifier service.
    
    Args:
        verification_type (str): Type of verification (SD, AD, GW, CP, SC)
        config_commands (list): Configuration commands to verify
        
    Returns:
        dict: Verification result from the IoT verifier service
    """
    url = f"http://{IOT_VERIFIER_IP}:{IOT_VERIFIER_PORT}/verify"
    payload = {
        "verification_type": verification_type,
        "commands": config_commands
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

if __name__ == "__main__":
    """
    Main execution function for IoT configuration validation service.
    Handles user input, configuration generation, and verification.
    """
    # Read the content of the prompt files
    translation_path = 'translator.txt'
    configuration_path = 'configurator.txt'

    with open(translation_path, "r", encoding="utf-8") as file:
        translator = file.read().strip()

    with open(configuration_path, "r", encoding="utf-8") as file:
        configurator = file.read().strip()

    # Validate prompt files are not empty
    if not translator:
        raise ValueError("Translator file is empty. Program stopped.")

    if not configurator:
        raise ValueError("Configurator file is empty. Program stopped.")

    print("IoT Configuration Validation Service Started")
    print("Enter 'quit' to exit the program")
    print("-" * 50)

    while True:
        requirement = input('IoT Requirement: ')
        
        # Check for exit command
        if requirement.lower() in ['quit', 'exit', 'q']:
            print("Exiting IoT Configuration Validation Service")
            break

        # Retrieve current IoT topology status
        topology_status = request_status()
        
        print("""
            \n------------------------ IoT Topology Status ----------------------------\n
        """)
        print(topology_status)
        
        # Prepare translation prompt with topology context
        translator_prompt = translator + str(
            topology_status) + "\n Use this information to gather relevant IoT information for the {requirements} goal. You are not authorized to make explanations of any type."

        # Step 1: Translate natural language requirement to configuration type
        try:
            trad = ollama.chat(model=MODEL_NAME,
                               messages=[{'role': 'system', 'content': translator_prompt}, {'role': 'user', 'content': requirement}])
        except Exception as e:
            print(f"Translation error: {e}")
            continue

        print("""
            \n------------------------ IoT Translation Model Answer ----------------------------\n
        """)
        print(trad)

        trad_response = trad['message']['content']

        # Extract and validate verification type from response
        verification_type = trad_response[:2].strip()
        
        # Validate verification type
        valid_types = ['SD', 'AD', 'GW', 'CP', 'SC']
        if verification_type not in valid_types:
            print(f" Warning: Invalid verification type '{verification_type}'. Expected one of {valid_types}")
            print(f" Full response: {trad_response[:100]}...")
            # Try to extract verification type from the response
            for vtype in valid_types:
                if vtype in trad_response:
                    verification_type = vtype
                    print(f"✅ Found valid type '{verification_type}' in response")
                    break
            else:
                print("❌ No valid verification type found in response")
                continue

        # Step 2: Generate specific configuration based on translated type
        try:
            config = ollama.chat(model=MODEL_NAME,
                                 messages=[{'role': 'system', 'content': configurator}, {'role': 'user', 'content': trad_response}])
        except Exception as e:
            print(f"Configuration generation error: {e}")
            continue
            
        if config:
            print("""
                \n------------------------ IoT Configuration Model Answer ----------------------------\n
            """)
            print(config)
            config_response = config['message']['content']

            # Step 3: Send configuration to IoT Verifier for validation
            try:
                verification_result = send_verification_request(verification_type, config_response)
                print("IoT Verification result for", verification_type, ":", verification_result)
            except Exception as e:
                print(f"Verification error: {e}")
        else:
            print("IoT Configuration failed for requirement:", requirement)



