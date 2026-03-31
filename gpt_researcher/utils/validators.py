"""Pydantic validation models for GPT Researcher."""

from typing import List
import socket
import ipaddress
import logging
from urllib.parse import urlparse

from pydantic import BaseModel, Field


class Subtopic(BaseModel):
    """Model representing a single research subtopic.

    Attributes:
        task: The name or description of the subtopic task.
    """
    task: str = Field(description="Task name", min_length=1)


class Subtopics(BaseModel):
    """Model representing a collection of research subtopics.

    Used for parsing and validating subtopic lists generated
    by the LLM during research planning.

    Attributes:
        subtopics: List of Subtopic objects.
    """
    subtopics: List[Subtopic] = []

def validate_url(url: str) -> bool:
    """
    Validates a URL to ensure it does not point to a private IP address.
    Returns True if valid, False if invalid (private/loopback).
    """
    try:
        parsed = urlparse(url)
        if parsed.scheme not in ('http', 'https'):
            return False

        hostname = parsed.hostname
        if not hostname:
            return False

        # Resolve hostname to IP
        try:
            # Note: this is blocking, but typically fast unless DNS is slow/down
            ip_address = socket.gethostbyname(hostname)
        except socket.gaierror:
            logger.warning(f"Could not resolve hostname: {hostname}")
            return False

        # Check if IP is private
        ip = ipaddress.ip_address(ip_address)
        if ip.is_private or ip.is_loopback or ip.is_link_local:
            logger.warning(f"Blocked private IP access: {url} -> {ip_address}")
            return False

        return True
    except Exception as e:
        logger.warning(f"Error validating URL {url}: {e}")
        return False
