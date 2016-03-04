import pytest

from adam.adam import *

@pytest.fixture
def storage():
    return AssetStorage()

def test_contains_asset(storage):
    a = Asset()
    storage['key'] = a
    assert storage['key'] == a
    
def test_contains_key(storage):
    a = Asset()
    assert 'key' not in storage
    storage['key'] = a
    assert 'key' in storage
    
def test_asset_is_versioned(storage):
    a = Asset()
    updated_a = Asset()
    storage['key'] = a
    storage['key'] = updated_a
    versions = storage.versions_of('key')
    assert len(versions) == 2
    assert versions[0] == a
    assert versions[1] == updated_a

def test_asset_is_deleted(storage):
    a = Asset()
    storage['key'] = a
    del storage['key']
    assert 'key' not in storage

def test_search_asset(storage):
    assets_with_1s_duration = storage.get(duration=1)
    assert not assets_with_1s_duration
    
    a = Asset()
    a.duration = 1
    storage['key'] = a

    assets_with_1s_duration = storage.get(duration=1)
    assert len(assets_with_1s_duration) == 1
    assert assets_with_1s_duration[0] == a

def test_read_unkown_file():
    reader = AssetReader()
    file_path = 'tests/16-bit-mono.wav'
    asset = reader.read(file_path)
    assert asset == WavReader().read(file_path)

def test_supported_mime_types():
    assert len(AssetReader.supported_mime_types) > 0

def test_deleting_unkown_key_raises_exception(storage):
    with pytest.raises(KeyError):
        del storage['key']

def test_create_asset_from_wav():
    reader = WavReader()
    asset = reader.read('tests/16-bit-mono.wav')
    assert asset.mime_type == 'audio/wav'
    assert asset.framerate == 48000
    assert asset.channels == 1
    assert asset.essence != None
    
def test_create_asset_from_mp3():
    reader = Mp3Reader()
    mp3_file_path = 'tests/64kbits.mp3'
    asset = reader.read(mp3_file_path)
    assert asset.mime_type == 'audio/mpeg'
    assert asset.duration == 0.1
    assert asset.essence != None

    # Assert that essence was stripped from metadata
    with open(mp3_file_path, 'rb') as mp3_file:
        assert asset.essence != mp3_file.read()

def test_mp3_reader_does_not_change_file():
    mp3_file_path = 'tests/64kbits.mp3'
    with open(mp3_file_path, 'rb') as mp3_file:
        expected_data = mp3_file.read()
    reader = Mp3Reader()
    reader.read(mp3_file_path)
    with open(mp3_file_path, 'rb') as mp3_file:
        actual_data = mp3_file.read()
    assert expected_data == actual_data
    
def test_asset_has_mime_type():
    a = Asset()
    assert hasattr(a, 'mime_type')

def test_asset_has_essence():
    asset = Asset()
    assert hasattr(asset, 'essence')

def test_asset_equality():
    a = Asset()
    a.some_attr = 42
    b = Asset()
    b.some_attr = 42
    
    assert a is not b
    assert a == b
