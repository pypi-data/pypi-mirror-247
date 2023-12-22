import os
from zrcl3.expirable_property import ExpireOnFileProperty 
import json
import toml

def test_std_file_property():
    class A:
        @ExpireOnFileProperty("file.txt")
        def someproperty(self):
            return "some default value"

    if os.path.exists("file.txt"):
        os.remove("file.txt")

    a = A()

    assert a.someproperty == "some default value"

    with open("file.txt", 'w') as file:
        file.write("a value")

    assert a.someproperty == "a value"

    a.someproperty = "new value"  # Will save to the file

    with open("file.txt", 'r') as file:
        assert file.read() == "new value"

    os.remove("file.txt")
    
def test_json_file_property():
    class A:
        @ExpireOnFileProperty("file.json")
        def someproperty(self):
            return {"default_key": "default_value"}

    # Ensure the file is not present before the test
    if os.path.exists("file.json"):
        os.remove("file.json")

    a = A()

    # Check that the default value is set correctly
    assert a.someproperty == {'default_key': 'default_value'}

    # Modify the file with a new value
    with open("file.json", 'w') as file:
        json.dump({"key": "value"}, file)

    # Check that the property reflects the new file contents
    assert a.someproperty == {"key": "value"}

    # Change the property value, which should update the file
    a.someproperty = {"new_key": "new_value"}

    # Read the file and check if it has the new value
    with open("file.json", 'r') as file:
        file_content = json.load(file)
        assert file_content == {"new_key": "new_value"}
        
    os.remove("file.json")
    
def test_toml_file_property():
    class A:
        @ExpireOnFileProperty("file.toml")
        def someproperty(self):
            return {"default_key": "default_value"}

    # Ensure the file is not present before the test
    if os.path.exists("file.toml"):
        os.remove("file.toml")

    a = A()

    # Check that the default value is set correctly
    assert a.someproperty == {"default_key": "default_value"}

    # Modify the file with a new value
    with open("file.toml", 'w') as file:
        toml.dump({"key": "value"}, file)

    # Check that the property reflects the new file contents
    assert a.someproperty == {"key": "value"}

    # Change the property value, which should update the file
    a.someproperty = {"new_key": "new_value"}

    # Read the file and check if it has the new value
    with open("file.toml", 'r') as file:
        file_content = toml.load(file)
        assert file_content == {"new_key": "new_value"}

    os.remove("file.toml")