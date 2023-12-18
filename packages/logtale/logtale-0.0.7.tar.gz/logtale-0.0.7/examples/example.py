import logtale.logtale as tale
import logtale.filter as filter


def main():
    logtale = tale.LogTale("example", "./example.toml")
    logger = logtale.logger.getChild(__name__)
    logger.addFilter(filter.LogFilter(prepend_text="ExamplePrepend"))

    logger.debug("test - debug")
    logger.info("test - info")
    logger.warning("test - warning")
    logger.error("test - error")
    logger.critical("test - critical")

if __name__ == "__main__":
    main()
