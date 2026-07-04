# Nginx Reverse Proxy Configuration

## Architecture

Nginx serves as the single entry point for the entire LAWIM platform:

```
Internet Traffic (HTTP/HTTPS)
         ↓
    Nginx Proxy
    (Port 80/443)
         ↓
    ┌────────┴────────┬────────────┬────────────┐
    │                 │            │            │
Frontend          Backend        Brain       Knowledge
(React SPA)       (FastAPI)     (Intent)     (Search)
```

## Configuration Files

### `/deployment/nginx/nginx.conf` (Main Configuration)

- Worker processes: Auto (match CPU cores)
- Worker connections: 2048 per process
- Gzip compression: Enabled for text/JSON
- SSL session caching: 10 minutes
- Rate limiting zones: General (10 req/s), API (100 req/s), Auth (5 req/min)
- Proxy cache paths: Static assets (60 days), API responses (10 minutes)
- Upstream load balancing: Least connections algorithm

### `/deployment/nginx/conf.d/production.conf` (Production Server Block)

**Security Headers:**
```
Strict-Transport-Security: 1 year HSTS
X-Frame-Options: SAMEORIGIN
X-Content-Type-Options: nosniff
X-XSS-Protection: enabled
Content-Security-Policy: Restrictive
```

**SSL/TLS:**
- Protocols: TLSv1.2, TLSv1.3 only
- Ciphers: HIGH:!aNULL:!MD5
- Session cache: 10 minutes
- Prefer server ciphers: enabled

**Routing:**
- Static assets: Cached for 30 days
- Frontend SPA: Proxies to React app on port 3000
- API: Proxies backend on port 8000 with 1 minute cache
- Brain/Agents/Knowledge: Proxies to microservices
- WebSocket: Supports ws:// protocol
- Authentication: Stricter rate limiting (5 req/min)

**Rate Limiting:**
```
- General endpoints: 10 requests/second
- API endpoints: 100 requests/second
- Authentication: 5 requests/minute
- Burst allowed: 50 extra requests
```

**Caching:**
- Static assets: 30-day cache (immutable)
- API responses: 1 minute cache with stale-on-error fallback
- Cache key: Request URI + method

## Proxying Backends

### Frontend Proxying

```nginx
location / {
    proxy_pass http://frontend_upstream;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    # SPA routing: serve index.html for 404
    error_page 404 =200 /index.html;
}
```

### API Proxying

```nginx
location /api/ {
    proxy_cache api_cache;
    proxy_cache_valid 200 1m;
    proxy_pass http://backend_upstream;
    proxy_http_version 1.1;
    proxy_set_header Connection "";
    # Connection pooling
    keepalive 32;
}
```

### WebSocket Support

```nginx
location /ws/ {
    proxy_pass http://backend_upstream;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_read_timeout 3600s;
    proxy_send_timeout 3600s;
}
```

## Performance Optimization

### Compression

- **Enabled**: gzip compression for text/HTML/JSON
- **Level**: 6 (good balance between speed and ratio)
- **Types**: text/plain, text/css, text/xml, application/json, etc.

### Caching

```nginx
proxy_cache_path /var/cache/nginx/static
    levels=1:2
    keys_zone=static:10m
    max_size=1g
    inactive=60m
    use_temp_path=off;
```

### Connection Pooling

```nginx
proxy_http_version 1.1;
proxy_set_header Connection "";
keepalive 32;
```

## SSL/TLS Setup

### Self-Signed Certificate (Development)

```bash
openssl req -x509 -newkey rsa:4096 -keyout lawim.key -out lawim.crt -days 365 -nodes
cp lawim.{crt,key} deployment/nginx/ssl/
```

### Let's Encrypt Certificate (Production)

```bash
# Using Certbot
certbot certonly --manual --preferred-challenges=http -d lawim.app

# Copy certificates
cp /etc/letsencrypt/live/lawim.app/fullchain.pem deployment/nginx/ssl/lawim.crt
cp /etc/letsencrypt/live/lawim.app/privkey.pem deployment/nginx/ssl/lawim.key
```

## Monitoring

### Access Logs

```
/var/log/nginx/access.log
Format: IP, User, Time, Request, Status, Bytes, Referer, User-Agent
```

### Error Logs

```
/var/log/nginx/error.log
Details: Errors, warnings, notices
```

### Health Monitoring

```bash
# Check Nginx status
curl http://localhost/health

# Monitor active connections
watch 'ss -tan | grep ESTABLISHED | wc -l'

# Check cache hit rate
tail -f /var/log/nginx/access.log | grep X-Cache-Status
```

## Troubleshooting

### High Error Rates

1. Check upstream service health: `docker-compose ps`
2. Review backend logs: `docker-compose logs backend`
3. Check rate limiting: `grep "limiting requests" /var/log/nginx/error.log`

### Slow Response Times

1. Monitor cache hit rate: Review X-Cache-Status header
2. Check backend response time: Review proxy_connect_timeout
3. Monitor active connections: `netstat -an | grep ESTABLISHED | wc -l`

### SSL/TLS Issues

1. Verify certificate: `openssl x509 -in lawim.crt -text`
2. Check expiration: `openssl x509 -in lawim.crt -noout -enddate`
3. Test connection: `openssl s_client -connect lawim.app:443`

## Best Practices

1. **Always use HTTPS in production**
2. **Keep security headers up to date**
3. **Monitor cache hit ratios**
4. **Implement proper rate limiting**
5. **Use connection pooling**
6. **Regular certificate renewal**
7. **Monitor error logs**
8. **Test configuration changes**
