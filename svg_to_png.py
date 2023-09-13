import cairosvg

def svg_to_png(input_path: str, output_path: str, dpi: int = 1200):
  """Convert one SVG file to a PNG file with the requested ppi (Pixel per inch).

  Args:
    input_path: The path to the input SVG file.
    output_path: The path to the output PNG file.
    ppi: The PPI (Pixel per inch) of the output PNG file.
  """


  cairosvg.svg2png(
      url=input_path,
      write_to=output_path,
      dpi=dpi,
      background_color="white"
  )

if __name__ == "__main__":
  svg_to_png(r".\SVGs\8x8.svg",r".\PNGs\8x8.png")