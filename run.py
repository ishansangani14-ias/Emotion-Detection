#!/usr/bin/env python3
"""
Quick start script for Adaptive Multimodal Emotion Detection System
"""
import os
import sys

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'flask',
        'tensorflow',
        'opencv-python',
        'scikit-learn',
        'numpy',
        'pandas'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing.append(package)
    
    if missing:
        print("❌ Missing required packages:")
        for pkg in missing:
            print(f"   - {pkg}")
        print("\n📦 Install them with:")
        print("   pip install -r requirements.txt")
        return False
    
    return True

def main():
    """Main entry point"""
    print("=" * 60)
    print("🎭 Adaptive Multimodal Emotion Detection System")
    print("=" * 60)
    print()
    
    # Check dependencies
    print("🔍 Checking dependencies...")
    if not check_dependencies():
        sys.exit(1)
    
    print("✅ All dependencies installed")
    print()
    
    # Import and run app
    print("🚀 Starting Flask application...")
    print("📍 Server will be available at: http://localhost:5000")
    print()
    print("⚠️  On first run, the system will:")
    print("   1. Generate synthetic training data")
    print("   2. Train CNN model (~5-10 minutes)")
    print("   3. Train text model (~30 seconds)")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    print()
    
    # Run the app
    from app import app, initialize_system
    initialize_system()
    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down gracefully...")
        sys.exit(0)
