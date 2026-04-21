// Source: NEW - Tools API Client
// CORTEX MODIFICATION: API client for tools/skills management

interface Tool {
  name: string;
  description: string;
  status: string;
  last_used?: string;
}

interface ApiResponse<T = any> {
  status: 'ok' | 'error';
  data?: T;
  error?: string;
}

class ToolsClient {
  private baseUrl: string;

  constructor(baseUrl: string = '/api/cortex') {
    this.baseUrl = baseUrl;
  }

  async list(): Promise<ApiResponse<Tool[]>> {
    try {
      const response = await fetch(`${this.baseUrl}/tools/list`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
      });
      return response.json();
    } catch (error) {
      return {
        status: 'error',
        error: error instanceof Error ? error.message : 'Unknown error'
      };
    }
  }

  async execute(
    toolName: string,
    params: Record<string, any> = {}
  ): Promise<ApiResponse<any>> {
    try {
      const response = await fetch(`${this.baseUrl}/tools/execute`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ tool: toolName, params })
      });
      return response.json();
    } catch (error) {
      return {
        status: 'error',
        error: error instanceof Error ? error.message : 'Unknown error'
      };
    }
  }

  async getStatus(toolName: string): Promise<ApiResponse<{ status: string }>> {
    try {
      const response = await fetch(`${this.baseUrl}/tools/status/${toolName}`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
      });
      return response.json();
    } catch (error) {
      return {
        status: 'error',
        error: error instanceof Error ? error.message : 'Unknown error'
      };
    }
  }
}

export const toolsClient = new ToolsClient();
