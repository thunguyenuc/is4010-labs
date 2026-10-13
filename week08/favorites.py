import json
import os


class FavoritesManager:
    def __init__(self, filename):
        self.filename = filename
        self._favorites = self._load()

    def _normalize_name(self, name):
        return str(name).strip().lower()

    def _load(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)
        except (FileNotFoundError, OSError, json.JSONDecodeError, TypeError, ValueError):
            return {}

        if not isinstance(data, dict):
            return {}

        cleaned = {}
        for key, value in data.items():
            if isinstance(key, str) and isinstance(value, str):
                cleaned[key.strip()] = value
        return cleaned

    def _save(self):
        directory = os.path.dirname(self.filename)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(self._favorites, file)

    def add(self, name, location):
        cleaned_name = str(name).strip()
        if not cleaned_name:
            return False

        for existing_name in self._favorites:
            if self._normalize_name(existing_name) == self._normalize_name(cleaned_name):
                return False

        self._favorites[cleaned_name] = str(location)
        self._save()
        return True

    def remove(self, name):
        cleaned_name = str(name).strip()
        for existing_name in list(self._favorites):
            if self._normalize_name(existing_name) == self._normalize_name(cleaned_name):
                del self._favorites[existing_name]
                self._save()
                return True
        return False

    def list_all(self):
        return dict(self._favorites)

    def get_location(self, name):
        cleaned_name = str(name).strip()
        for existing_name, location in self._favorites.items():
            if self._normalize_name(existing_name) == self._normalize_name(cleaned_name):
                return location
        return None
