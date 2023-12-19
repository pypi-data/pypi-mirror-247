from pydantic import BaseModel, Field
from typing import Callable, Type
import json
from pathlib import Path
import importlib

class ChatbotExtension(BaseModel):
    """A class that defines the interface for a user extension"""
    name: str = Field(..., description="The name of the extension")
    description: str = Field(..., description="A description of the extension")
    schema_class: Type[BaseModel] = Field(..., description="The pydantic model for the extension's aask return type")
    execute: Callable = Field(..., description="The extension's execution function")

def load_extensions_from_json(json_file_path):
    # Read JSON file
    with open(json_file_path, 'r') as file:
        extensions = json.load(file)
    # Process each extension
    extension_objects = []
    for extension in extensions:
        module_name = extension['name']
        schema_class_name = extension["schema"]
        execute_function_name = extension["execute"]
        # Construct absolute module path
        module_path = f"bioimageio_chatbot.chatbot_extensions.{module_name}.{module_name}"
        # Dynamically import the module
        module = importlib.import_module(module_path)
        # Load the class and function
        schema_class = getattr(module, schema_class_name)
        execute_function = getattr(module, execute_function_name)
        extension_obj = ChatbotExtension(
            name=module_name,
            description=extension['description'],
            schema_class=schema_class,
            execute=execute_function
        )
        extension_objects.append(extension_obj)
    return extension_objects

if __name__ == "__main__":
    json_file_path = Path(__file__).parent / "extensions.json"
    print(json_file_path)
    extension_objects = load_extensions_from_json(json_file_path)
    print(extension_objects)
