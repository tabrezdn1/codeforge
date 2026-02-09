"""CodeForge: Multi-agent requirements-to-code system built with Google ADK."""

import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("codeforge")

from .agent import root_agent

logger.info("CodeForge application starting up.")

__all__ = ["root_agent"]
