#!/usr/bin/env python3
"""
Enhanced Performance Data Collection Script - Covering All 5 Verification Types
This script performs comprehensive testing of IoT configuration validation framework
across different device types and communication protocols.
"""

import requests
import ollama
import time
import json
import csv
from datetime import datetime
import os

class EnhancedPerformanceDataCollector:
    """
    Enhanced performance data collector for IoT configuration validation testing.
    Handles comprehensive testing across multiple verification types and generates
    detailed performance metrics and reports.
    """
    
    def __init__(self):
        """Initialize the data collector with model configuration and prompt files."""
        self.model_name = 'zephyr:7b-beta'
        self.results = []
        
        # Load configuration prompt files
        try:
            with open('translator.txt', 'r', encoding='utf-8') as f:
                self.translator_prompt = f.read().strip()
            with open('configurator.txt', 'r', encoding='utf-8') as f:
                self.configurator_prompt = f.read().strip()
        except FileNotFoundError as e:
            print(f"Error: Cannot find prompt file - {e}")
            return
    
    def get_enhanced_test_cases(self):
        """
        Get comprehensive test cases covering all 5 verification types.
        Returns a list of test cases with requirements, expected types, and success criteria.
        """
        return [
            # ===== SENSOR DEVICE (SD) TESTS =====
            {
                "requirement": "Configure a temperature sensor with device ID temp_001, sampling rate 1Hz, data format JSON",
                "expected_type": "SD",
                "expected_success": True,
                "category": "Temperature_Sensor",
                "description": "Temperature Sensor Configuration"
            },
            {
                "requirement": "Set up humidity sensor, device ID humidity_01, sampling every 30 seconds, send data via MQTT",
                "expected_type": "SD",
                "expected_success": True,
                "category": "Humidity_Sensor",
                "description": "Humidity Sensor with MQTT"
            },
            {
                "requirement": "Configure motion sensor with device ID motion_001, sampling rate 10Hz, data format binary",
                "expected_type": "SD",
                "expected_success": True,
                "category": "Motion_Sensor",
                "description": "Motion Sensor Configuration"
            },
            {
                "requirement": "Set up pressure sensor but missing device ID",
                "expected_type": "SD",
                "expected_success": False,
                "category": "Incomplete_Sensor",
                "description": "Incomplete Sensor Configuration"
            },
            
            # ===== ACTUATOR DEVICE (AD) TESTS =====
            {
                "requirement": "Configure smart light actuator, device ID light_001, control brightness 0-100%, response time <100ms",
                "expected_type": "AD",
                "expected_success": True,
                "category": "Smart_Light",
                "description": "Smart Light Actuator Configuration"
            },
            {
                "requirement": "Set up motor actuator, device ID motor_01, speed control 0-1000 RPM, safety limits enabled",
                "expected_type": "AD",
                "expected_success": True,
                "category": "Motor_Actuator",
                "description": "Motor Actuator with Safety"
            },
            {
                "requirement": "Configure valve actuator, device ID valve_001, position control 0-100%, emergency stop function",
                "expected_type": "AD",
                "expected_success": True,
                "category": "Valve_Actuator",
                "description": "Valve Actuator Configuration"
            },
            {
                "requirement": "Set up actuator but no safety mechanism specified",
                "expected_type": "AD",
                "expected_success": False,
                "category": "Unsafe_Actuator",
                "description": "Actuator without Safety"
            },
            
            # ===== GATEWAY (GW) TESTS =====
            {
                "requirement": "Configure IoT gateway, device ID gateway_01, support max 100 devices, protocol translation MQTT to HTTP",
                "expected_type": "GW",
                "expected_success": True,
                "category": "IoT_Gateway",
                "description": "IoT Gateway Configuration"
            },
            {
                "requirement": "Set up edge gateway, device ID edge_01, device discovery enabled, firmware update support",
                "expected_type": "GW",
                "expected_success": True,
                "category": "Edge_Gateway",
                "description": "Edge Gateway with Management"
            },
            {
                "requirement": "Configure gateway but missing device management capabilities",
                "expected_type": "GW",
                "expected_success": False,
                "category": "Incomplete_Gateway",
                "description": "Incomplete Gateway Configuration"
            },
            
            # ===== COMMUNICATION PROTOCOL (CP) TESTS =====
            {
                "requirement": "Configure MQTT client to connect to mqtt.example.com, port 1883, topic sensors/temperature, QoS 1",
                "expected_type": "CP",
                "expected_success": True,
                "category": "MQTT_Standard",
                "description": "Standard MQTT Client Configuration"
            },
            {
                "requirement": "Set up MQTT broker at broker.hivemq.com, port 8883, use TLS encryption, topic device/status",
                "expected_type": "CP", 
                "expected_success": True,
                "category": "MQTT_TLS",
                "description": "TLS Encrypted MQTT Configuration"
            },
            {
                "requirement": "Configure a TCP server listening on port 8080, allow max 100 concurrent connections",
                "expected_type": "CP",
                "expected_success": True,
                "category": "TCP_Server",
                "description": "TCP Server Configuration"
            },
            {
                "requirement": "Set up UDP client, target address 192.168.1.100, port 5000",
                "expected_type": "CP",
                "expected_success": True,
                "category": "UDP_Client",
                "description": "UDP Client Configuration"
            },
            {
                "requirement": "Configure a non-existent protocol xyz://example.com",
                "expected_type": "CP",
                "expected_success": False,
                "category": "Invalid_Protocol",
                "description": "Invalid Protocol Configuration"
            },
            
            # ===== SECURITY CONFIGURATION (SC) TESTS =====
            {
                "requirement": "Configure device authentication using username/password, enable TLS encryption",
                "expected_type": "SC",
                "expected_success": True,
                "category": "Auth_Encryption",
                "description": "Authentication and Encryption"
            },
            {
                "requirement": "Set up certificate-based authentication, AES-256 encryption, access control list",
                "expected_type": "SC",
                "expected_success": True,
                "category": "Certificate_Auth",
                "description": "Certificate-based Security"
            },
            {
                "requirement": "Configure JWT token authentication, OAuth 2.0 authorization",
                "expected_type": "SC",
                "expected_success": True,
                "category": "JWT_OAuth",
                "description": "JWT and OAuth Security"
            },
            {
                "requirement": "Set up security but no authentication method specified",
                "expected_type": "SC",
                "expected_success": False,
                "category": "Incomplete_Security",
                "description": "Incomplete Security Configuration"
            }
        ]
    
    def run_single_test(self, test_case, test_id):
        """
        Execute a single test case and collect performance metrics.
        
        Args:
            test_case (dict): Test case configuration with requirements and expectations
            test_id (str): Unique identifier for the test case
            
        Returns:
            dict: Test results including performance metrics and validation outcomes
        """
        try:
            start_time = time.time()
            
            # Retrieve current IoT topology status
            topology_response = requests.get("http://127.0.0.1:5000/topology")
            topology_status = topology_response.json()
            
            # Prepare translation prompt with topology context
            translator_prompt_full = self.translator_prompt + str(topology_status) + "\n Use this information to gather relevant IoT information for the {requirements} goal. You are not authorized to make explanations of any type."
            
            # Step 1: Translate natural language requirement to configuration type
            translate_start = time.time()
            try:
                trad = ollama.chat(
                    model=self.model_name,
                    messages=[
                        {'role': 'system', 'content': translator_prompt_full}, 
                        {'role': 'user', 'content': test_case["requirement"]}
                    ],
                    options={'timeout': 30}  # 30 second timeout
                )
            except Exception as e:
                print(f"Translation timeout/error: {e}")
                trad = {'message': {'content': 'type: CP\nsteps:\n1. Error in translation'}}
            translate_time = time.time() - translate_start
            
            trad_response = trad['message']['content']
            
            # Extract and validate verification type from response
            verification_type = trad_response[:2].strip()
            valid_types = ['SD', 'AD', 'GW', 'CP', 'SC']
            if verification_type not in valid_types:
                for vtype in valid_types:
                    if vtype in trad_response:
                        verification_type = vtype
                        break
                else:
                    verification_type = "CP"  # Default fallback
            
            # Step 2: Generate specific configuration based on translated type
            config_start = time.time()
            try:
                config = ollama.chat(
                    model=self.model_name,
                    messages=[
                        {'role': 'system', 'content': self.configurator_prompt}, 
                        {'role': 'user', 'content': trad_response}
                    ],
                    options={'timeout': 60}  # 60 second timeout
                )
            except Exception as e:
                print(f"Config generation timeout/error: {e}")
                config = {'message': {'content': '<No Configuration Requirements>'}}
            config_time = time.time() - config_start
            
            config_response = config['message']['content']
            
            # Step 3: Validate generated configuration using IoT verifier
            verify_start = time.time()
            verify_payload = {
                "verification_type": verification_type,
                "commands": config_response
            }
            
            verify_response = requests.post("http://127.0.0.1:5000/verify", json=verify_payload)
            verify_result = verify_response.json()
            verify_time = time.time() - verify_start
            
            total_time = time.time() - start_time
            
            # Analyze test results and calculate accuracy metrics
            verification_success = verify_result.get("result") == "Successful"
            expected_success = test_case["expected_success"]
            
            result = {
                "test_id": test_id,
                "requirement": test_case["requirement"],
                "description": test_case["description"],
                "category": test_case["category"],
                "expected_type": test_case["expected_type"],
                "expected_success": expected_success,
                
                "translated_type": verification_type,
                "translated_response": trad_response,
                "translate_time": translate_time,
                
                "config_response": config_response,
                "config_time": config_time,
                
                "verification_result": verify_result.get("result"),
                "verification_success": verification_success,
                "verify_time": verify_time,
                "total_time": total_time,
                
                "type_accuracy": verification_type == test_case["expected_type"],
                "success_accuracy": verification_success == expected_success,
                
                "timestamp": datetime.now().isoformat(),
                "errors": verify_result.get("errors", [])
            }
            
            return result
            
        except Exception as e:
            return {
                "test_id": test_id,
                "requirement": test_case["requirement"],
                "description": test_case["description"],
                "category": test_case["category"],
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "translate_success": False,
                "verification_success": False,
                "type_accuracy": False,
                "success_accuracy": False
            }
    
    def run_enhanced_tests(self, iterations=3):
        """
        Execute comprehensive test suite covering all 5 verification types.
        
        Args:
            iterations (int): Number of test iterations to run
            
        Returns:
            list: Complete test results with performance metrics
        """
        print("=" * 80)
        print("Enhanced Performance Data Collection Test")
        print("=" * 80)
        print(f"Model: {self.model_name}")
        print(f"Test Cases: {len(self.get_enhanced_test_cases())}")
        print(f"Iterations: {iterations}")
        print(f"Total Tests: {len(self.get_enhanced_test_cases()) * iterations}")
        print("=" * 80)
        
        test_cases = self.get_enhanced_test_cases()
        
        for iteration in range(iterations):
            print(f"\nIteration {iteration + 1}")
            print("-" * 40)
            
            for i, test_case in enumerate(test_cases):
                test_id = f"iter_{iteration+1}_test_{i+1}"
                print(f"  {test_case['description']} [{test_case['expected_type']}]")
                print(f"     Requirement: {test_case['requirement'][:60]}...")
                
                result = self.run_single_test(test_case, test_id)
                self.results.append(result)
                
                # Show results
                if result.get("error"):
                    print(f"     ERROR: {result['error']}")
                else:
                    type_acc = "PASS" if result["type_accuracy"] else "FAIL"
                    success_acc = "PASS" if result["success_accuracy"] else "FAIL"
                    print(f"     {type_acc} Type Recognition | {success_acc} Verification | Time: {result['total_time']:.1f}s")
        
        print(f"\nTest completed! Total tests: {len(self.results)}")
        return self.results
    
    def generate_enhanced_statistics(self):
        """
        Generate comprehensive statistics report from test results.
        
        Returns:
            dict: Statistical analysis including accuracy metrics and performance data
        """
        if not self.results:
            print("No test results to analyze")
            return
        
        print("\n" + "=" * 80)
        print("Performance Statistics Report")
        print("=" * 80)
        
        # Basic statistics
        total_tests = len(self.results)
        successful_tests = len([r for r in self.results if not r.get("error")])
        failed_tests = total_tests - successful_tests
        
        print(f"Basic Statistics:")
        print(f"   Total Tests: {total_tests}")
        print(f"   Successful Tests: {successful_tests} ({successful_tests/total_tests*100:.1f}%)")
        print(f"   Failed Tests: {failed_tests} ({failed_tests/total_tests*100:.1f}%)")
        
        if successful_tests == 0:
            print("No successful test cases")
            return
        
        # Accuracy statistics
        type_accurate = len([r for r in self.results if r.get("type_accuracy")])
        success_accurate = len([r for r in self.results if r.get("success_accuracy")])
        
        print(f"\nAccuracy Statistics:")
        print(f"   Type Recognition Accuracy: {type_accurate}/{total_tests} ({type_accurate/total_tests*100:.1f}%)")
        print(f"   Verification Result Accuracy: {success_accurate}/{total_tests} ({success_accurate/total_tests*100:.1f}%)")
        
        # Time statistics
        times = [r["total_time"] for r in self.results if r.get("total_time")]
        if times:
            avg_time = sum(times) / len(times)
            min_time = min(times)
            max_time = max(times)
            print(f"\nTime Statistics:")
            print(f"   Average Response Time: {avg_time:.2f} seconds")
            print(f"   Minimum Response Time: {min_time:.2f} seconds")
            print(f"   Maximum Response Time: {max_time:.2f} seconds")
        
        # Verification type statistics
        type_stats = {}
        for result in self.results:
            expected_type = result.get("expected_type", "Unknown")
            if expected_type not in type_stats:
                type_stats[expected_type] = {"total": 0, "success": 0, "type_acc": 0, "success_acc": 0}
            
            type_stats[expected_type]["total"] += 1
            if not result.get("error"):
                type_stats[expected_type]["success"] += 1
            if result.get("type_accuracy"):
                type_stats[expected_type]["type_acc"] += 1
            if result.get("success_accuracy"):
                type_stats[expected_type]["success_acc"] += 1
        
        print(f"\nVerification Type Statistics:")
        for vtype, stats in type_stats.items():
            total = stats["total"]
            success_rate = stats["success"] / total * 100 if total > 0 else 0
            type_acc_rate = stats["type_acc"] / total * 100 if total > 0 else 0
            success_acc_rate = stats["success_acc"] / total * 100 if total > 0 else 0
            
            print(f"   {vtype} ({self.get_type_name(vtype)}):")
            print(f"     Tests: {total} | Success Rate: {success_rate:.1f}%")
            print(f"     Type Accuracy: {type_acc_rate:.1f}% | Verification Accuracy: {success_acc_rate:.1f}%")
        
        return {
            "total_tests": total_tests,
            "successful_tests": successful_tests,
            "type_accuracy": type_accurate / total_tests * 100,
            "success_accuracy": success_accurate / total_tests * 100,
            "avg_response_time": avg_time if times else 0,
            "type_stats": type_stats
        }
    
    def get_type_name(self, vtype):
        """
        Get full descriptive name for verification type abbreviation.
        
        Args:
            vtype (str): Verification type abbreviation (SD, AD, GW, CP, SC)
            
        Returns:
            str: Full descriptive name of the verification type
        """
        type_names = {
            "SD": "Sensor Device",
            "AD": "Actuator Device", 
            "GW": "Gateway",
            "CP": "Communication Protocol",
            "SC": "Security Configuration"
        }
        return type_names.get(vtype, "Unknown")
    
    def save_enhanced_data(self):
        """
        Save test results to JSON and CSV files with timestamp.
        
        Returns:
            tuple: Paths to saved JSON and CSV files
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save detailed results
        json_file = f"enhanced_test_results_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        
        # Save CSV report
        csv_file = f"enhanced_test_report_{timestamp}.csv"
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                "Test ID", "Category", "Description", "Requirement", "Expected Type", "Expected Success",
                "Recognized Type", "Type Accuracy", "Verification Result", "Verification Accuracy",
                "Total Time", "Translate Time", "Config Time", "Verify Time", "Errors", "Timestamp"
            ])
            
            for result in self.results:
                writer.writerow([
                    result.get("test_id", ""),
                    result.get("category", ""),
                    result.get("description", ""),
                    result.get("requirement", ""),
                    result.get("expected_type", ""),
                    result.get("expected_success", ""),
                    result.get("translated_type", ""),
                    result.get("type_accuracy", False),
                    result.get("verification_result", ""),
                    result.get("success_accuracy", False),
                    result.get("total_time", 0),
                    result.get("translate_time", 0),
                    result.get("config_time", 0),
                    result.get("verify_time", 0),
                    "; ".join(result.get("errors", [])),
                    result.get("timestamp", "")
                ])
        
        print(f"\nData saved:")
        print(f"   Detailed Results: {json_file}")
        print(f"   CSV Report: {csv_file}")
        
        return json_file, csv_file

def main():
    """
    Main function to execute the performance data collection process.
    Handles environment checks, test execution, and result generation.
    """
    print("Starting Enhanced Performance Data Collection")
    
    # Check environment
    print("\nChecking environment...")
    
    # Check Ollama
    try:
        models = ollama.list()
        print(f"Ollama available, models: {[m['name'] for m in models['models']]}")
    except Exception as e:
        print(f"Ollama error: {e}")
        print("Please ensure Ollama service is running")
        return
    
    # Check IoT verifier
    try:
        response = requests.get("http://127.0.0.1:5000/health", timeout=5)
        if response.status_code != 200:
            print("IoT verifier status abnormal")
            return
        print("IoT verifier running normally")
    except:
        print("Cannot connect to IoT verifier http://127.0.0.1:5000")
        print("Please run: python IoT_Request.py")
        return
    
    # Create enhanced data collector
    collector = EnhancedPerformanceDataCollector()
    
    # Run tests
    print(f"\nEstimated runtime: 75-150 minutes")
    print("Starting enhanced tests...")
    
    results = collector.run_enhanced_tests(iterations=5)
    
    # Generate statistics report
    stats = collector.generate_enhanced_statistics()
    
    # Save data
    json_file, csv_file = collector.save_enhanced_data()
    
    # Performance summary
    print(f"\nPerformance Summary:")
    print(f"We conducted comprehensive performance evaluation with {stats['total_tests']} test cases,")
    print(f"covering all 5 verification types: Sensor Device (SD), Actuator Device (AD), Gateway (GW),")
    print(f"Communication Protocol (CP), and Security Configuration (SC). Test results show,")
    print(f"the framework achieved {stats['type_accuracy']:.1f}% accuracy in type recognition tasks,")
    print(f"and {stats['success_accuracy']:.1f}% accuracy in configuration verification tasks,")
    print(f"with an average response time of {stats['avg_response_time']:.2f} seconds.")
    
    if stats['success_accuracy'] >= 90:
        print("This indicates excellent performance and reliability across all IoT configuration verification tasks.")
    elif stats['success_accuracy'] >= 80:
        print("This indicates good performance and reliability across all IoT configuration verification tasks.")
    else:
        print("This indicates that the framework needs further improvement in IoT configuration verification tasks.")

if __name__ == "__main__":
    main()

