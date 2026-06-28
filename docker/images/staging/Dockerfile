# syntax=docker/dockerfile:1.7
#
# Staging overlay for LAWIM_V2.
#
# This layer mirrors production behavior as closely as possible while keeping
# the environment explicitly marked as staging.

ARG BASE_IMAGE=lawim/base:local
FROM ${BASE_IMAGE}

LABEL org.opencontainers.image.title="LAWIM_V2 staging image" \
      org.opencontainers.image.description="Staging overlay for LAWIM_V2" \
      org.opencontainers.image.source="LAWIM_V2"

ENV LAWIM_ENV=staging \
    LAWIM_IMAGE_FLAVOR=staging \
    LAWIM_DEBUG=0
