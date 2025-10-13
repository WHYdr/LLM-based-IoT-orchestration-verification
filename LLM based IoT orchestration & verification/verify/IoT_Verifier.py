from flask import Flask, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

# IoT Device Registry - stores device configurations and topology information
iot_devices = {}
iot_topology = {}

def load_iot_topology():
    """
    Load IoT network topology configuration from JSON file.
    Handles file loading errors and provides fallback empty topology.
    """
    global iot_topology
    try:
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        topology_file = os.path.join(script_dir, 'iot_topology.json')
        
        with open(topology_file, 'r') as f:
            iot_topology = json.load(f)
        print(f"IoT topology loaded successfully from {topology_file}")
    except Exception as e:
        print(f"Error loading IoT topology: {str(e)}")
        iot_topology = {"edges": []}

def load_iot_devices():
    """
    Load IoT device configurations from JSON files in the iot_devices directory.
    Scans for all .json files and loads them into the device registry.
    """
    global iot_devices
    try:
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        devices_dir = os.path.join(script_dir, 'iot_devices')
        
        if os.path.exists(devices_dir):
            for filename in os.listdir(devices_dir):
                if filename.endswith('.json'):
                    device_id = filename.replace('.json', '')
                    device_file = os.path.join(devices_dir, filename)
                    with open(device_file, 'r') as f:
                        iot_devices[device_id] = json.load(f)
        print(f"Loaded {len(iot_devices)} IoT devices from {devices_dir}")
    except Exception as e:
        print(f"Error loading IoT devices: {str(e)}")

def validate_sensor_config(config_commands):
    """
    Validate sensor device configuration parameters and requirements.
    
    Args:
        config_commands: Configuration commands to validate
        
    Returns:
        dict: Validation results with success status and error details
    """
    validation_results = {
        "syntax_check": True,
        "protocol_check": True,
        "data_format_check": True,
        "security_check": True,
        "errors": []
    }
    
    # Check for required sensor parameters
    required_params = ["device_id", "sensor_type", "sampling_rate", "data_format"]
    for param in required_params:
        if param not in str(config_commands):
            validation_results["errors"].append(f"Missing required parameter: {param}")
            validation_results["syntax_check"] = False
    
    # Check MQTT configuration
    if "mqtt" in str(config_commands).lower():
        # Required MQTT parameters for sensors
        required_mqtt_params = ["broker", "topic"]
        for param in required_mqtt_params:
            if param not in str(config_commands):
                validation_results["errors"].append(f"Missing required MQTT parameter: {param}")
                validation_results["protocol_check"] = False
        
        # Optional MQTT parameters
        optional_mqtt_params = ["port", "qos", "username", "password"]
        missing_optional = []
        for param in optional_mqtt_params:
            if param not in str(config_commands):
                missing_optional.append(param)
        
        if missing_optional:
            validation_results["errors"].append(f"Missing optional MQTT parameters: {', '.join(missing_optional)} (using defaults)")
    
    return validation_results

def validate_actuator_config(config_commands):
    """
    Validate actuator device configuration parameters and safety requirements.
    
    Args:
        config_commands: Configuration commands to validate
        
    Returns:
        dict: Validation results with success status and error details
    """
    validation_results = {
        "syntax_check": True,
        "protocol_check": True,
        "control_check": True,
        "safety_check": True,
        "errors": []
    }
    
    # Check for required actuator parameters
    required_params = ["device_id", "actuator_type", "control_interface", "safety_features"]
    for param in required_params:
        if param not in str(config_commands):
            validation_results["errors"].append(f"Missing required parameter: {param}")
            validation_results["syntax_check"] = False
    
    # Check control interface
    if "control_interface" in str(config_commands):
        validation_results["control_check"] = True
    else:
        validation_results["errors"].append("Missing control interface configuration")
        validation_results["control_check"] = False
    
    return validation_results

def validate_gateway_config(config_commands):
    """
    Validate IoT gateway configuration parameters and management capabilities.
    
    Args:
        config_commands: Configuration commands to validate
        
    Returns:
        dict: Validation results with success status and error details
    """
    validation_results = {
        "syntax_check": True,
        "protocol_check": True,
        "device_management_check": True,
        "security_check": True,
        "data_format_check": True,
        "control_check": True,
        "safety_check": True,
        "authentication_check": True,
        "encryption_check": True,
        "general_check": True,
        "errors": []
    }
    
    # Check for required gateway parameters
    required_params = ["device_id", "max_connected_devices", "protocol_translation", "device_discovery"]
    for param in required_params:
        if param not in str(config_commands):
            validation_results["errors"].append(f"Missing required parameter: {param}")
            validation_results["syntax_check"] = False
    
    # Check device management capabilities
    if "device_management" in str(config_commands):
        validation_results["device_management_check"] = True
    else:
        validation_results["errors"].append("Missing device management configuration")
        validation_results["device_management_check"] = False
    
    return validation_results

def validate_communication_protocol(config_commands):
    """
    Validate communication protocol configuration parameters and settings.
    
    Args:
        config_commands: Configuration commands to validate
        
    Returns:
        dict: Validation results with success status and error details
    """
    validation_results = {
        "syntax_check": True,
        "protocol_check": True,
        "security_check": True,
        "qos_check": True,
        "errors": []
    }
    
    # Try to parse JSON configuration
    config_dict = {}
    try:
        if isinstance(config_commands, str):
            config_dict = json.loads(config_commands)
        elif isinstance(config_commands, dict):
            config_dict = config_commands
    except:
        # If JSON parsing fails, treat as string
        config_dict = {}
    
    # Check for supported protocols (expanded list)
    supported_protocols = ["mqtt", "coap", "http", "websocket", "lora", "zigbee", "tcp", "udp"]
    protocol_found = False
    config_str = str(config_commands).lower()
    
    for protocol in supported_protocols:
        if protocol in config_str:
            protocol_found = True
            break
    
    if not protocol_found:
        validation_results["errors"].append("No supported communication protocol found")
        validation_results["protocol_check"] = False
    
    # Check MQTT specific parameters with flexible matching
    if "mqtt" in config_str:
        # Required MQTT parameters with flexible matching
        required_mqtt_params = ["broker", "topic"]
        missing_required = []
        
        for param in required_mqtt_params:
            param_found = False
            
            # Check in JSON structure
            if config_dict:
                # Direct parameter
                if param in config_dict:
                    param_found = True
                # Check nested structures
                elif "subscriptions" in config_dict and isinstance(config_dict["subscriptions"], list):
                    for sub in config_dict["subscriptions"]:
                        if isinstance(sub, dict) and param in sub:
                            param_found = True
                            break
                # Check alternative naming (camelCase, etc.)
                elif param == "topic":
                    alt_names = ["topicFilter", "topic_name", "mqtt_topic"]
                    for alt_name in alt_names:
                        if alt_name in config_dict:
                            param_found = True
                            break
            
            # Check in string representation
            if not param_found:
                param_found = param in config_str
            
            if not param_found:
                missing_required.append(param)
        
        if missing_required:
            validation_results["errors"].append(f"Missing required MQTT parameter: {', '.join(missing_required)}")
            validation_results["protocol_check"] = False
        
        # Optional MQTT parameters (warn if missing but don't fail)
        optional_mqtt_params = ["port", "qos", "username", "password"]
        missing_optional = []
        
        for param in optional_mqtt_params:
            param_found = False
            
            # Check in JSON structure
            if config_dict and param in config_dict:
                param_found = True
            # Check in string representation
            elif param in config_str:
                param_found = True
            
            if not param_found:
                missing_optional.append(param)
        
        # Add warning for missing optional parameters
        if missing_optional:
            validation_results["errors"].append(f"Missing optional MQTT parameters: {', '.join(missing_optional)} (using defaults)")
    
    # Check TCP/UDP specific parameters
    elif "tcp" in config_str or "udp" in config_str:
        # For TCP/UDP, we just need to verify the protocol is mentioned
        validation_results["protocol_check"] = True
    
    return validation_results

def validate_security_config(config_commands):
    """
    Validate security configuration parameters and authentication settings.
    
    Args:
        config_commands: Configuration commands to validate
        
    Returns:
        dict: Validation results with success status and error details
    """
    validation_results = {
        "syntax_check": True,
        "authentication_check": True,
        "encryption_check": True,
        "access_control_check": True,
        "errors": []
    }
    
    # Check for authentication
    auth_methods = ["username", "password", "certificate", "jwt", "oauth"]
    auth_found = False
    for method in auth_methods:
        if method in str(config_commands).lower():
            auth_found = True
            break
    
    if not auth_found:
        validation_results["errors"].append("No authentication method found")
        validation_results["authentication_check"] = False
    
    # Check for encryption
    encryption_methods = ["tls", "ssl", "aes", "encryption"]
    encryption_found = False
    for method in encryption_methods:
        if method in str(config_commands).lower():
            encryption_found = True
            break
    
    if not encryption_found:
        validation_results["errors"].append("No encryption method found")
        validation_results["encryption_check"] = False
    
    return validation_results

@app.route('/verify', methods=['POST'])
def verify_iot_configuration():
    """
    Verify IoT device configuration based on verification type.
    Routes to appropriate validator based on device type.
    
    Returns:
        JSON response with verification results and status
    """
    data = request.get_json()
    
    verification_type = data.get("verification_type", "DEFAULT")
    commands = data.get("commands", [])
    
    print(f"Verifying IoT configuration for type: {verification_type}")
    print(f"Commands: {commands}")
    
    # Determine verification type and call appropriate validator
    if verification_type == "SD":
        result = validate_sensor_config(commands)
    elif verification_type == "AD":
        result = validate_actuator_config(commands)
    elif verification_type == "GW":
        result = validate_gateway_config(commands)
    elif verification_type == "CP":
        result = validate_communication_protocol(commands)
    elif verification_type == "SC":
        result = validate_security_config(commands)
    else:
        result = {
            "syntax_check": True,
            "general_check": True,
            "errors": []
        }
    
    # Determine overall result
    all_checks_passed = all([
        result.get("syntax_check", True),
        result.get("protocol_check", True),
        result.get("data_format_check", True),
        result.get("security_check", True),
        result.get("control_check", True),
        result.get("safety_check", True),
        result.get("device_management_check", True),
        result.get("authentication_check", True),
        result.get("encryption_check", True),
        result.get("general_check", True)
    ])
    
    # Filter out warnings from errors for final result determination
    critical_errors = []
    warnings = []
    
    for error in result.get("errors", []):
        if "using defaults" in error or "not specified" in error:
            warnings.append(error)
        else:
            critical_errors.append(error)
    
    # Success if all checks passed and no critical errors (warnings are OK)
    if all_checks_passed and not critical_errors:
        return jsonify({
            "result": "Successful",
            "verification_type": verification_type,
            "timestamp": datetime.now().isoformat(),
            "details": result,
            "warnings": warnings
        })
    else:
        return jsonify({
            "result": "Verification failed",
            "verification_type": verification_type,
            "timestamp": datetime.now().isoformat(),
            "errors": critical_errors,
            "warnings": warnings,
            "details": result
        })

@app.route('/topology', methods=['GET'])
def get_iot_topology():
    """
    Retrieve current IoT network topology information.
    
    Returns:
        JSON response with topology data and device information
    """
    try:
        return jsonify({
            "topology": iot_topology,
            "devices": list(iot_devices.keys()),
            "device_count": len(iot_devices),
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/devices', methods=['GET'])
def get_iot_devices():
    """
    Retrieve all registered IoT device information.
    
    Returns:
        JSON response with complete device registry
    """
    try:
        return jsonify({
            "devices": iot_devices,
            "device_count": len(iot_devices),
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/devices/<device_id>', methods=['GET'])
def get_iot_device(device_id):
    """
    Retrieve specific IoT device information by device ID.
    
    Args:
        device_id (str): Unique identifier for the device
        
    Returns:
        JSON response with device configuration or error message
    """
    try:
        if device_id in iot_devices:
            return jsonify({
                "device": iot_devices[device_id],
                "timestamp": datetime.now().isoformat()
            })
        else:
            return jsonify({"error": f"Device {device_id} not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for service monitoring.
    
    Returns:
        JSON response with service status and metrics
    """
    return jsonify({
        "status": "healthy",
        "service": "IoT Configuration Verifier",
        "timestamp": datetime.now().isoformat(),
        "devices_loaded": len(iot_devices),
        "topology_loaded": len(iot_topology.get("edges", []))
    })

if __name__ == '__main__':
    """
    Main execution function for IoT Configuration Verifier service.
    Initializes device registry, loads configurations, and starts Flask server.
    """
    print("Initializing IoT Configuration Verifier...")
    load_iot_topology()
    load_iot_devices()
    print("IoT Configuration Verifier started on port 5000")
    app.run(host='0.0.0.0', port=5000, debug=True)



