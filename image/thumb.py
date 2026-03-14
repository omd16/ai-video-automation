import os.path

from PIL import Image, ImageDraw, ImageFont
import re

# from config.app_config import Config


def add_text_to_image(image_path, output_path, text, font_path="arial.ttf", font_size=40,
                      margin_top=20, margin_bottom=20, margin_left=20, margin_right=20,
                      highlight_bg="yellow", text_color="black", underline_color=None,
                      border_color="black", border_width=10,
                      highlight_lines=2, line_spacing=5, bold=False):
    # Load image
    image = Image.open(image_path)
    img_width, img_height = image.size

    # Create a new image with a border
    bordered_image = Image.new("RGB", (img_width + 2 * border_width, img_height + 2 * border_width), border_color)
    bordered_image.paste(image, (border_width, border_width))
    draw = ImageDraw.Draw(bordered_image)

    # Use bold font if available
    if bold and "arial" in font_path.lower():
        font_path = "arialbd.ttf"  # Use Arial Bold if using Arial

    font = ImageFont.truetype(font_path, font_size)

    # Calculate text wrapping width based on image width and margins
    max_text_width = img_width - (margin_left + margin_right)

    # Ensure words with dots remain together
    words = re.split(r'(\s+)', text)  # Keeps spaces intact

    # Wrap text manually
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word
        bbox = draw.textbbox((0, 0), test_line, font=font)
        line_width = bbox[2] - bbox[0]

        if line_width <= max_text_width:
            current_line = test_line  # Add word to current line
        else:
            lines.append(current_line.strip())  # Store current line
            current_line = word  # Start a new line with the current word

    if current_line:
        lines.append(current_line.strip())  # Add last line

    # Calculate starting position
    x = margin_left + border_width
    y = margin_top + border_width
    max_lines = (img_height - margin_top - margin_bottom) // (font_size + line_spacing)

    # Adjust lines to fit within the image
    if len(lines) > max_lines:
        lines = lines[:max_lines]  # Keep only the visible lines
        lines[-1] = lines[-1].rstrip() + "..."  # Add ellipsis to the last visible line

    # Draw text on image
    for i, line in enumerate(lines):
        bbox = draw.textbbox((x, y), line, font=font)
        line_width = bbox[2] - bbox[0]
        line_height = bbox[3] - bbox[1]

        # Highlight first few lines
        if i < highlight_lines:
            extra_pad = 25
            draw.rectangle([x, y+ extra_pad -5, x + line_width + 10, y + line_height+ extra_pad], fill=highlight_bg)

        # Draw bold text (if enabled)
        if bold:
            offsets = [(0, 0), (1, 0), (0, 1), (-1, 0), (0, -1)]  # Offsets to simulate thickness
            for offset in offsets:
                draw.text((x + offset[0], y + offset[1]), line, font=font, fill=text_color)
        else:
            draw.text((x, y), line, font=font, fill=text_color)

        # Underline all lines **except** the highlighted ones
        if i >= highlight_lines:
            underline_y = bbox[3] + 2  # Exact bottom position of text
            draw.line([x, underline_y, x + line_width, underline_y],
                      fill=underline_color if underline_color else highlight_bg, width=6)

        y += line_height + line_spacing  # Configurable line spacing

    # Convert image to RGB if saving as JPEG
    if output_path.lower().endswith(".jpg") or output_path.lower().endswith(".jpeg"):
        bordered_image = bordered_image.convert("RGB")

    # Save image
    bordered_image.save(output_path)
    print(f"Image saved to {output_path}")


def create_thumb(text, output_path, config):
# Example usage
    add_text_to_image(
        image_path= os.path.join(config.thumb.dir, config.thumb.name),
        output_path= output_path,
        text= text,
        font_path="verdana.ttf",
        font_size=110,
        margin_top=310,
        margin_bottom=30,
        margin_left=50,
        margin_right=50,
        highlight_bg="pink",
        text_color="black",
        underline_color="pink",  # Custom underline color
        border_color="pink",  # Custom border color
        border_width=5,  # Border thickness
        line_spacing=20,  # Customizable line height
        bold=True  # Enable bold text
    )

def create_thumb_scr(text, output_path):
# Example usage
    add_text_to_image(
        image_path= os.path.join("zimages", "template.png"),
        output_path= output_path,
        text= text,
        font_path="verdana.ttf",
        font_size=110,
        margin_top=350,
        margin_bottom=30,
        margin_left=50,
        margin_right=50,
        highlight_bg="pink",
        text_color="black",
        underline_color="pink",  # Custom underline color
        border_color="pink",  # Custom border color
        border_width=5,  # Border thickness
        line_spacing=30,  # Customizable line height
        bold=True  # Enable bold text
    )

create_thumb_scr("My Husband Cheated with My Sister—So I Made Sure Their Wedding Was Ruined...", "./working-dir/story_1/thumb.jpg")