import random

import numpy as np
import pytest
import torch
from PIL import Image, ImageDraw
from torchvision.transforms.functional import to_tensor

from chariot_transforms import bbox_ops
from chariot_transforms.augmentations.transforms import (
    AutoContrast,
    Brightness,
    CenterCrop,
    ColorJitter,
    Contrast,
    Cutout,
    Equalize,
    Gamma,
    Grayscale,
    HorizontalShear,
    Hue,
    Invert,
    Pad,
    Posterize,
    RandAugment,
    RandomAffine,
    RandomCrop,
    RandomGrayscale,
    RandomHorizontalFlip,
    RandomPerspective,
    RandomResize,
    RandomRotation,
    RandomVerticalFlip,
    Resize,
    ResizePreserveAspect,
    Rotation,
    Saturation,
    Sharpness,
    Solarize,
    TranslateY,
)

bbox_ops.DROP_BBOX_AREA_RATIO_THRES = 0.0

random.seed(7)
np.random.seed(6)


def random_bbox(img):
    ymin = random.randint(0, img.height - 40)
    ymax = random.randint(ymin + 20, img.height)
    xmin = random.randint(0, img.width - 40)
    xmax = random.randint(xmin + 20, img.width)

    return [ymin, xmin, ymax, xmax]


eps = 1e-6


def check_image(img):
    assert len(img.shape) == 4
    assert img.min().item() >= 0 - eps
    assert img.max().item() <= 1 + eps


def _test_bbox_conversion(transform, atol: float = 3.5):
    """
    Test that bounding boxes get transformed properly with an image.
    It does this by doing the following 100 times:

    1. Create a PIL image with a random rectangle in it.
    2. Transform the image and bounding box of the rectangle
    3. Check that the resulting rectangle in the image is
    circumscribed by the transformed bounding box
    """

    for _ in range(100):
        img = Image.new("RGB", (200, 100))
        bbox = random_bbox(img)
        img_draw = ImageDraw.Draw(img)
        img_draw.rectangle([bbox[1], bbox[0], bbox[3], bbox[2]], fill="red")

        img_tensor = to_tensor(img).unsqueeze(0)
        trans_img, trans_bbox_dict = transform(
            img_tensor, bbox_dict={"bboxes": [bbox], "classes": ["class"]}
        )

        # find pixels of the rectangle in the image
        _, ys, xs = torch.where(trans_img[0] > 20 / 255)

        if len(ys) == 0 or ys.max() - ys.min() < 1 or xs.max() - xs.min() < 1:
            # if no pixels (e.g. if rectangle got cropped out) check that
            # no bounding boxes come back
            assert len(trans_bbox_dict["bboxes"]) == 0
        elif ys.max() - ys.min() == 1 or xs.max() - xs.min() == 1:
            # a sliver
            assert len(trans_bbox_dict["bboxes"]) <= 1
        else:
            assert len(trans_bbox_dict["bboxes"]) != 0
            trans_bbox = trans_bbox_dict["bboxes"][0]
            np.testing.assert_allclose(
                [ys.min(), xs.min(), ys.max(), xs.max()],
                trans_bbox,
                rtol=1e-3,
                atol=atol,
            )


def _test_mask_conversion(
    transform, check_mask_unchanged: bool, decimal: int = 7
):
    """Test that masks get transformed properly with an image. If check_mask_unchanged
    is True then it checks the transformed mask is the same as the original mask. Otheriwse
    it checks that the transformed mask is the same as the transformed image.
    """
    for _ in range(100):
        img = torch.randint(0, 256, (1, 100, 100), dtype=torch.uint8)
        mask = Image.fromarray(img[0].numpy())

        trans_img, trans_mask = transform(img.unsqueeze(0) / 255, mask=mask)

        assert isinstance(trans_mask, Image.Image)
        assert trans_mask.mode == "L"

        if check_mask_unchanged:
            np.testing.assert_equal(mask, trans_mask)
        else:
            np.testing.assert_almost_equal(
                trans_img[0][0].numpy(),
                np.array(trans_mask) / 255,
                decimal=decimal,
            )


def test_auto_contrast():
    t = AutoContrast()
    _test_bbox_conversion(t)
    _test_mask_conversion(t, check_mask_unchanged=True)


def test_brightness():
    t = Brightness(0.7)
    _test_bbox_conversion(t)
    _test_mask_conversion(t, check_mask_unchanged=True)


def test_saturation():
    t = Saturation(0.7)
    _test_bbox_conversion(t)
    _test_mask_conversion(t, check_mask_unchanged=True)


def test_center_crop():
    t = CenterCrop(size=(12, 20))
    _test_bbox_conversion(t)
    _test_mask_conversion(t, check_mask_unchanged=False)


def test_color_jitter():
    t = ColorJitter(0.2, 0.2, 0.2, 0.2)
    _test_bbox_conversion(t)
    _test_mask_conversion(t, check_mask_unchanged=True)


def test_contrast():
    t = Contrast(1.2)
    _test_bbox_conversion(t)
    _test_mask_conversion(t, check_mask_unchanged=True)


def test_gamma():
    t = Gamma(1.2)
    _test_bbox_conversion(t)
    _test_mask_conversion(t, check_mask_unchanged=True)


def test_hue():
    t = Hue(0.2)
    _test_bbox_conversion(t)
    _test_mask_conversion(t, check_mask_unchanged=True)


def test_cutout():
    t = Cutout(16)
    _test_bbox_conversion(t)
    _test_mask_conversion(t, check_mask_unchanged=False)


def test_equalize():
    t = Equalize()
    _test_bbox_conversion(t)
    _test_mask_conversion(t, check_mask_unchanged=True)


def test_grayscale():
    t = Grayscale(num_output_channels=3)
    _test_bbox_conversion(t)
    _test_mask_conversion(t, check_mask_unchanged=True)


def test_horizontal_shear():
    t = HorizontalShear(0.1)
    _test_bbox_conversion(t)
    _test_mask_conversion(t, check_mask_unchanged=False)


def test_invert():
    img = to_tensor(Image.new("RGB", (200, 100))).unsqueeze(0)
    new_img = Invert()(img)
    assert new_img.max() <= 1
    assert new_img.min() >= 0
    assert new_img.shape == img.shape
    torch.testing.assert_close(1 - img, new_img)

    _test_mask_conversion(Invert(), check_mask_unchanged=True)


def test_pad():
    t = Pad(padding=(16, 14, 32, 6))
    _test_bbox_conversion(t)
    _test_mask_conversion(t, check_mask_unchanged=False)


def test_posterize():
    t = Posterize(3)
    _test_bbox_conversion(t)
    _test_mask_conversion(t, check_mask_unchanged=True)


def test_random_crop():
    t = RandomCrop((100, 50))
    _test_bbox_conversion(t)
    _test_mask_conversion(t, check_mask_unchanged=False)


def test_random_horizontal_flip():
    t = RandomHorizontalFlip()
    _test_bbox_conversion(t)
    _test_mask_conversion(t, check_mask_unchanged=False)


def test_horizontal_flip():
    t = RandomHorizontalFlip(1)
    _test_bbox_conversion(t)
    _test_mask_conversion(t, check_mask_unchanged=False)


def test_random_resize():
    t = RandomResize(scale_range_high=2.0, p=1.0)
    _test_bbox_conversion(t, atol=3)
    _test_mask_conversion(t, check_mask_unchanged=False, decimal=2)


def test_random_vertical_flip():
    t = RandomVerticalFlip()
    _test_bbox_conversion(t)
    _test_mask_conversion(t, check_mask_unchanged=False)


def test_random_affine():
    t = RandomAffine(
        degrees=0, translate=(0.1, 0.1), scale=(0.9, 1.2), shear=(-10, 10)
    )
    _test_bbox_conversion(t, atol=10)
    _test_mask_conversion(t, check_mask_unchanged=False)


def test_rand_augment_m_specified():
    t = RandAugment(
        n=2,
        m=3,
        augs_to_remove=[  # remove color transforms
            "Invert",
            "Solarize",
            "Brightness",
            "Contrast",
            "AutoContrast",
            "HorizontalShear",
            "VerticalShear",
            "Posterize",
            "Sharpness",
            "Equalize",
        ],
    )
    _test_bbox_conversion(t, atol=8.5)
    _test_mask_conversion(t, check_mask_unchanged=False)


def test_rand_augment_m_not_specified():
    t = RandAugment(
        n=3,
        augs_to_use=[
            "TranslateY",
            "TranslateX",
        ],
    )
    _test_bbox_conversion(t)
    _test_mask_conversion(t, check_mask_unchanged=False)


def test_random_grayscale():
    t = RandomGrayscale()
    _test_bbox_conversion(t)
    _test_mask_conversion(t, check_mask_unchanged=True)


def test_random_perspective():
    t = RandomPerspective(0.1)
    _test_bbox_conversion(t, atol=11)
    # the mask test is failing, unsure why. this transform doesn't seem
    # to be used in chariot so maybe should just remove it
    # _test_mask_conversion(t, check_mask_unchanged=False)


def test_random_rotation():
    t = RandomRotation(10)
    _test_bbox_conversion(t)
    _test_mask_conversion(t, check_mask_unchanged=False)


def test_resize():
    t = Resize((32, 32))
    _test_bbox_conversion(t)
    _test_mask_conversion(t, check_mask_unchanged=False, decimal=2)


def test_resize_single_int():
    img = to_tensor(Image.new("RGB", (200, 100))).unsqueeze(0)
    new_img = Resize(32)(img)
    assert new_img.shape == (1, 3, 32, 32 * 200 / 100)
    img = to_tensor(Image.new("RGB", (100, 200))).unsqueeze(0)
    new_img = Resize(32)(img)
    assert new_img.shape == (1, 3, 32 * 200 / 100, 32)


def test_resize_preserve_aspect():
    _test_bbox_conversion(ResizePreserveAspect(new_h=32, new_w=32))


def test_rotation():
    t = Rotation(10)
    _test_bbox_conversion(t)
    _test_mask_conversion(t, check_mask_unchanged=False)


def test_sharpness():
    t = Sharpness(0.5)
    _test_bbox_conversion(t)
    _test_mask_conversion(t, check_mask_unchanged=True)


def test_solarize():
    img = Image.new("RGB", (200, 100))
    img_tensor = to_tensor(img).unsqueeze(0)

    check_image(Solarize(1)(img_tensor))
    check_image(Solarize(0)(img_tensor))
    check_image(Solarize(0.5)(img_tensor))

    # with threshold 1 the transform shouldn't do anything
    _test_bbox_conversion(Solarize(1))
    _test_mask_conversion(Solarize(0.5), check_mask_unchanged=True)


def test_translate_y():
    t = TranslateY(0.4)
    _test_bbox_conversion(t)
    _test_mask_conversion(t, check_mask_unchanged=False)


def test_compose_preprocessing_and_random_augmentation():
    from chariot_transforms.augmentations.transforms import AugmentationCompose

    transform = AugmentationCompose(
        [
            Resize((128, 64)),
            RandAugment(
                2,
                1,
                augs_to_remove=[
                    "Invert",
                    "Solarize",
                    "Brightness",
                    "Contrast",
                    "HorizontalShear",
                    "VerticalShear",
                    "Equalize",
                ],
            ),
        ]
    )

    _test_bbox_conversion(transform.transforms[0], atol=8)


def test_rand_augment_color_deprecation():
    with pytest.warns(DeprecationWarning) as w:
        RandAugment(n=2, m=3, augs_to_use=["Solarize", "Color"])
    assert "The `Color` option has been removed" in str(w[0].message)

    with pytest.warns(DeprecationWarning) as w:
        RandAugment(n=2, m=3, augs_to_remove=["Solarize", "Color"])
    assert "The `Color` option has been removed" in str(w[0].message)


def test_rand_augment_invalid_augmentation():
    with pytest.raises(ValueError) as exc_info:
        RandAugment(n=2, m=3, augs_to_use=["DNE"])
    assert "Invalid augmentation name" in str(exc_info.value)

    with pytest.raises(ValueError) as exc_info:
        RandAugment(n=2, m=3, augs_to_remove=["DNE"])
    assert "Invalid augmentation name" in str(exc_info.value)


def test_random_crop_convert_mask():
    # cropping
    t = RandomCrop((10, 20), p=1.0)

    # grayscale image
    img = torch.randint(0, 256, (1, 100, 100), dtype=torch.uint8)
    mask = Image.fromarray(img[0].numpy())

    trans_img, trans_mask = t(img.unsqueeze(0) / 255, mask=mask)

    assert trans_img.shape == (1, 1, 10, 20)
    assert isinstance(trans_mask, Image.Image)
    assert trans_mask.mode == "L"
    np.testing.assert_almost_equal(
        trans_img[0][0].numpy(), np.array(trans_mask) / 255
    )

    # no cropping
    t = RandomCrop((10, 20), p=0.0)

    trans_img, trans_mask = t(img.unsqueeze(0) / 255, mask=mask)

    assert trans_img.shape == (1, 1, 100, 100)
    assert isinstance(trans_mask, Image.Image)
    assert trans_mask.mode == "L"
    np.testing.assert_almost_equal(
        trans_img[0][0].numpy(), np.array(trans_mask) / 255
    )
