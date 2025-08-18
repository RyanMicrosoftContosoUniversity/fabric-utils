import logging

class BaseLogger:
    GLOBAL_LOG_LEVEL = None

    def __init__(self, logger_name=None, level=logging.INFO, config=None):
        # use class name as logger name by default for clarity
        name = logger_name or self.__class__.__name__
        self.logger = logging.getLogger(name)

        # if global override is set, use it; otherwise use the provided level
        effective_level = BaseLogger.GLOBAL_LOG_LEVEL or level
        self.logger.setLevel(effective_level)

        destinations = []
        if config and "destinations" in config:
            destinations = config["destinations"]
        else:
            destinations = ["console"]

        for dest in destinations:
            if dest == "console":
                # setup as console handler
                if not self.logger.handlers:
                    # default to console handler; additional handlers can eb added via config
                    console_handler = logging.StreamHandler()
                    console_handler.setLevel(effective_level)

                    # set a default formatter (to be defined in a standardized format section)
                    console_handler.setFormatter(self._get_default_formatter())
                    self.logger.addHandler(console_handler)
                    self.logger.propagate = False  # prevent double logging in root
            elif dest == "file":
                file_path = config.get("file_path", "app.log")
                file_handler = logging.FileHandler(file_path)
                file_handler.setLevel
                file_handler.setFormatter(self._get_default_formatter())
                self.logger.addHandler(file_handler)
            elif dest == "external":
                # not setup for now
                pass




    def _get_default_formatter(self):
        """
        Define the standard format for all logs 
        """
        fmt = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"

        return logging.Formatter(fmt)
    
    
