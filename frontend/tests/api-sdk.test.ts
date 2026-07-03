import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { apiSdk } from '../packages/api-sdk/src';

describe('apiSdk', () => {
  beforeEach(() => {
    vi.unstubAllEnvs();
  });

  afterEach(() => {
    vi.unstubAllEnvs();
  });

  it('returns mock properties when mock mode is enabled', async () => {
    vi.stubEnv('VITE_LAWIM_USE_MOCKS', 'true');

    const response = await apiSdk.getProperties();

    expect(response.data.length).toBeGreaterThan(0);
    expect(response.data[0]).toHaveProperty('title');
  });
});
