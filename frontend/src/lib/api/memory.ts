// Source: NEW - Memory API Client
// CORTEX MODIFICATION: API client for memory management

interface MemoryEntry {
  id?: number;
  category: string;
  title: string;
  content: string;
  importance: number;
  date: string;
  status: string;
}

interface ApiResponse<T = any> {
  status: 'ok' | 'error';
  data?: T;
  error?: string;
}

class MemoryClient {
  private baseUrl: string;

  constructor(baseUrl: string = '/api/cortex') {
    this.baseUrl = baseUrl;
  }

  async list(): Promise<ApiResponse<MemoryEntry[]>> {
    try {
      const response = await fetch(`${this.baseUrl}/memory/list`, {
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

  async search(query: string): Promise<ApiResponse<MemoryEntry[]>> {
    try {
      const response = await fetch(`${this.baseUrl}/memory/search`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query })
      });
      return response.json();
    } catch (error) {
      return {
        status: 'error',
        error: error instanceof Error ? error.message : 'Unknown error'
      };
    }
  }

  async add(entry: Omit<MemoryEntry, 'id' | 'date'>): Promise<ApiResponse<MemoryEntry>> {
    try {
      const response = await fetch(`${this.baseUrl}/memory/add`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(entry)
      });
      return response.json();
    } catch (error) {
      return {
        status: 'error',
        error: error instanceof Error ? error.message : 'Unknown error'
      };
    }
  }

  async promote(id: number): Promise<ApiResponse<void>> {
    try {
      const response = await fetch(`${this.baseUrl}/memory/promote/${id}`, {
        method: 'POST',
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

  async delete(id: number): Promise<ApiResponse<void>> {
    try {
      const response = await fetch(`${this.baseUrl}/memory/delete/${id}`, {
        method: 'DELETE',
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

export const memoryClient = new MemoryClient();
