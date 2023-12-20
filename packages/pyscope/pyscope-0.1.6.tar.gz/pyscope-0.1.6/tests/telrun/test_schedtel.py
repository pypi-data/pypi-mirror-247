import pytest

from pyscope.telrun import schedtel


def test_schedtel(tmp_path):
    catalog = "./tests/reference/test_schedtel.cat"
    observatory = "./tests/reference/simulator_observatory.cfg"

    schedule = schedtel(catalog=catalog, observatory=observatory)


if __name__ == "__main__":
    test_schedtel("")
