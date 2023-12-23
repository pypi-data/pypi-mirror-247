from mkdocs.config.base import Config
from mkdocs.config.config_options import Deprecated, Type


# Minecraft plugin configuration
class MinecraftConfig(Config):
    enabled = Type(bool, default=True)
    cache_dir = Type(str, default=".cache/plugin/minecraft")

    images_dir = Type(str, default="assets/images/minecraft")
    background_path = Type(str, default="")
    items_path = Type(str, default="")
