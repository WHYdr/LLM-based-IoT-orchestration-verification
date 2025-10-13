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

## 📋 Prerequisites

- Python 3.7+
- Ollama (for local model execution)
- Git

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd LLM-IoT-Configuration-Framework
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Ollama**
   ```bash
   # Install Ollama (if not already installed)
   # Download Zephyr-7B-Beta model
   ollama pull zephyr:7b-beta
   
   # Create custom model with configuration
   ollama create zephyr:7b-beta -f zephyr_configurator
   ```

4. **Start Ollama service**
   ```bash
   ollama serve
   ```

## 🏃‍♂️ Quick Start

### Prerequisites Setup

1. **Start Ollama Service**
   ```bash
   # Start Ollama service (required first)
   ollama serve
   ```

2. **Create Custom Model Configuration**
   ```bash
   # Create custom Zephyr model with configuration
   ollama create zephyr:7b-beta -f zephyr_configurator
   ```

3. **Start IoT Verification Service**
   ```bash
   # Start the verification service backend
   # (Navigate to verify/ directory and start the service)
   cd verify
   python app.py  # or the appropriate service file
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

## 📊 Project Structure

```
IoT-Configuration-Validation-Framework/
├── enhanced_paper_data_collector.py    # Enhanced performance data collection script
├── IoT_Request.py                      # IoT verification service client
├── configurator.txt                    # Configuration generation prompts
├── translator.txt                      # Type classification prompts
├── zephyr_configurator                 # Ollama model configuration
├── enhanced_test_results_*.json         # Test results JSON files
├── enhanced_test_report_*.csv          # Test report CSV files
├── verify/                             # IoT verification service
│   └── (verification service files)    # Backend verification logic
└── Graphs/                             # Visualization tools
    ├── generate_performance_charts.py  # Performance chart generator
    ├── time_consumption.png          # Time consumption chart
    ├── type_accuracy.png              # Type accuracy chart
    └── verification_accuracy.png       # Verification accuracy chart
```

## 🔧 Configuration

### Model Configuration
The framework uses Zephyr-7B-Beta by default. To modify model settings, edit `zephyr_configurator`:

```
FROM zephyr:7b-beta
PARAMETER temperature 0
TEMPLATE """{{- if .System }}
<|system|>
{{ .System }}
</s>
{{- end }}
<|user|>
{{ .Prompt }}
</s>
<|assistant|>
"""
PARAMETER stop "<|system|>"
PARAMETER stop "<|user|>"
PARAMETER stop "<|assistant|>"
PARAMETER stop "</s>"
```

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
- Pressure sensor configurations
- Light sensor configurations

### Actuator Device (AD) Tests
- Smart light actuators
- Motor actuators
- Valve actuators
- Relay actuators
- Pump actuators

### Gateway Device (GW) Tests
- IoT gateway configurations
- Protocol translation gateways
- Device management gateways
- Data aggregation gateways

### Communication Protocol (CP) Tests
- MQTT protocol configurations
- HTTP protocol configurations
- TCP/UDP protocol configurations
- CoAP protocol configurations

### Security Configuration (SC) Tests
- TLS/SSL encryption configurations
- Authentication configurations
- Access control configurations
- Data encryption configurations

### Error Handling Tests
- Invalid protocol handling
- Missing parameter detection
- Configuration conflict detection
- Security vulnerability detection

## 📝 Usage Examples

### Generate MQTT Configuration
```python
from IoT_Request import send_verification_request

# Generate MQTT client configuration
result = send_verification_request(
    verification_type="CP",
    config_commands=["mqtt_client_config"]
)
print(result)
```

### Check IoT Topology Status
```python
from IoT_Request import request_status

# Get current IoT topology status
status = request_status()
print(status)
```

### Run Performance Tests
```python
from enhanced_paper_data_collector import EnhancedPaperDataCollector

# Create data collector
collector = EnhancedPaperDataCollector()

# Run enhanced tests
collector.run_enhanced_tests()
```

### Complete Workflow Example
```python
from IoT_Request import send_verification_request, request_status

# 1. Check service status
status = request_status()
print("Service Status:", status)

# 2. Generate sensor device configuration
sensor_result = send_verification_request(
    verification_type="SD",
    config_commands=["temperature_sensor_config"]
)
print("Sensor Config:", sensor_result)

# 3. Generate actuator device configuration  
actuator_result = send_verification_request(
    verification_type="AD", 
    config_commands=["smart_light_config"]
)
print("Actuator Config:", actuator_result)
```

### Generate Visualization Charts
```python
from Graphs.generate_performance_charts import PerformanceChartGenerator

# Create chart generator
generator = PerformanceChartGenerator("enhanced_test_report_20251013_090406.csv")

# Generate all charts
generator.generate_all_charts()
```

### Sensor Device Configuration Example
```python
# Temperature sensor configuration
sensor_config = {
    "device_id": "temp_001",
    "sensor_type": "temperature", 
    "sampling_rate": 1,
    "data_format": "JSON"
}
```

### Actuator Device Configuration Example
```python
# Smart light actuator configuration
actuator_config = {
    "device_id": "light_001",
    "actuator_type": "smart_light",
    "control_interface": "brightness",
    "safety_features": "overcurrent_protection"
}
```

## 🔍 Troubleshooting

### Common Issues

1. **Connection Failed**
   - Ensure Ollama service is running: `ollama serve`
   - Check IoT verifier service: `python IoT_Request.py`

2. **Model Not Found**
   - Pull the model: `ollama pull zephyr:7b-beta`
   - Verify model exists: `ollama list`

3. **Timeout Errors**
   - Check network connectivity
   - Increase timeout values in configuration

### Health Checks
```bash
# Check Ollama status
ollama list

# Check if custom model exists
ollama list | grep zephyr

# Check IoT verifier service
curl http://127.0.0.1:5000/health

# Test IoT verification service
python IoT_Request.py
```

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

#### Chart Types
1. **Bar Charts**: Performance comparison across types
2. **Line Charts**: Time trends and performance changes
3. **Pie Charts**: Success/failure ratio distribution
4. **Heat Maps**: Performance heat maps for different configuration types

#### Using Visualization Features
```bash
# Generate all charts
cd Graphs
python generate_performance_charts.py

# Specify specific CSV file
python generate_performance_charts.py --csv enhanced_test_report_20251013_090406.csv
```

## 🤝 Contributing

1. Fork this repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Submit a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📚 References

- [Zephyr-7B-Beta Model](https://huggingface.co/HuggingFaceH4/zephyr-7b-beta)
- [Ollama Documentation](https://ollama.ai/docs)
- [IoT Configuration Management Best Practices](https://docs.iot.org/)

## 🆘 Technical Support

For questions or support:
- Check test files for usage examples
- Review generated log files for troubleshooting
- Submit Issues to report bugs or feature requests

## 🎯 Project Highlights

- ✅ Support for 5 IoT device verification types
- ✅ Automated configuration generation and validation
- ✅ Comprehensive performance evaluation framework
- ✅ Automatic visualization analysis
- ✅ Local model support
- ✅ Detailed test reports

---

**Start your IoT configuration management journey!** 🚀
