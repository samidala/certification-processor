from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

def create_mock_certificate(output_path: str, data: dict):
    """
    Simulates a death certificate image by drawing text on a blank canvas.
    """
    img = Image.new('RGB', (800, 1000), color=(255, 255, 250))
    d = ImageDraw.Draw(img)
    
    # Simple layout
    d.text((300, 50), "CERTIFICATE OF DEATH", fill=(0,0,0))
    d.text((50, 150), f"First Name: {data['first_name']}", fill=(0,0,0))
    d.text((50, 200), f"Last Name: {data['last_name']}", fill=(0,0,0))
    d.text((50, 250), f"Date of Birth: {data['date_of_birth']}", fill=(0,0,0))
    d.text((50, 300), f"Date of Death: {data['date_of_death']}", fill=(0,0,0))
    d.text((50, 350), f"Cause of Death: {', '.join(data['cause_of_death'])}", fill=(0,0,0))
    d.text((50, 400), f"SSN (Last 4): {data['ssn_last_4']}", fill=(0,0,0))
    
    img.save(output_path)
    print(f"Created mock certificate: {output_path}")

if __name__ == "__main__":
    sample_data = {
        "first_name": "John",
        "last_name": "Doe",
        "date_of_birth": "1950-01-01",
        "date_of_death": "2023-05-15",
        "cause_of_death": ["Respiratory Failure", "Pneumonia"],
        "ssn_last_4": "1234"
    }
    Path("data/samples").mkdir(parents=True, exist_ok=True)
    create_mock_certificate("data/samples/sample_1.jpg", sample_data)
