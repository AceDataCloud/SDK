/** OAuth 2.0 client helpers for "Sign in with Ace Data Cloud". */

const AUTH_BASE = 'https://auth.acedata.cloud';

export interface OAuthTokenResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
  scope: string;
  refresh_token?: string;
}

export interface OAuthUserInfo {
  id: string;
  username?: string;
  nickname?: string;
  avatar?: string;
  is_verified?: boolean;
  date_joined?: string;
  email?: string;
  phone?: string;
  region?: string;
}

export interface BuildAuthorizationUrlParams {
  clientId: string;
  redirectUri: string;
  scope: string;
  state: string;
  codeChallenge?: string;
  codeChallengeMethod?: 'S256' | 'plain';
  responseType?: string;
}

export interface ExchangeCodeParams {
  clientId: string;
  code: string;
  redirectUri: string;
  clientSecret?: string;
  codeVerifier?: string;
}

export interface RefreshTokenParams {
  refreshToken: string;
  clientId?: string;
  clientSecret?: string;
}

export interface RevokeTokenParams {
  token: string;
  clientId?: string;
  clientSecret?: string;
}

async function checkResponse(resp: Response): Promise<void> {
  if (!resp.ok) {
    const text = await resp.text();
    let message = text;
    try {
      const body = JSON.parse(text) as Record<string, unknown>;
      if (typeof body.error_description === 'string') message = body.error_description;
      else if (typeof body.error === 'string') message = body.error;
    } catch {
      // use raw text as message
    }
    throw new Error(`OAuth request failed (${resp.status}): ${message}`);
  }
}

export class OAuth {
  private authBaseURL: string;

  constructor(authBaseURL?: string) {
    let base = authBaseURL ?? AUTH_BASE;
    while (base.endsWith('/')) base = base.slice(0, -1);
    this.authBaseURL = base;
  }

  buildAuthorizationUrl(params: BuildAuthorizationUrlParams): string {
    const urlParams = new URLSearchParams({
      response_type: params.responseType ?? 'code',
      client_id: params.clientId,
      redirect_uri: params.redirectUri,
      scope: params.scope,
      state: params.state,
    });
    if (params.codeChallenge) {
      urlParams.set('code_challenge', params.codeChallenge);
      urlParams.set('code_challenge_method', params.codeChallengeMethod ?? 'S256');
    }
    return `${this.authBaseURL}/oauth2/authorize?${urlParams.toString()}`;
  }

  async discover(): Promise<Record<string, unknown>> {
    const resp = await fetch(`${this.authBaseURL}/.well-known/oauth-authorization-server`);
    await checkResponse(resp);
    return (await resp.json()) as Record<string, unknown>;
  }

  async exchangeCode(params: ExchangeCodeParams): Promise<OAuthTokenResponse> {
    const body = new URLSearchParams({
      grant_type: 'authorization_code',
      code: params.code,
      client_id: params.clientId,
      redirect_uri: params.redirectUri,
    });
    if (params.clientSecret) body.set('client_secret', params.clientSecret);
    if (params.codeVerifier) body.set('code_verifier', params.codeVerifier);

    const resp = await fetch(`${this.authBaseURL}/oauth2/token`, {
      method: 'POST',
      headers: { 'content-type': 'application/x-www-form-urlencoded' },
      body: body.toString(),
    });
    await checkResponse(resp);
    return (await resp.json()) as OAuthTokenResponse;
  }

  async refreshToken(params: RefreshTokenParams): Promise<OAuthTokenResponse> {
    const body = new URLSearchParams({
      grant_type: 'refresh_token',
      refresh_token: params.refreshToken,
    });
    if (params.clientId) body.set('client_id', params.clientId);
    if (params.clientSecret) body.set('client_secret', params.clientSecret);

    const resp = await fetch(`${this.authBaseURL}/oauth2/token`, {
      method: 'POST',
      headers: { 'content-type': 'application/x-www-form-urlencoded' },
      body: body.toString(),
    });
    await checkResponse(resp);
    return (await resp.json()) as OAuthTokenResponse;
  }

  async revokeToken(params: RevokeTokenParams): Promise<void> {
    const body = new URLSearchParams({ token: params.token });
    if (params.clientId) body.set('client_id', params.clientId);
    if (params.clientSecret) body.set('client_secret', params.clientSecret);

    const resp = await fetch(`${this.authBaseURL}/oauth2/revoke`, {
      method: 'POST',
      headers: { 'content-type': 'application/x-www-form-urlencoded' },
      body: body.toString(),
    });
    await checkResponse(resp);
  }

  async getUserInfo(accessToken: string): Promise<OAuthUserInfo> {
    const resp = await fetch(`${this.authBaseURL}/api/v1/users/me`, {
      headers: { authorization: 'Bearer ' + accessToken },
    });
    await checkResponse(resp);
    return (await resp.json()) as OAuthUserInfo;
  }
}
