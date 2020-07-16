import os
import imageio
import imgaug as ia
from imgaug.augmentables.bbs import BoundingBox, BoundingBoxesOnImage
ia.seed(1)


print(os.getcwd())


# this happens with a pascal voc format.
path="C:\\Users\\Կարեն\\Desktop\\0000084_02139_d_0000007.jpg"
image = imageio.imread(path)
image = ia.imresize_single_image(image, (540, 960))
bbs = BoundingBoxesOnImage([
    BoundingBox(x1=258, x2=298, y1=326, y2=420),
    BoundingBox(x1=733, x2=771, y1=269, y2=342),
    BoundingBox(x1=475, x2=501, y1=213, y2=296)
    ], shape=image.shape)

ia.imshow(bbs.draw_on_image(image, size=3))


from imgaug import augmenters as iaa 
ia.seed(1)

seq = iaa.Sequential([
    iaa.GammaContrast(1.5),
    iaa.Affine(translate_percent={"x": 0.1}, scale=0.8),
    iaa.AdditiveGaussianNoise(scale=(10, 60)),
    iaa.Affine(rotate=(-30, 30))
])


image_aug, bbs_aug = seq(image=image, bounding_boxes=bbs)
ia.imshow(bbs_aug.draw_on_image(image_aug, size=2))

