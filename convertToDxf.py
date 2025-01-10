import sys
import cv2
import ezdxf
import os

def image_to_dxf(image_path, dxf_path):
    # 画像の読み込みとグレースケール化
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: '{image_path}' が見つからないか、読み込めません。")
        sys.exit(1)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # エッジ検出（Canny法）
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    # 輪郭検出
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # DXFファイルの作成
    doc = ezdxf.new()
    msp = doc.modelspace()

    # 輪郭をポリラインとしてDXFに追加
    for contour in contours:
        points = [(point[0][0], -point[0][1]) for point in contour]  # Y軸反転
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

    # 拡張子をDXFに変更
    base_name = os.path.splitext(image_path)[0]
    dxf_path = f"{base_name}.dxf"

    # 変換処理の実行
    image_to_dxf(image_path, dxf_path)

if __name__ == "__main__":
    main()
