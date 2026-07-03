export interface AuthUser {
  id: string;
  email: string;
  role: 'admin' | 'operator' | 'viewer';
}

export function getUserDisplayName(user: AuthUser) {
  return user.email.split('@')[0];
}
