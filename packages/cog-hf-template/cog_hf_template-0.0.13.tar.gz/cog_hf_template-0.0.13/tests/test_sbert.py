import torch

from cog_hf_template import get_predictor

from .testing_utils import cache_clear


def test_sbert_predictor(cache_clear):
    predictor = get_predictor(
        hf_model_id="sentence-transformers/paraphrase-TinyBERT-L6-v2",
        task="sentence-transformers-feature-extraction",
        cache_dir="./weights-cache",
    )()

    predictor.setup()
    a = predictor.predict("I like dogs")
    b = predictor.predict("pizza pizza")

    # 2 x 768
    embeds = torch.tensor([a, b])

    # 2 x 2
    similarity = embeds @ embeds.T
    assert torch.allclose(similarity, torch.tensor([[0.9999, 0.1293], [0.1293, 0.9999]]), atol=1e-4)
