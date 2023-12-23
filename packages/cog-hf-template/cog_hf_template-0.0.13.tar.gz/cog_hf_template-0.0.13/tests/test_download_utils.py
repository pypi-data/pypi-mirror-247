from pathlib import Path

from cog_hf_template.download_utils import maybe_pget_weights

from .testing_utils import cache_clear


def test_maybe_pget_weights(cache_clear):
    cache_dir = "./weights-cache"
    cache_path = Path(cache_dir)
    assert not cache_path.exists()
    maybe_pget_weights(
        "./weights-cache",
        "https://storage.googleapis.com/replicate-hf-weights/facebook/opt-125m/27dcfa74d334bc871f3234de431e71c6eeba5dd6",
        [
            "config.json",
            "generation_config.json",
            "merges.txt",
            "pytorch_model.bin",
            "special_tokens_map.json",
            "tokenizer_config.json",
            "vocab.json",
        ],
    )
    files = list(cache_path.glob("**/*"))
    assert len(files) == 7
