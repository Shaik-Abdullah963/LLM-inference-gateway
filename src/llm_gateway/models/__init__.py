"""Models module initialization."""

# Lazy imports to avoid loading heavy dependencies during test collection
__all__ = ["InferenceEngine", "engine"]


def __getattr__(name):
    """Lazy load model components."""
    if name == "InferenceEngine":
        from .engine import InferenceEngine
        return InferenceEngine
    elif name == "engine":
        from .engine import engine
        return engine
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
