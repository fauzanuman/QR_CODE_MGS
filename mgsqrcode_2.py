import qrcode
from PIL import Image, ImageDraw, ImageFont
import datetime
import os

def generate_custom_qr(url, 
                       filename=None, 
                       logo_path=None, 
                       text_below=None, 
                       text_above=None, 
                       fill_color="black", 
                       back_color="white", 
                       qr_version=1, 
                       error_correction=qrcode.constants.ERROR_CORRECT_H,
                       output_size=(1000, 1000),
                       font_path="Inter-Bold.ttf",    # Custom font path
                       font_size=40,                  # Custom font size
                       qr_margin=30,                  # Margin around the QR code
                       text_margin=10,                # Margin between QR code and text
                       border_margin=10):             # Margin between text and outer border
    
    # Create a QR code instance
    qr = qrcode.QRCode(
        version=qr_version,
        error_correction=error_correction,  # High error correction for robustness
        box_size=20,  # Larger box size for higher resolution
        border=6,     # Border around the QR code
    )
    qr.add_data(url)
    qr.make(fit=True)

    # Generate QR code image with custom colors
    img = qr.make_image(fill=fill_color, back_color=back_color).convert('RGB')
    print("QR code generated!")

    # Add a logo to the QR code (if provided and path exists)
    if logo_path:
        if os.path.exists(logo_path):
            print("Adding logo to QR code...")
            logo = Image.open(logo_path).convert("RGBA")  # Handle transparency
            logo_size = (120, 120)  # Adjust logo size
            logo = logo.resize(logo_size)

            # Calculate position to center the logo
            img_w, img_h = img.size
            logo_w, logo_h = logo.size
            pos = ((img_w - logo_w) // 2, (img_h - logo_h) // 2)

            # Paste the logo with transparency mask
            img.paste(logo, pos, logo)
            print("Logo added!")
        else:
            print(f"Error: The logo file at {logo_path} does not exist.")

    # Create a new image for the final output
    total_height = img.size[1] + (text_margin * 2) + border_margin * 2
    output_img = Image.new('RGB', (img.size[0], total_height), back_color)

    # Paste the QR code into the new image
    output_img.paste(img, (0, text_margin + border_margin))

    # Add additional text above the QR code (if provided)
    if text_above:
        print("Adding text above QR code...")
        draw = ImageDraw.Draw(output_img)
        try:
            # Load custom font
            font = ImageFont.truetype(font_path, font_size)
        except:
            print("Error loading font, using default.")
            font = ImageFont.load_default()

        # Use textbbox to calculate the size of the text
        text_bbox = draw.textbbox((0, 0), text_above, font=font)
        text_w = text_bbox[2] - text_bbox[0]
        img_w = output_img.size[0]
        
        # Add text above the QR code with margins
        draw.text(((img_w - text_w) // 2, border_margin), text_above, fill="black", font=font)
        print("Text above added!")

    # Add text below the QR code (if provided)
    if text_below:
        print("Adding text below QR code...")
        draw = ImageDraw.Draw(output_img)
        text_bbox = draw.textbbox((0, 0), text_below, font=font)
        text_w = text_bbox[2] - text_bbox[0]
        img_w = output_img.size[0]
        
        # Add text below the QR code with margins
        draw.text(((img_w - text_w) // 2, total_height - text_bbox[1] - border_margin), text_below, fill="black", font=font)
        print("Text below added!")

    # Resize image for higher output resolution
    output_img = output_img.resize(output_size, Image.Resampling.LANCZOS)  # High-quality resizing

    # Create dynamic filename using input text above and current date
    if filename is None:
        timestamp = datetime.datetime.now().strftime("%d%m%y")
        safe_text_above = "".join(c for c in text_above if c.isalnum() or c in (' ', '_')).strip().replace(' ', '_')  # Clean text for filename
        filename = f"MGSQRCODE_{timestamp}_{safe_text_above}.png"

    # Save the QR code image
    output_img.save(filename)
    print(f"QR code saved as {filename}")

# Continuous loop to keep the application running
if __name__ == "__main__":
    while True:
        url = input("Masukkan alamat URL (atau ketik 'exit' untuk keluar): ")
        if url.lower() == 'exit':
            print("Exiting the application.")
            break

        text_above = input("Masukkan Nama Kode QR: ")  # User input for text above
        text_below = "MGS QR CODE GEN©"  # Fixed text below
        logo_path = r"C:\Users\Fauzan\OneDrive\문서\sinaukoding\qrcodegenerator\QR code MGS\Main-Logo.png"  # Update to your logo path

        # Provide the path to the font you want to use
        font_path = r"C:\Users\Fauzan\OneDrive\문서\sinaukoding\qrcodegenerator\QR code MGS\Inter-Bold.ttf"  # Replace with your font path
        font_size = 20  # Set font size

        generate_custom_qr(
            url=url,
            logo_path=logo_path,       # Optional logo path
            text_below=text_below,     # Optional text below the QR code
            text_above=text_above,     # User-provided text above the QR code
            fill_color="blue",         # Foreground color
            back_color="white",        # Background color
            qr_version=5,              # Controls the size of the QR code
            error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction for logos
            output_size=(2000, 2000),  # Custom output image size for high resolution
            font_path=font_path,       # Use the custom font path
            font_size=font_size,       # Set the font size
            qr_margin=30,              # Margin around the QR code
            text_margin=50,            # Increase space between QR code and text
            border_margin=50           # Margin between text and outer border
        )

        print("QR code generated. You can generate another one or type 'exit' to quit.")
