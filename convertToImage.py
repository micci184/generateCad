import sys
from pdf2image import convert_from_path

def main():
	# コマンドライン引数でPDFファイルのパスを受け取る
	if len(sys.argv) != 2:
		print("Usage: python convertImage.py <PDF_FILE>")
		sys.exit(1)

	pdf_path = sys.argv[1]

	try:
		# PDFを画像に変換
		print(f"Converting PDF: {pdf_path}")
		images = convert_from_path(pdf_path, dpi=300)

		# 各ページをJPEG形式で保存
		for i, image in enumerate(images):
			image_path = f"page_{i + 1}.jpg"
			image.save(image_path, "JPEG")
			print(f"Saved: {image_path}")

		print("Conversion completed successfully!")

	except FileNotFoundError:
		print(f"Error: The file '{pdf_path}' was not found. Please check the path.")
	except Exception as e:
		print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
