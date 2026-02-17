import os
import logging

def maybe_run_model_inference(db_path: str):
    """
    Placeholder:
    - إذا ENABLE_MODEL=false -> ما يسوي شيء
    - لما نركب مودل لاحقًا، نحط inference هنا.
    """
    log = logging.getLogger("model")
    enabled = os.getenv("ENABLE_MODEL", "false").lower() == "true"
    if not enabled:
        return None

    model_path = os.getenv("MODEL_PATH", "models/model.h5")
    log.info("Model enabled but not implemented yet. MODEL_PATH=%s", model_path)

    # لاحقًا: تحميل مودل + قراءة آخر N قياسات + تصنيف (مستقر/غير مستقر) أو (سكري/لا)
    return {"status": "MODEL_PLACEHOLDER", "model_path": model_path}
