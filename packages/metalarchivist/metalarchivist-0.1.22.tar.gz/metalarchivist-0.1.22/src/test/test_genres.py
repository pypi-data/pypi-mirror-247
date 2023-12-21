
import sys
import unittest
import importlib.util
from types import ModuleType
from enum import Enum

from configparser import ConfigParser


class Submodule(Enum):
    MODULE = 'metalarchivist', './src/metalarchivist/__init__.py'
    EXPORT = 'metalarchivist.export', './src/metalarchivist/export/__init__.py'
    IFACE = 'metalarchivist.interface', './src/metalarchivist/interface/__init__.py'


def run_test_cases():
    unittest.main(argv=[''], verbosity=2)


def prepare_submodule(submodule: Submodule) -> ModuleType:
    submodule_name, submodule_path = submodule.value
    spec = importlib.util.spec_from_file_location(submodule_name, submodule_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[submodule_name] = module
    spec.loader.exec_module(module)

    return module


def load_module():
    config = ConfigParser({'unittests': {'OUTPUTDIR': './'}})
    config.read('metallum.cfg')

    metalarchivist = prepare_submodule(Submodule.MODULE)
    interface = prepare_submodule(Submodule.IFACE)
    export = prepare_submodule(Submodule.EXPORT)

    return metalarchivist, interface, export, config


class TestGenres(unittest.TestCase):
    metalarchivist, interface, export, config = load_module()

    def test_genres_pages(self):
        genre_bands = self.export.Genres.get_genre(self.interface.Genre.BLACK)
        self.assertIsNotNone(genre_bands)
        self.assertIsInstance(genre_bands, self.interface.GenrePage)
        self.assertIsInstance(genre_bands.data, list)
        self.assertIsInstance(genre_bands.data[0], self.interface.BandGenre)
        self.assertIsInstance(genre_bands.data[0].genre, self.interface.Genre.BLACK.value)

    def test_genres_export(self):
        ...



if __name__ == '__main__':
    run_test_cases()
