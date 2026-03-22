/** Management-plane resources. */

import { Transport } from '../runtime/transport';

class Applications {
  constructor(private transport: Transport) {}

  async list(params?: Record<string, string>): Promise<Record<string, unknown>> {
    return this.transport.request('GET', '/api/v1/applications/', { params, platform: true });
  }

  async create(opts: { serviceId: string; [key: string]: unknown }): Promise<Record<string, unknown>> {
    const { serviceId, ...rest } = opts;
    return this.transport.request('POST', '/api/v1/applications/', {
      json: { service_id: serviceId, ...rest },
      platform: true,
    });
  }

  async get(applicationId: string): Promise<Record<string, unknown>> {
    return this.transport.request('GET', `/api/v1/applications/${applicationId}/`, { platform: true });
  }
}

class Credentials {
  constructor(private transport: Transport) {}

  async list(params?: Record<string, string>): Promise<Record<string, unknown>> {
    return this.transport.request('GET', '/api/v1/credentials/', { params, platform: true });
  }

  async create(opts: { applicationId: string; [key: string]: unknown }): Promise<Record<string, unknown>> {
    const { applicationId, ...rest } = opts;
    return this.transport.request('POST', '/api/v1/credentials/', {
      json: { application_id: applicationId, ...rest },
      platform: true,
    });
  }

  async rotate(credentialId: string): Promise<Record<string, unknown>> {
    return this.transport.request('POST', `/api/v1/credentials/${credentialId}/rotate/`, { platform: true });
  }

  async delete(credentialId: string): Promise<Record<string, unknown>> {
    return this.transport.request('DELETE', `/api/v1/credentials/${credentialId}/`, { platform: true });
  }
}

class Models {
  constructor(private transport: Transport) {}

  async list(params?: Record<string, string>): Promise<Record<string, unknown>> {
    return this.transport.request('GET', '/api/v1/models/', { params, platform: true });
  }
}

class Config {
  constructor(private transport: Transport) {}

  async get(): Promise<Record<string, unknown>> {
    return this.transport.request('GET', '/api/v1/config/', { platform: true });
  }
}

export class Platform {
  readonly applications: Applications;
  readonly credentials: Credentials;
  readonly models: Models;
  readonly config: Config;

  constructor(transport: Transport) {
    this.applications = new Applications(transport);
    this.credentials = new Credentials(transport);
    this.models = new Models(transport);
    this.config = new Config(transport);
  }
}
