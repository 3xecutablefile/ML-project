from pathlib import Path

BASE_DIR = Path(__file__).parent
DATASET_DIR = BASE_DIR / "dataset"
MODELS_DIR = BASE_DIR / "models"
OUTPUTS_DIR = BASE_DIR / "outputs"

BASE_MODEL = "gpt2"
MAX_LENGTH = 128
DEVICE = "mps"
EPOCHS = 3
BATCH_SIZE = 4
LEARNING_RATE = 5e-5
