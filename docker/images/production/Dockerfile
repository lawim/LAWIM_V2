# syntax=docker/dockerfile:1.7
#
# Production overlay for LAWIM_V2.
#
# This layer is intentionally the most conservative: it inherits the shared
# base and keeps the runtime surface minimal.

ARG BASE_IMAGE=lawim/base:local
FROM ${BASE_IMAGE}

LABEL org.opencontainers.image.title="LAWIM_V2 production image" \
      org.opencontainers.image.description="Production overlay for LAWIM_V2" \
      org.opencontainers.image.source="LAWIM_V2"

ENV LAWIM_ENV=production \
    LAWIM_IMAGE_FLAVOR=production \
    LAWIM_DEBUG=0
