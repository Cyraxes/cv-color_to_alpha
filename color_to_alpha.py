from PIL import Image
import numpy as np


def color_to_alpha(image, color, transparency_threshold, opacity_threshold):
    rgba_image = image.convert("RGBA")
    data = np.array(rgba_image)

    r = data[:, :, 0]
    g = data[:, :, 1]
    b = data[:, :, 2]
    a = data[:, :, 3]


    r_alpha = value_to_alpha(r, color[0], transparency_threshold, opacity_threshold)
    g_alpha = value_to_alpha(g, color[1], transparency_threshold, opacity_threshold)
    b_alpha = value_to_alpha(b, color[2], transparency_threshold, opacity_threshold)
    
    new_alpha = (np.maximum(r_alpha,b_alpha,g_alpha)*a).astype('int8')

    data[:, :, 3] = new_alpha  # Set the alpha channel to the filtered values

    rgba_image = Image.fromarray(data, 'RGBA')

    return rgba_image





def value_to_alpha(image_value_raw, color_value_raw, transparency_threshold, opacity_threshold, scale = 255):
    image_value = image_value_raw/scale
    color_value = color_value_raw/scale

    cv_ot_left = max(0, color_value - opacity_threshold)
    cv_ot_right = min(1, color_value + opacity_threshold)
    cv_tt_left = max(0, color_value - transparency_threshold)
    cv_tt_right = min(1, color_value + transparency_threshold)
    
    
    condition_1 = (cv_tt_left <= image_value) & (image_value <= cv_tt_right)
    condition_2 = (image_value < cv_ot_left) | (image_value > cv_ot_right)
    condition_3 = (cv_ot_left <= image_value) & (image_value <= cv_tt_left)
    condition_4 = (cv_tt_right <= image_value) & (image_value <= cv_ot_right)
    
    result = (
        (condition_1 * 0) +
        (condition_2 * 1) +
        (condition_3 * (cv_tt_left - image_value) / (opacity_threshold - transparency_threshold)) +
        (condition_4 * (image_value - cv_tt_right) / (opacity_threshold - transparency_threshold))
    )

    return result


input_image = Image.open("AE8158DL.jpeg")
new_image = color_to_alpha(input_image, (255, 255, 255), 0.1, 0.5)
new_image.save("output_image.png")

print(value_to_alpha(255, 255, 0, 0.5, scale = 255))
pass