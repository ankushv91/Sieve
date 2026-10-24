"""
ARQ worker entry point.
arq app.domains.campaigns.worker_entry.WorkerSettings
Terminal failure handling
The ``ingest_single_file`` atomic worker detects terminal failure inline by
comparing ``ctx['job_try']`` against ``settings.WORKER_MAX_TRIES``.  On the
last attempt the item is removed from the Redis pending Set so the batch can
reach completion even when individual files fail permanently.  No separate
``on_job_end`` hook is needed.
"""

from __future__ import annotations

import logging

from arq.connections import RedisSettings
from arq.cron import cron

from app.core.config import settings
from app.domains.campaigns.worker import (
    dispatch_ingestion_batch,
    dispatch_campaign_screening,
    ingest_single_file,
    process_csv_chunk,
    screen_single_candidate,
    reconcile_zombie_tasks,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(name)-30s  %(levelname)-8s  %(message)s",
)


def _parse_redis_settings() -> RedisSettings:
    """Convert the application ``REDIS_URL`` into arq ``RedisSettings``."""
    return RedisSettings.from_dsn(settings.REDIS_URL)


class WorkerSettings:
    """Configuration object consumed by ``arq``."""

    functions = [
        dispatch_ingestion_batch,
        dispatch_campaign_screening,
        ingest_single_file,
        process_csv_chunk,
        screen_single_candidate,
    ]

    cron_jobs = [
        # Re-queue candidates stuck IN_PROGRESS for > 2 h (zombie recovery)
        cron(reconcile_zombie_tasks, minute={0, 10, 20, 30, 40, 50}),
    ]

    redis_settings = _parse_redis_settings()

    max_jobs = 20

    job_timeout = settings.ARQ_JOB_TIMEOUT_SECONDS

    max_tries = settings.WORKER_MAX_TRIES

    health_check_key = "arq:solobuildai:health"
