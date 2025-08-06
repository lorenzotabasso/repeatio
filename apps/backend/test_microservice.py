#!/usr/bin/env python3
"""
Test script for the Audio Microservice
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_supported_languages():
    """Test supported languages endpoint"""
    print("\nTesting supported languages endpoint...")
    response = requests.get(f"{BASE_URL}/api/v1/audio/supported-languages")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_text_to_audio():
    """Test text to audio conversion"""
    print("\nTesting text to audio conversion...")
    
    payload = {
        "text": "Hello, this is a test message in English",
        "language": "en",
        "output_filename": "test_hello.mp3"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/v1/audio/text-to-audio",
        json=payload
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_list_files():
    """Test listing audio files"""
    print("\nTesting list files endpoint...")
    response = requests.get(f"{BASE_URL}/api/v1/audio/files")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def main():
    """Run all tests"""
    print("Starting Audio Microservice Tests...")
    print("=" * 50)
    
    tests = [
        ("Health Check", test_health),
        ("Supported Languages", test_supported_languages),
        ("Text to Audio", test_text_to_audio),
        ("List Files", test_list_files),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except requests.exceptions.ConnectionError:
            print(f"❌ {test_name}: Connection failed - Is the service running?")
            results.append((test_name, False))
        except Exception as e:
            print(f"❌ {test_name}: Error - {str(e)}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("Test Results:")
    print("=" * 50)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    print(f"\nSummary: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The microservice is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the service logs for details.")

if __name__ == "__main__":
    main() 