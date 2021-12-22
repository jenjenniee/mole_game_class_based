import cv2
import os
import numpy as np
import mediapipe as mp
import numpy as np

from PIL import Image

mp_drawing = mp.solutions.drawing_utils
mp_selfie_segmentation = mp.solutions.selfie_segmentation
BG_COLOR = (192, 192, 192) # gray

def remove_bg_mediapipe_selfie(image):
  with mp_selfie_segmentation.SelfieSegmentation(
      model_selection=1) as selfie_segmentation:
    
    bg_image = None

    # Flip the image horizontally for a later selfie-view display, and convert
    # the BGR image to RGB.
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    results = selfie_segmentation.process(image)

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Draw selfie segmentation on the background image.
    # To improve segmentation around boundaries, consider applying a joint
    # bilateral filter to "results.segmentation_mask" with "image".um
    condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1
    # The background can be customized.
    #   a) Load an image (with the same width and height of the input image) to
    #      be the background, e.g., bg_image = cv2.imread('/path/to/image/file')
    #   b) Blur the input image by applying image filtering, e.g.,
    #      bg_image = cv2.GaussianBlur(image,(55,55),0)
    if bg_image is None:
      bg_image = np.zeros(image.shape, dtype=np.uint8)
      bg_image[:] = BG_COLOR
    
    output_image = np.where(condition, image, bg_image)
    
    return output_image
    
def remove_bg_grabCut(img_dir):
    
    # 참고 블로그
    # https://velog.io/@jaehyeong/OpenCV%EB%A5%BC-%ED%99%9C%EC%9A%A9%ED%95%9C-%EA%B8%B0%EC%B4%88-%EC%9D%B4%EB%AF%B8%EC%A7%80-%EC%B2%98%EB%A6%AC-with-Python
    
    # 이미지 로드 후 RGB로 변환
    image_bgr = cv2.imread(img_dir)
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    
    rows, cols, _ = image_rgb.shape
    print(f'rows: {rows}, cols: {cols}')
    
    rectangle = (0, 0, 800, 600)

    # 초기 마스크 생성
    mask = np.zeros(image_rgb.shape[:2], np.uint8)

    # grabCut에 사용할 임시 배열 생성
    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)

    # grabCut 실행
    cv2.grabCut(image_rgb,  # 원본 이미지
            mask,           # 마스크
            rectangle,      # 사각형
            bgdModel,       # 배경을 위한 임시 배열
            fgdModel,       # 전경을 위한 임시 배열 
            10,              # 반복 횟수
            cv2.GC_INIT_WITH_RECT) # 사각형을 위한 초기화
    
    # 배경인 곳은 0, 그 외에는 1로 설정한 마스크 생성
    mask_2 = np.where((mask==2) | (mask==0), 0, 1).astype('uint8')

    # 이미지에 새로운 마스크를 곱행 배경을 제외
    image_rgb_nobg = image_rgb * mask_2[:, :, np.newaxis]

    # plot
    cv2.imshow('result - removed img', image_rgb_nobg)
    
    cv2.waitKey()
    cv2.destroyAllWindows()

    return image_rgb_nobg


def remove_bg_PIL(img_dir):
    
    # 참고 블로그: 
    #   http://minsone.github.io/programming/how-to-replace-from-white-to-transparent-image
    
    img = Image.open(img_dir)
    img = img.convert("RGBA")
    datas = img.getdata()

    newData = []
    for item in datas:
        if item[0] > 200 and item[1] > 200 and item[2] > 200:
            newData.append((item[0], item[1], item[2], 0))
        else:
            newData.append(item)

    img.putdata(newData)

    newData_np = np.array(img)
    newData_opencv = cv2.cvtColor(newData_np, cv2.COLOR_RGB2BGRA)
    
    filename = os.path.splitext(img_dir)
    save_path = filename[0] + "_output" + filename[1]
    img.save(save_path, "PNG")
    print(f'Processed file is saved --> {save_path}')
    
    img_removed_bg = cv2.imread(save_path, cv2.IMREAD_UNCHANGED)
    # img_removed_bg = cv2.imread(save_path, cv2.IMREAD_COLOR)
    
    # cv2.imshow('result - removed img', img_removed_bg)
    # cv2.waitKey()
    # cv2.destroyAllWindows()
    
    return img_removed_bg
    # return newData_opencv


if __name__=='__main__':
    
    bg_dir = './imgs/bg_yellow.png'
    top_dir = './imgs/mole_jklee_no_bg.png'
    
    print('Bye, end of computation ^^')
    