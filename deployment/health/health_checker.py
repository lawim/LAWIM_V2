#!/usr/bin/env python3
"""
Health Check System for LAWIM V2
Validates all service dependencies and provides status reporting
"""

import os
import sys
import json
import asyncio
from typing import Dict, Any
from datetime import datetime
import asyncpg
import aioredis
import httpx


class HealthChecker:
    def __init__(self):
        self.results: Dict[str, Any] = {}
        self.start_time = datetime.now()

    async def check_database(self) -> Dict[str, Any]:
        """Check PostgreSQL database connectivity"""
        try:
            db_url = os.getenv(
                'DATABASE_URL',
                'postgresql://lawim:lawim_dev@postgres:5432/lawim_dev'
            )
            conn = await asyncpg.connect(db_url)
            version = await conn.fetchval('SELECT version()')
            await conn.close()
            return {
                'status': 'healthy',
                'message': 'PostgreSQL connected',
                'version': version.split(',')[0] if version else 'unknown'
            }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'message': f'Database connection failed: {str(e)}',
                'error': str(e)
            }

    async def check_redis(self) -> Dict[str, Any]:
        """Check Redis connectivity"""
        try:
            redis_url = os.getenv('REDIS_URL', 'redis://redis:6379/0')
            redis = await aioredis.create_redis_pool(redis_url)
            info = await redis.info()
            redis.close()
            await redis.wait_closed()
            return {
                'status': 'healthy',
                'message': 'Redis connected',
                'version': info.get('redis_version', 'unknown'),
                'memory_mb': int(info.get('used_memory', 0) / 1024 / 1024)
            }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'message': f'Redis connection failed: {str(e)}',
                'error': str(e)
            }

    async def check_backend(self) -> Dict[str, Any]:
        """Check Backend service"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    'http://backend:8000/health',
                    timeout=10
                )
                return {
                    'status': 'healthy' if response.status_code == 200 else 'unhealthy',
                    'message': 'Backend service responding',
                    'status_code': response.status_code
                }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'message': f'Backend service unavailable: {str(e)}',
                'error': str(e)
            }

    async def check_brain(self) -> Dict[str, Any]:
        """Check Brain service"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    'http://brain:8001/health',
                    timeout=10
                )
                return {
                    'status': 'healthy' if response.status_code == 200 else 'unhealthy',
                    'message': 'Brain service responding',
                    'status_code': response.status_code
                }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'message': f'Brain service unavailable: {str(e)}',
                'error': str(e)
            }

    async def check_agents(self) -> Dict[str, Any]:
        """Check Agents service"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    'http://agents:8002/health',
                    timeout=10
                )
                return {
                    'status': 'healthy' if response.status_code == 200 else 'unhealthy',
                    'message': 'Agents service responding',
                    'status_code': response.status_code
                }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'message': f'Agents service unavailable: {str(e)}',
                'error': str(e)
            }

    async def check_knowledge(self) -> Dict[str, Any]:
        """Check Knowledge service"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    'http://knowledge:8003/health',
                    timeout=10
                )
                return {
                    'status': 'healthy' if response.status_code == 200 else 'unhealthy',
                    'message': 'Knowledge service responding',
                    'status_code': response.status_code
                }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'message': f'Knowledge service unavailable: {str(e)}',
                'error': str(e)
            }

    async def check_frontend(self) -> Dict[str, Any]:
        """Check Frontend service"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    'http://frontend:3000/',
                    timeout=10,
                    follow_redirects=True
                )
                return {
                    'status': 'healthy' if response.status_code == 200 else 'unhealthy',
                    'message': 'Frontend service responding',
                    'status_code': response.status_code
                }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'message': f'Frontend service unavailable: {str(e)}',
                'error': str(e)
            }

    async def run_all_checks(self) -> Dict[str, Any]:
        """Run all health checks concurrently"""
        checks = await asyncio.gather(
            self.check_database(),
            self.check_redis(),
            self.check_backend(),
            self.check_brain(),
            self.check_agents(),
            self.check_knowledge(),
            self.check_frontend()
        )

        self.results = {
            'timestamp': datetime.now().isoformat(),
            'services': {
                'database': checks[0],
                'redis': checks[1],
                'backend': checks[2],
                'brain': checks[3],
                'agents': checks[4],
                'knowledge': checks[5],
                'frontend': checks[6]
            }
        }

        # Overall status
        unhealthy_count = sum(
            1 for check in checks if check.get('status') == 'unhealthy'
        )
        
        if unhealthy_count == 0:
            self.results['overall_status'] = 'healthy'
        elif unhealthy_count <= 2:
            self.results['overall_status'] = 'degraded'
        else:
            self.results['overall_status'] = 'unhealthy'

        self.results['elapsed_seconds'] = (
            datetime.now() - self.start_time
        ).total_seconds()

        return self.results


async def main():
    """Main entry point"""
    checker = HealthChecker()
    results = await checker.run_all_checks()
    
    # Print results
    print(json.dumps(results, indent=2))
    
    # Return appropriate exit code
    if results['overall_status'] == 'healthy':
        sys.exit(0)
    elif results['overall_status'] == 'degraded':
        sys.exit(1)
    else:
        sys.exit(2)


if __name__ == '__main__':
    asyncio.run(main())
