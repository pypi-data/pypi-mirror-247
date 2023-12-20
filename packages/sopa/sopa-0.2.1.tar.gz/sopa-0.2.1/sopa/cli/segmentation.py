import typer

from .utils import SDATA_HELPER

app_segmentation = typer.Typer()


@app_segmentation.command()
def cellpose(
    sdata_path: str = typer.Argument(help=SDATA_HELPER),
    diameter: float = typer.Option(help="Cellpose diameter parameter"),
    channels: list[str] = typer.Option(
        help="Names of the channels used for Cellpose. If one channel, then provide just a nucleus channel. If two channels, this is the nucleus and then the cytoplasm channel"
    ),
    flow_threshold: float = typer.Option(help="Cellpose `flow_threshold` parameter"),
    cellprob_threshold: float = typer.Option(help="Cellpose `cellprob_threshold` parameter"),
    model_type: str = typer.Option("cyto2", help="Name of the cellpose model"),
    min_area: int = typer.Option(
        0, help="Minimum area (in pixels^2) for a cell to be considered as valid"
    ),
    clip_limit: float = typer.Option(
        0.01,
        help="Parameter for skimage.exposure.equalize_adapthist (applied before running cellpose)",
    ),
    gaussian_sigma: float = typer.Option(
        1, help="Parameter for scipy gaussian_filter (applied before running cellpose)"
    ),
    patch_index: int = typer.Option(
        default=None,
        help="Index of the patch on which cellpose should be run. NB: the number of patches is `len(sdata['sopa_patches'])`",
    ),
    patch_dir: str = typer.Option(
        default=None,
        help="Path to the temporary cellpose directory inside which we will store each individual patch segmentation",
    ),
    patch_width: int = typer.Option(
        default=None, help="Ignore this if you already run `sopa patchify`. Patch width in pixels"
    ),
    patch_overlap: int = typer.Option(
        default=None,
        help="Ignore this if you already run `sopa patchify`. Patches overlaps in pixels",
    ),
):
    """Perform cellpose segmentation. This can be done on all patches directly, or on one individual patch.

    Usage:

        - [On one patch] Use this mode to run patches in parallel. Just provide `--patch-index` and `--patch-dir`. Note that `--patch-dir` will be used during `sopa resolve cellpose` afterwards.

        - [On all patches at once] For small images, you can run cellpose sequentially (no need to run `sopa patchify`). You need to provide `--patch-width` and `--patch-overlap`
    """
    from sopa._constants import SopaKeys
    from sopa.io.standardize import read_zarr_standardized
    from sopa.segmentation.methods import cellpose_patch
    from sopa.segmentation.stainings import StainingSegmentation

    sdata = read_zarr_standardized(sdata_path)

    method = cellpose_patch(
        diameter,
        channels,
        flow_threshold=flow_threshold,
        cellprob_threshold=cellprob_threshold,
        model_type=model_type,
    )
    segmentation = StainingSegmentation(
        sdata,
        method,
        channels,
        min_area=min_area,
        clip_limit=clip_limit,
        gaussian_sigma=gaussian_sigma,
    )

    if patch_index is not None:
        segmentation.write_patch_cells(patch_dir, patch_index)
        return

    cells = segmentation.run_patches(patch_width, patch_overlap)

    StainingSegmentation.add_shapes(
        sdata, cells, segmentation.image_key, SopaKeys.CELLPOSE_BOUNDARIES
    )
