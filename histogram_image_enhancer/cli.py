#!/usr/bin/env python

import click
import cv2
from pathlib import Path

from .config import RESULTS_DIR, LOG_FILE
from .core.utils import setup_logger, load_image
from .core.enhancement import process_image
from .core.visualization import save_comparison

logger = setup_logger("histogram_enhancer_cli", LOG_FILE)

@click.command(
    help="Enhance the histogram of an image using equalize, CLAHE, gamma correction, "
         "contrast adjustment, or histogram matching."
)
@click.argument("input_file", type=click.Path(exists=True, dir_okay=False))
@click.option(
    "--method",
    type=click.Choice(["equalize", "clahe", "gamma", "contrast", "match"]),
    default="equalize",
    show_default=True,
    help="Enhancement method."
)
@click.option("--clip-limit",   default=2.0, show_default=True, help="Contrast limit for CLAHE.")
@click.option(
    "--tile-size",
    default="8,8",
    show_default=True,
    help="Tile size for CLAHE (width,height)."
)
@click.option("--gamma",        default=1.0, show_default=True, help="Gamma value for gamma correction.")
@click.option(
    "--alpha",
    default=1.0,
    show_default=True,
    help="Alpha (contrast) value for contrast adjustment."
)
@click.option(
    "--beta",
    default=0,
    show_default=True,
    help="Beta (brightness) value for contrast adjustment."
)
@click.option(
    "--reference-file",
    type=click.Path(exists=True, dir_okay=False),
    help="Reference image for histogram matching."
)
def main(
    input_file,
    method,
    clip_limit,
    tile_size,
    gamma,
    alpha,
    beta,
    reference_file
):
    """
    Entry point of the CLI.
    """
    # Parse CLAHE parameters
    tile = tuple(map(int, tile_size.split(",")))

    # Load original image
    img = load_image(Path(input_file))

    # For histogram matching, also load the reference image
    ref_img = None
    if method == "match":
        if not reference_file:
            raise click.UsageError(
                "When selecting --method match, you must provide --reference-file"
            )
        ref_img = load_image(Path(reference_file))

    # Process image
    result = process_image(
        img,
        method=method,
        clip_limit=clip_limit,
        tile_size=tile,
        gamma=gamma,
        alpha=alpha,
        beta=beta,
        reference=ref_img
    )

    # Save result
    out_path = RESULTS_DIR / Path(input_file).name
    cv2.imwrite(str(out_path), result)
    logger.info("Processed -> %s", out_path)
    click.echo(f"Processed image saved at: {out_path}")

    # Save comparison image
    comp_path = RESULTS_DIR / f"{Path(input_file).stem}_comparison.png"
    save_comparison(img, result, comp_path)
    logger.info("Comparison -> %s", comp_path)
    click.echo(f"Comparison saved at: {comp_path}")


if __name__ == "__main__":
    main()
