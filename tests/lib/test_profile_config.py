from awslogs_watch.lib.profile_config import ProfileConfig


def test_load_profiles():
    path = "tests/config/cred"
    profiles = ["default", "test", "dev"]

    _profiles = ProfileConfig.load_profiles(path)

    assert profiles == _profiles


def test_load_profiles_empty():
    path = "tests/config/no_file"
    profiles = []

    _profiles = ProfileConfig.load_profiles(path)

    assert profiles == _profiles
