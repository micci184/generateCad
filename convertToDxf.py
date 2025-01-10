import sys
import cv2
import ezdxf
import os

def preprocess_image(image_path):
    # 画像の読み込み
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: '{image_path}' が見つからないか、読み込めません。")
        sys.exit(1)

    # グレースケール変換
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # ノイズ除去（Gaussian Blur）
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # 二値化（Adaptive Threshold）
    thresh = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV, 11, 2
    )

    return thresh

def image_to_dxf(image_path, dxf_path):
    # 画像の前処理
    processed_img = preprocess_image(image_path)

    # エッジ検出（Canny法の閾値を調整）
    edges = cv2.Canny(processed_img, 30, 100, apertureSize=3)

    # 輪郭検出（細かい線も拾う）
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # DXFファイルの作成
    doc = ezdxf.new()
    msp = doc.modelspace()

    # 輪郭をポリラインとしてDXFに追加
    for contour in contours:
        points = [(point[0][0], -point[0][1]) for point in contour]
        if len(points) > 1:
            msp.add_lwpolyline(points, close=True)

    # DXFファイルの保存
    doc.saveas(dxf_path)
    print(f"✅ DXFファイルを保存しました: {dxf_path}")

def main():
    # コマンドライン引数のチェック
    if len(sys.argv) != 2:
        print("Usage: python convertToDxf.py <IMAGE_FILE>")
        sys.exit(1)

    image_path = sys.argv[1]
    base_name = os.path.splitext(image_path)[0]
    dxf_path = f"{base_name}_improved.dxf"

    # 変換処理の実行
    image_to_dxf(image_path, dxf_path)

if __name__ == "__main__":
    main()
