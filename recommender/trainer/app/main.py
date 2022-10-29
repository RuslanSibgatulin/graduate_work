from cli import root
from containers import Container
from core.config import get_settings


def main():
    args = root.parse_args()

    settings = get_settings()
    container = Container()
    container.config.from_pydantic(settings)

    args.handler(args)


if __name__ == "__main__":
    main()
