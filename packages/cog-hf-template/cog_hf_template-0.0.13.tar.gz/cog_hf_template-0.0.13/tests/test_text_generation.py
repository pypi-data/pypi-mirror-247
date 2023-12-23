from pathlib import Path

from cog_hf_template import get_predictor

from .testing_utils import cache_clear


def test_text_generation_predictor(cache_clear):
    predictor = get_predictor(
        task="text-generation",
        hf_model_id="facebook/opt-125m",
        cache_dir="./weights-cache",
        load_in_4bit=False,
        torch_dtype="fp32",
    )()
    predictor.setup()
    generator = predictor.predict("The meaning of life is", 50, 1.0, 1.0, 1)

    results = ""
    for out in generator:
        results += out

    assert isinstance(results, str)
    assert len(out) > 0
    assert Path("./weights-cache").is_dir() and list(Path("./weights-cache").glob("**/*")) != []
