# syntax=docker/dockerfile:1.7
#
# Development overlay for LAWIM_V2.
#
# This layer is intentionally thin. It inherits the shared base and only adds
# development-oriented metadata and runtime flags.

ARG BASE_IMAGE=lawim/base:local
FROM ${BASE_IMAGE}

LABEL org.opencontainers.image.title="LAWIM_V2 development image" \
      org.opencontainers.image.description="Development overlay for LAWIM_V2" \
      org.opencontainers.image.source="LAWIM_V2"

ENV LAWIM_ENV=development \
    LAWIM_IMAGE_FLAVOR=development \
    LAWIM_DEBUG=1
