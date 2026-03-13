const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export interface InteractionInput {
    session_id: string;
    user_input: string;
    user_name?: string;
    script_name?: string;
}

export async function processMessage(data: InteractionInput) {
    const response = await fetch(`${API_BASE_URL}/process-message`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    });

    if (!response.ok) {
        throw new Error('Failed to process message');
    }

    return response.json();
}

export async function fetchScripts() {
    const response = await fetch(`${API_BASE_URL}/scripts`);
    if (!response.ok) {
        throw new Error('Failed to fetch scripts');
    }
    return response.json();
}

export async function fetchScriptDetails(scriptId: string) {
    const response = await fetch(`${API_BASE_URL}/scripts/${scriptId}`);
    if (!response.ok) {
        throw new Error('Failed to fetch script details');
    }
    return response.json();
}
