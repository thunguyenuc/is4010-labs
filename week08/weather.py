import argparse
import importlib.util
import os
import sys
from pathlib import Path

from week08.favorites import FavoritesManager
from week08.weather_api import WeatherAPI, format_current_weather, format_forecast

FAVORITES_FILE = Path(__file__).with_name("favorites.json")


def load_api_key():
    api_key = os.getenv("WEATHER_API_KEY")
    if api_key and str(api_key).strip():
        return str(api_key).strip()

    config_path = Path(__file__).with_name("config.py")
    if not config_path.exists():
        return None

    try:
        spec = importlib.util.spec_from_file_location("week08_config", config_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        api_key = getattr(module, "WEATHER_API_KEY", None)
        if api_key and str(api_key).strip():
            return str(api_key).strip()
    except (ImportError, AttributeError, OSError, TypeError, ValueError):
        return None

    return None


def build_parser():
    parser = argparse.ArgumentParser(description="Weather CLI")
    subparsers = parser.add_subparsers(dest="command")

    current_parser = subparsers.add_parser("current", help="Show current weather")
    current_parser.add_argument("location")
    current_parser.set_defaults(command="current")

    forecast_parser = subparsers.add_parser("forecast", help="Show a forecast")
    forecast_parser.add_argument("location")
    forecast_parser.add_argument("--days", type=int, default=3)
    forecast_parser.set_defaults(command="forecast")

    favorites_parser = subparsers.add_parser("favorites", help="Manage saved favorites")
    favorites_subparsers = favorites_parser.add_subparsers(dest="favorites_command")

    add_parser = favorites_subparsers.add_parser("add", help="Save a favorite")
    add_parser.add_argument("name")
    add_parser.add_argument("location")
    add_parser.set_defaults(favorites_command="add")

    list_parser = favorites_subparsers.add_parser("list", help="List favorites")
    list_parser.set_defaults(favorites_command="list")

    remove_parser = favorites_subparsers.add_parser("remove", help="Remove a favorite")
    remove_parser.add_argument("name")
    remove_parser.set_defaults(favorites_command="remove")

    return parser


def _resolve_location(manager, location):
    favorite_location = manager.get_location(location)
    return favorite_location if favorite_location is not None else location


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "current":
        api_key = load_api_key()
        if not api_key:
            print("API key not found. Set WEATHER_API_KEY or create config.py.", file=sys.stderr)
            return 1

        manager = FavoritesManager(str(FAVORITES_FILE))
        location = _resolve_location(manager, args.location)
        data = WeatherAPI(api_key).get_current_weather(location)
        if data is None:
            print(f"Unable to fetch weather for {location}.", file=sys.stderr)
            return 1

        print(format_current_weather(data))
        return 0

    if args.command == "forecast":
        api_key = load_api_key()
        if not api_key:
            print("API key not found. Set WEATHER_API_KEY or create config.py.", file=sys.stderr)
            return 1

        manager = FavoritesManager(str(FAVORITES_FILE))
        location = _resolve_location(manager, args.location)

        try:
            data = WeatherAPI(api_key).get_forecast(location, days=args.days)
        except ValueError as exc:
            print(str(exc), file=sys.stderr)
            return 1

        if data is None:
            print(f"Unable to fetch forecast for {location}.", file=sys.stderr)
            return 1

        print(format_forecast(data))
        return 0

    if args.command == "favorites":
        manager = FavoritesManager(str(FAVORITES_FILE))

        if args.favorites_command == "add":
            if not manager.add(args.name, args.location):
                print(f"Favorite already exists: {args.name}", file=sys.stderr)
                return 1
            print(f"Added favorite: {args.name}")
            return 0

        if args.favorites_command == "list":
            for name, location in manager.list_all().items():
                print(f"{name}: {location}")
            return 0

        if args.favorites_command == "remove":
            if not manager.remove(args.name):
                print(f"Favorite not found: {args.name}", file=sys.stderr)
                return 1
            print(f"Removed favorite: {args.name}")
            return 0

    parser.print_help(sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
