import re
from io import BytesIO

from fastapi.exceptions import HTTPException
from PIL import Image, ImageDraw, ImageFont

from service_configs import service_configs


def make_ticket(img_file, color, attendee_name, offset, font_family, max_font_size, max_text_size, allow_multi_line=True) -> Image:  # noqa: FBT002
    #opens the image file and converts image to RGB mode
    img = Image.open(img_file, 'r').convert('RGB')
    imgdraw = ImageDraw.Draw(img)
    font_size = max_font_size

    def get_text_size(text, font):
        # multiline_text method to get text dimensions
        return imgdraw.multiline_textbbox((0, 0), text, font=font)[2]

    font = ImageFont.truetype(font_family, font_size)
    width = get_text_size(attendee_name, font)
    
    # checks if the name fits in the maximum font size
    while width > max_text_size:
        # replace spaces with newlines
        if font_size == max_font_size and allow_multi_line:
            attendee_name = attendee_name.replace(' ', '\n')
        else:
            font = ImageFont.truetype(font_family, font_size)

        width = get_text_size(attendee_name, font)
        font_size -= 1

    # Use multiline_text for drawing
    imgdraw.multiline_text(offset, attendee_name, color, font=font)
    return img


def get_buffer(stream, open_stream):
    """creates an in-memory buffer containing the PNG image data."""

    io = None
    if stream is not None:
        io = BytesIO()
        open_stream(stream, io)
        io.seek(0)
    return io

def generate_delegate_ticket(service: str, first_name: str, last_name: str):
    """generates a delegate ticket for a service and participant names."""

    service_config = service_configs.get(service)

    if service_config is None or service_config.ticket_config is None:
        raise HTTPException(status_code=404, detail="Requested service is unavailable")

    first_name = re.sub('([^A-z-]).+', '', first_name.strip()).upper()
    last_name = re.sub('([^A-z-]).+', '', last_name.strip()).upper()

    ticket_config = service_config.ticket_config

    single_line_name = f"{first_name} {last_name}"
    name = '{}{}{}'.format(first_name, '\n' if ticket_config.multi_line else ' ', last_name)

    img = make_ticket(
        ticket_config.registration_template,
        ticket_config.registration_color,
        name,
        ticket_config.offset,
        ticket_config.font_family,
        ticket_config.max_font_size,
        ticket_config.max_text_size,
        ticket_config.allow_multi_line
    )

    # return the in-memory image buffer and a formatted filename for the ticket
    return (
        get_buffer(img, lambda img, io: img.save(io, 'PNG')),
        f'{single_line_name} Confirmation Ticket.png'
    )
