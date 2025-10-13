# IoT Configuration Validation Framework

A comprehensive IoT device configuration validation framework that automatically generates, translates, and validates IoT device configurations. The framework supports 5 main verification types and provides comprehensive performance evaluation and visualization analysis capabilities.

## 🚀 Key Features

- **Automated Configuration Generation**: Generate IoT device configurations from natural language requirements
- **Multi-Protocol Support**: Support for MQTT, TCP, UDP, HTTP and other IoT protocols
- **Configuration Translation**: Convert between different configuration formats
- **Automated Validation**: Validate configuration correctness using custom validation rules for IoT devices
- **Performance Evaluation**: Comprehensive testing framework with detailed performance metrics
- **Local Model Support**: Integrated with Ollama for local model execution
- **Visualization Analysis**: Automatically generate performance charts and statistical reports
- **Multi-Type Validation**: Support for sensor devices, actuator devices, gateways, communication protocols, and security configurations

## 🏃‍♂️ Quick Start

### Prerequisites Setup

1. **Start Ollama Service**
   ```bash
   # Start Ollama service (required first)
   ollama serve
   ```

2. **Create Custom Model Configuration**
   ```bash
   # Create custom Zephyr model with configuration (with right path)
   ollama create zephyr:7b-beta -f zephyr_configurator
   ```

3. **Start IoT Verification Service**
   ```bash
   # Start the verification service backend
   # (Navigate to verify/ directory and start the service)
   cd ...verify #the right path
   python IoT_Verifier.py  
   ```

### Basic Usage

1. **Test IoT Verification Service**
   ```bash
   python IoT_Request.py
   ```

2. **Run Configuration Tests**
   ```bash
   python enhanced_paper_data_collector.py
   ```

### Performance Evaluation

Run comprehensive performance testing and data collection:

```bash
# Run enhanced data collection script
python enhanced_paper_data_collector.py
```

This will generate:
- `enhanced_test_results_*.json` - Detailed test results
- `enhanced_test_report_*.csv` - Statistical summary
- Real-time console output and metrics

### Visualization Analysis

Generate performance charts:

```bash
# Navigate to charts directory
cd Graphs

# Run chart generator
python generate_performance_charts.py
```

This will generate:
- `time_consumption.png` - Time consumption analysis chart
- `type_accuracy.png` - Type accuracy chart
- `verification_accuracy.png` - Verification accuracy chart


## 🔧 Configuration


### Prompt Files Configuration

The framework uses two key prompt files for different tasks:

#### `translator.txt` - Type Classification
This prompt file contains instructions for classifying user requirements into IoT device types:
- **SD (Sensor Device)**: Data collection devices
- **AD (Actuator Device)**: Control/action devices  
- **GW (Gateway)**: Connection/management devices
- **CP (Communication Protocol)**: Network/communication settings
- **SC (Security Configuration)**: Security/authentication settings

#### `configurator.txt` - Configuration Generation
This prompt file contains templates for generating JSON configurations for each device type:
- **SD Templates**: Sensor device configurations with sampling rate, data format, MQTT settings
- **AD Templates**: Actuator device configurations with control interfaces and safety features
- **GW Templates**: Gateway configurations with device management and protocol translation
- **CP Templates**: Communication protocol configurations (MQTT, HTTP, TCP/UDP)
- **SC Templates**: Security configurations with authentication and encryption settings

### Service Configuration
Modify `IoT_Request.py` to change:
- IoT verifier IP and port
- Model name
- Request timeouts

### Validation Framework
The framework uses custom validation rules for different IoT device types:
- **Sensor Devices**: Validates sampling rate, data format, and MQTT configuration
- **Actuator Devices**: Validates control interface and safety features
- **Gateway Devices**: Validates device management and protocol translation capabilities
- **Communication Protocols**: Validates protocol-specific parameters and settings
- **Security Configurations**: Validates authentication and encryption methods

## 📈 Performance Metrics

The framework tracks the following key performance metrics:

### Core Metrics
- **Type Recognition Accuracy**: Percentage of correctly identified configuration types
- **Verification Result Accuracy**: Percentage of successful configuration verifications
- **Average Response Time**: Total time including model inference
- **Classification Performance**: Performance breakdown by configuration type (MQTT, network, etc.)

### Detailed Time Analysis
- **Translation Time**: Time to convert natural language to configuration type
- **Configuration Time**: Time to generate specific configurations
- **Verification Time**: Time for configuration verification
- **Total Time**: Total time for complete workflow

### Supported Verification Types
1. **SD (Sensor Device)**: Sensor device configurations
2. **AD (Actuator Device)**: Actuator device configurations  
3. **GW (Gateway)**: Gateway device configurations
4. **CP (Communication Protocol)**: Communication protocol configurations
5. **SC (Security Configuration)**: Security configurations

## 🧪 Test Cases

The framework includes comprehensive test cases covering 5 verification types:

### Sensor Device (SD) Tests
- Temperature sensor configurations
- Humidity sensor configurations
- Motion sensor configurations

### Actuator Device (AD) Tests
- Smart light actuators
- Motor actuators
- Valve actuators

### Gateway Device (GW) Tests
- IoT gateway configurations
- Eadge gateway with management
  
### Communication Protocol (CP) Tests
- Standard MQTT Client Configuration 
- TLS Encrypted MQTT Configuration 
- TCP Server Configuration 
- UDP Client Configuration

### Security Configuration (SC) Tests
- Authentication and Encryption 
- Certificate-based Security 
- JWT and OAuth Security 

### Error Handling Tests
- Invalid protocol handling
- Missing parameter detection
- Configuration conflict detection
- Security vulnerability detection




## 📊 Results Analysis and Visualization

The framework generates detailed performance reports including:

### Data Output
- **JSON Files**: Complete test result data
- **CSV Files**: Structured data for statistical analysis
- **Real-time Console Output**: Progress tracking and metrics display

### Visualization Features
The framework provides powerful visualization analysis capabilities:

#### Automatic Chart Generation
- **Time Consumption Analysis Chart**: Shows time distribution across different stages
- **Type Accuracy Chart**: Comparison of recognition accuracy across verification types
- **Verification Accuracy Chart**: Analysis of configuration verification success rates


#### Using Visualization Features
```bash
# Generate all charts
cd Graphs
python generate_performance_charts.py

# Specify specific CSV file
python generate_performance_charts.py --csv enhanced_test_report_20251013_090406.csv
```


## 📚 References

- [Zephyr-7B-Beta Model](https://huggingface.co/HuggingFaceH4/zephyr-7b-beta)
- [Ollama Documentation](https://ollama.ai/docs)
- [IoT Configuration Management Best Practices](https://docs.iot.org/)


## 🎯 Project Highlights

- ✅ Support for 5 IoT device verification types
- ✅ Automated configuration generation and validation
- ✅ Comprehensive performance evaluation framework
- ✅ Automatic visualization analysis
- ✅ Local model support
- ✅ Detailed test reports

---

