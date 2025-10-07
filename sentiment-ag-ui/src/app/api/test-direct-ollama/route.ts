import { NextRequest, NextResponse } from 'next/server';

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    
    // Make direct fetch call to Ollama using exact same config as your AI Toolkit
    const response = await fetch('http://127.0.0.1:11434/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer unused'
      },
      body: JSON.stringify({
        model: 'gpt-oss:20b',
        messages: body.messages || [{ role: 'user', content: 'Hello from direct test' }],
        max_tokens: 100
      })
    });

    if (!response.ok) {
      const errorText = await response.text();
      return NextResponse.json({ 
        success: false, 
        error: `HTTP ${response.status}: ${errorText}` 
      }, { status: response.status });
    }

    const data = await response.json();
    return NextResponse.json({ 
      success: true, 
      message: 'Direct Ollama connection successful!',
      response: data
    });

  } catch (error) {
    return NextResponse.json({ 
      success: false, 
      error: `Connection failed: ${error}` 
    }, { status: 500 });
  }
}
