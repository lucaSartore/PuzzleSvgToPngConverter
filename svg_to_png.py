import cairosvg

def svg_to_png(input_path: str, output_path: str, ppi: int = 1200):
  """Convert one SVG file to a PNG file with the requested ppi (Pixel per inch).

  Args:
    input_path: The path to the input SVG file.
    output_path: The path to the output PNG file.
    ppi: The PPI (Pixel per inch) of the output PNG file.
  """

  with open(input_path, "rb") as f:
    svg = f.read()

  cairosvg.svg2png(
      svg=svg,
      write_to=output_path,
      dpi=ppi,
      background_color="#ffffff"
  )
