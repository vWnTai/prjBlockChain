import { randomBytes } from 'node:crypto';
import { existsSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
const env = fileURLToPath(new URL('../.env', import.meta.url));
if (!existsSync(env)) {
  const keys = ['POSTGRES_PASSWORD','APP_DB_PASSWORD','EVALUATOR_DB_PASSWORD','SESSION_SECRET','ADMIN_PASSWORD','ANALYST_PASSWORD','VIEWER_PASSWORD'];
  writeFileSync(env, '# Generated local credentials. Never commit this file.\n' + keys.map(k => `${k}=${randomBytes(24).toString('hex')}`).join('\n') + '\nWEB_PORT=8080\nAPI_PORT=8000\nDB_PORT=5433\n', { flag:'wx', mode:0o600 });
  console.log('Created .env with random credentials. Local accounts: admin, analyst, viewer.');
} else console.log('Existing .env retained.');
