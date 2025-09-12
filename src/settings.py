import logging
from pathlib import Path
from omegaconf import OmegaConf

logger = logging.getLogger(__name__)

CONFIG_PATH = Path(__file__).parents[1] / "conf" / "config.yaml"

def load_config():
    logger.debug(f"Loading config from: {CONFIG_PATH}")
    return OmegaConf.load(CONFIG_PATH)