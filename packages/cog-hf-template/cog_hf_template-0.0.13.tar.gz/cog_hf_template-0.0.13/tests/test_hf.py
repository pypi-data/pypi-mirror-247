from cog_hf_template import get_predictor

from .testing_utils import cache_clear


def test_image_classification_predictor(cache_clear):
    predictor = get_predictor(
        hf_model_id="WinKawaks/vit-tiny-patch16-224", task="image-classification", cache_dir="./weights-cache"
    )()

    predictor.setup()
    out = predictor.predict("https://huggingface.co/nateraw/rare-puppers/resolve/main/images/shiba_inu.jpg")
    assert out["label"] == "dingo, warrigal, warragal, Canis dingo"


def test_text_classification_predictor(cache_clear):
    predictor = get_predictor(
        task="text-classification",
        hf_model_id="distilbert-base-uncased-finetuned-sst-2-english",
        cache_dir="./weights-cache",
    )()

    predictor.setup()
    out = predictor.predict("I love you so much")
    assert out == {"label": "POSITIVE", "score": 0.9998691082000732}
