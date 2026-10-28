from app.memory.memory_writer import MemoryWriter
from config import LEARNING_DATA_DIR

writer = MemoryWriter(LEARNING_DATA_DIR)

memory = {
    "should_update": True,
    "target_file": "relationship.txt",
    "entry_key": "Mother's Name",
    "entry_value": "Rakhi Tarco",
    "operation": "append",
}

result = writer.write_memory(memory)

print(result)