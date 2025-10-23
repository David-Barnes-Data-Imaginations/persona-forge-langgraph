#!/usr/bin/env python3
"""
Test script to verify remote model configuration

This script tests that:
1. SSH tunnel to mini-itx is working
2. Local models are accessible
3. Remote scribe model is accessible
4. All models in the deep_agent workflow are configured correctly
"""
from src.io_py.edge.ssh_tunnel import SSHTunnel
from src.io_py.edge.config import MINI_SSH_CONFIG, LLMConfigScribe, LLMConfigPeon, LLMConfigOverseer


def test_tunnel():
    """Test SSH tunnel connectivity"""
    print("=" * 60)
    print("Testing SSH Tunnel to Mini-ITX")
    print("=" * 60)

    tunnel = SSHTunnel(
        host=MINI_SSH_CONFIG["host"],
        user=MINI_SSH_CONFIG["user"],
        local_port=MINI_SSH_CONFIG["local_port"],
        remote_port=MINI_SSH_CONFIG["remote_port"]
    )

    if tunnel.is_running():
        print("✅ SSH tunnel is running")
        print(f"   Port: {MINI_SSH_CONFIG['local_port']}")
        print(f"   Target: {MINI_SSH_CONFIG['host']}:{MINI_SSH_CONFIG['remote_port']}")
    else:
        print("❌ SSH tunnel is not running")
        print("   Starting tunnel...")
        tunnel.start()

    # Test connectivity
    import requests
    try:
        response = requests.get(f"http://localhost:{MINI_SSH_CONFIG['local_port']}/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json()['models']
            print(f"✅ Connected to mini-itx Ollama")
            print(f"   Available models: {len(models)}")
            for model in models:
                print(f"      - {model['name']}")
        else:
            print(f"⚠️  Unexpected response: {response.status_code}")
    except Exception as e:
        print(f"❌ Failed to connect: {e}")


def test_local_models():
    """Test local model configuration"""
    print("\n" + "=" * 60)
    print("Testing Local Models (Main PC)")
    print("=" * 60)

    from langchain_openai import ChatOpenAI

    # Test peon model
    print(f"\nTesting Peon model: {LLMConfigPeon.model_name}")
    try:
        peon = ChatOpenAI(
            model=LLMConfigPeon.model_name,
            temperature=0.0,
            base_url="http://localhost:1234/v1",
            api_key="lm-studio"
        )
        response = peon.invoke("Say 'test' in one word")
        print(f"✅ Peon model working: {response.content[:50]}")
    except Exception as e:
        print(f"❌ Peon model failed: {e}")

    # Test overseer model
    print(f"\nTesting Overseer model: {LLMConfigOverseer.model_name}")
    try:
        overseer = ChatOpenAI(
            model=LLMConfigOverseer.model_name,
            temperature=0.0,
            base_url="http://localhost:1234/v1",
            api_key="lm-studio"
        )
        response = overseer.invoke("Say 'test' in one word")
        print(f"✅ Overseer model working: {response.content[:50]}")
    except Exception as e:
        print(f"❌ Overseer model failed: {e}")


def test_remote_model():
    """Test remote scribe model"""
    print("\n" + "=" * 60)
    print("Testing Remote Model (Mini-ITX)")
    print("=" * 60)

    from langchain_openai import ChatOpenAI

    print(f"\nTesting Scribe model: {LLMConfigScribe.model_name}")
    print(f"Remote execution: {LLMConfigScribe.use_remote}")
    print(f"Remote port: {LLMConfigScribe.remote_port}")

    try:
        scribe = ChatOpenAI(
            model=LLMConfigScribe.model_name,
            temperature=0.0,
            base_url=f"http://localhost:{LLMConfigScribe.remote_port}/v1",
            api_key="lm-studio"
        )
        response = scribe.invoke("Say 'test' in one word")
        print(f"✅ Scribe model working: {response.content[:50]}")
        print(f"✅ Remote execution successful!")
    except Exception as e:
        print(f"❌ Scribe model failed: {e}")


def test_deep_agent_import():
    """Test that deep_agent loads correctly with remote config"""
    print("\n" + "=" * 60)
    print("Testing Deep Agent Import")
    print("=" * 60)

    try:
        from src.graphs.deep_agent import scribe_model, alt_model, overseer_model
        print("✅ Deep agent imported successfully")
        print(f"   - Alt model: {alt_model}")
        print(f"   - Overseer model: {overseer_model}")
        print(f"   - Scribe model: {scribe_model}")

        # Test scribe model from deep_agent
        print("\nTesting scribe model from deep_agent...")
        response = scribe_model.invoke("Say 'hello' in one word")
        print(f"✅ Scribe model response: {response.content[:50]}")

    except Exception as e:
        print(f"❌ Deep agent import failed: {e}")
        import traceback
        traceback.print_exc()


def main():
    print("\n" + "=" * 60)
    print("REMOTE MODEL CONFIGURATION TEST")
    print("=" * 60 + "\n")

    test_tunnel()
    test_local_models()
    test_remote_model()
    test_deep_agent_import()

    print("\n" + "=" * 60)
    print("Test Complete")
    print("=" * 60)


if __name__ == "__main__":
    main()
