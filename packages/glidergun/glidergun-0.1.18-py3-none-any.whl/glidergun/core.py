import dataclasses
import folium
import numpy as np
import rasterio
import warnings
from base64 import b64encode
from concurrent import futures
from dataclasses import dataclass
from io import BytesIO
from matplotlib import pyplot
from numpy import arctan, arctan2, cos, gradient, ndarray, pi, sin, sqrt
from numpy.lib.stride_tricks import sliding_window_view
from rasterio.crs import CRS
from rasterio.drivers import driver_from_extension
from rasterio.io import MemoryFile
from rasterio.transform import Affine
from rasterio.warp import calculate_default_transform, reproject, Resampling
from typing import Callable, Iterable, Iterator, List, Optional, Tuple, Union, overload
from glidergun.literals import ColorMap, DataType


class Extent(Tuple[float, float, float, float]):
    def __new__(cls, xmin: float, ymin: float, xmax: float, ymax: float):
        return super(Extent, cls).__new__(cls, (xmin, ymin, xmax, ymax))

    def intersect(self, extent: "Extent"):
        return Extent(*[f(x) for f, x in zip((max, max, min, min), zip(self, extent))])

    def union(self, extent: "Extent"):
        return Extent(*[f(x) for f, x in zip((min, min, max, max), zip(self, extent))])

    __and__ = intersect
    __rand__ = __and__
    __or__ = union
    __ror__ = __or__


Operand = Union["Grid", float, int]
Value = Union[float, int]


@dataclass(frozen=True)
class Grid:
    data: ndarray
    crs: CRS
    transform: Affine
    _cmap: ColorMap = "gray"

    def __post_init__(self):
        self.data.flags.writeable = False

    def __repr__(self):
        d = 3 if self.dtype.startswith("float") else 0
        return (
            f"image: {self.width}x{self.height} {self.dtype} | range: {self.min:.{d}f}~{self.max:.{d}f}"
            + f" | mean: {self.mean:.{d}f} | std: {self.std:.{d}f} | crs: {self.crs} | cell: {self.cell_size}"
        )

    @property
    def width(self) -> int:
        return self.data.shape[1]

    @property
    def height(self) -> int:
        return self.data.shape[0]

    @property
    def dtype(self) -> DataType:
        return str(self.data.dtype)  # type: ignore

    @property
    def nodata(self):
        if self.dtype == "bool":
            return None
        if self.dtype.startswith("float"):
            return np.finfo(self.dtype).min
        if self.dtype.startswith("uint"):
            return np.iinfo(self.dtype).max
        return np.iinfo(self.dtype).min

    @property
    def has_nan(self) -> bool:
        return self.is_nan().data.any()  # type: ignore

    @property
    def xmin(self) -> float:
        return self.transform.c

    @property
    def ymin(self) -> float:
        return self.ymax + self.height * self.transform.e

    @property
    def xmax(self) -> float:
        return self.xmin + self.width * self.transform.a

    @property
    def ymax(self) -> float:
        return self.transform.f

    @property
    def extent(self) -> Extent:
        return Extent(self.xmin, self.ymin, self.xmax, self.ymax)

    @property
    def mean(self) -> float:
        return np.nanmean(self.data)  # type: ignore

    @property
    def std(self) -> float:
        return np.nanstd(self.data)  # type: ignore

    @property
    def min(self) -> float:
        return np.nanmin(self.data)

    @property
    def max(self) -> float:
        return np.nanmax(self.data)

    @property
    def cell_size(self) -> float:
        return self.transform.a

    def __add__(self, n: Operand):
        return self._apply(self, n, np.add)

    __radd__ = __add__

    def __sub__(self, n: Operand):
        return self._apply(self, n, np.subtract)

    def __rsub__(self, n: Operand):
        return self._apply(n, self, np.subtract)

    def __mul__(self, n: Operand):
        return self._apply(self, n, np.multiply)

    __rmul__ = __mul__

    def __pow__(self, n: Operand):
        return self._apply(self, n, np.power)

    def __rpow__(self, n: Operand):
        return self._apply(n, self, np.power)

    def __truediv__(self, n: Operand):
        return self._apply(self, n, np.true_divide)

    def __rtruediv__(self, n: Operand):
        return self._apply(n, self, np.true_divide)

    def __floordiv__(self, n: Operand):
        return self._apply(self, n, np.floor_divide)

    def __rfloordiv__(self, n: Operand):
        return self._apply(n, self, np.floor_divide)

    def __mod__(self, n: Operand):
        return self._apply(self, n, np.mod)

    def __rmod__(self, n: Operand):
        return self._apply(n, self, np.mod)

    def __lt__(self, n: Operand):
        return self._apply(self, n, np.less)

    def __gt__(self, n: Operand):
        return self._apply(self, n, np.greater)

    __rlt__ = __gt__

    __rgt__ = __lt__

    def __le__(self, n: Operand):
        return self._apply(self, n, np.less_equal)

    def __ge__(self, n: Operand):
        return self._apply(self, n, np.greater_equal)

    __rle__ = __ge__

    __rge__ = __le__

    def __eq__(self, n: Operand):
        return self._apply(self, n, np.equal)

    __req__ = __eq__

    def __ne__(self, n: Operand):
        return self._apply(self, n, np.not_equal)

    __rne__ = __ne__

    def __and__(self, n: Operand):
        return self._apply(self, n, np.bitwise_and)

    __rand__ = __and__

    def __or__(self, n: Operand):
        return self._apply(self, n, np.bitwise_or)

    __ror__ = __or__

    def __xor__(self, n: Operand):
        return self._apply(self, n, np.bitwise_xor)

    def __rxor__(self, n: Operand):
        return self._apply(n, self, np.bitwise_xor)

    def __rshift__(self, n: Operand):
        return self._apply(self, n, np.right_shift)

    def __lshift__(self, n: Operand):
        return self._apply(self, n, np.left_shift)

    __rrshift__ = __lshift__

    __rlshift__ = __rshift__

    def __neg__(self):
        return self._create(-1 * self.data)

    def __pos__(self):
        return self._create(1 * self.data)

    def __invert__(self):
        return con(self, False, True)

    def _create(self, data: ndarray):
        return Grid(data, self.crs, self.transform)

    def _data(self, n: Operand):
        if isinstance(n, Grid):
            return n.data
        return n

    def _apply(self, left: Operand, right: Operand, op: Callable):
        if not isinstance(left, Grid) or not isinstance(right, Grid):
            return self._create(op(self._data(left), self._data(right)))

        if left.cell_size == right.cell_size and left.extent == right.extent:
            return self._create(op(left.data, right.data))

        l_adjusted, r_adjusted = _standardize(True, left, right)

        return self._create(op(l_adjusted.data, r_adjusted.data))

    def is_nan(self):
        return self.local(np.isnan)

    def local(self, func: Callable[[ndarray], ndarray]):
        return self._create(func(self.data))

    def focal(
        self,
        func: Callable[[np.ndarray], Value],
        buffer: int,
        circle: bool,
        max_workers: Optional[int] = 1,
    ):
        return _focal(func, buffer, circle, max_workers, self)

    def focal_mean(
        self, buffer=1, circle: bool = False, max_workers: Optional[int] = 1
    ) -> "Grid":
        return self.focal(np.mean, buffer, circle, max_workers)

    def focal_std(
        self, buffer=1, circle: bool = False, max_workers: Optional[int] = 1
    ) -> "Grid":
        return self.focal(np.std, buffer, circle, max_workers)

    def focal_min(
        self, buffer=1, circle: bool = False, max_workers: Optional[int] = 1
    ) -> "Grid":
        return self.focal(np.min, buffer, circle, max_workers)

    def focal_max(
        self, buffer=1, circle: bool = False, max_workers: Optional[int] = 1
    ) -> "Grid":
        return self.focal(np.max, buffer, circle, max_workers)

    def focal_sum(
        self, buffer=1, circle: bool = False, max_workers: Optional[int] = 1
    ) -> "Grid":
        return self.focal(np.sum, buffer, circle, max_workers)

    def _reproject(self, transform, crs, width, height, resampling: Resampling):
        grid = self.type("float64")
        destination = np.ones((round(height), round(width)), grid.dtype) * np.nan
        reproject(
            source=grid.data,
            destination=destination,
            src_transform=grid.transform,
            src_crs=grid.crs,
            src_nodata=grid.nodata,
            dst_transform=transform,
            dst_crs=crs,
            dst_nodata=grid.nodata,
            resampling=resampling,
        )
        result = Grid(destination, crs, transform)
        return con(result == result.nodata, np.nan, result)

    def project(
        self, epsg: Union[int, CRS], resampling: Resampling = Resampling.nearest
    ):
        crs = CRS.from_epsg(epsg) if isinstance(epsg, int) else epsg
        transform, width, height = calculate_default_transform(
            self.crs, crs, self.width, self.height, *self.extent
        )
        return self._reproject(transform, crs, width, height, resampling)

    def _resample(
        self,
        extent: Tuple[float, float, float, float],
        cell_size: float,
        resampling: Resampling,
    ):
        (xmin, ymin, xmax, ymax) = extent
        xoff = (xmin - self.xmin) / self.transform.a
        yoff = (ymax - self.ymax) / self.transform.e
        scaling = cell_size / self.cell_size
        transform = (
            self.transform * Affine.translation(xoff, yoff) * Affine.scale(scaling)
        )
        width = (xmax - xmin) / abs(self.transform.a) / scaling
        height = (ymax - ymin) / abs(self.transform.e) / scaling
        return self._reproject(transform, self.crs, width, height, resampling)

    def clip(self, extent: Tuple[float, float, float, float]):
        return self._resample(extent, self.cell_size, Resampling.nearest)

    def resample(self, cell_size: float, resampling: Resampling = Resampling.nearest):
        return self._resample(self.extent, cell_size, resampling)

    def abs(self):
        return self.local(np.abs)

    def zeros(self):
        return self.local(np.zeros_like)

    def ones(self):
        return self.local(np.ones_like)

    def random(self):
        return self._create(np.random.rand(self.height, self.width))

    def round(self, decimals: int = 0):
        return self.local(lambda data: np.round(data, decimals))

    def aspect(self):
        x, y = gradient(self.data)
        return self._create(arctan2(-x, y))

    def slope(self):
        x, y = gradient(self.data)
        return self._create(pi / 2.0 - arctan(sqrt(x * x + y * y)))

    def hillshade(self, azimuth: float = 315, altitude: float = 45):
        azimuth = np.deg2rad(azimuth)
        altitude = np.deg2rad(altitude)
        aspect = self.aspect().data
        slope = self.slope().data
        shaded = sin(altitude) * sin(slope) + cos(altitude) * cos(slope) * cos(
            azimuth - aspect
        )
        return self._create((255 * (shaded + 1) / 2))

    def buffer(self, value: Value, buffer: int):
        def f(data: List[ndarray]):
            if value in data[0]:
                return [value]
            return [data[0][1, 1]]

        g = self
        for i in range(buffer):
            g = focal(f, 1, False, g)[0]

        return g

    def fill_nan(self):
        grid = self
        n = 0
        while grid.has_nan:
            grid = con(grid.is_nan(), grid.focal_mean(2**n, True), grid)
            n += 1
        return grid

    def replace(self, value: Operand, replacement: Operand):
        return con(
            value if isinstance(value, Grid) else self == value, replacement, self
        )

    def set_nan(self, value: Operand):
        return self.replace(value, np.nan)

    def value(self, x: float, y: float) -> Value:
        xoff = (x - self.xmin) / self.transform.a
        yoff = (y - self.ymax) / self.transform.e
        if xoff < 0 or xoff >= self.width or yoff < 0 or yoff >= self.height:
            return np.nan
        return self.data[int(yoff), int(xoff)]

    def data_extent(self):
        xmin, ymin, xmax, ymax = None, None, None, None
        for x, y, _ in self.to_points():
            if not xmin or x < xmin:
                xmin = x
            if not ymin or y < ymin:
                ymin = y
            if not xmax or x > xmax:
                xmax = x
            if not ymax or y > ymax:
                ymax = y
        if xmin is None or ymin is None or xmax is None or ymax is None:
            raise ValueError("None of the cells has a value.")
        n = self.cell_size / 2
        return Extent(xmin - n, ymin - n, xmax + n, ymax + n)

    def shrink(self):
        return self.clip(self.data_extent())

    def to_points(self) -> Iterable[Tuple[float, float, Value]]:
        n = self.cell_size / 2
        for y, row in enumerate(self.data):
            for x, value in enumerate(row):
                if np.isfinite(value):
                    yield self.xmin + x * self.cell_size + n, self.ymax - y * self.cell_size - n, value

    def plot(self, cmap: ColorMap):
        return dataclasses.replace(self, _cmap=cmap)

    def map(
        self,
        cmap: ColorMap = "gray",
        opacity: float = 1.0,
        folium_map=None,
        width: int = 800,
        height: int = 600,
        basemap: str = "CartoDB positron",
        attribution: Optional[str] = None,
    ):
        return _map(
            self, cmap, opacity, folium_map, width, height, basemap, attribution
        )

    def type(self, dtype: DataType):
        return self.local(lambda data: np.asanyarray(data, dtype=dtype))

    @overload
    def save(self, file: str, driver: str = ""):
        ...

    @overload
    def save(self, file: MemoryFile, driver: str = ""):
        ...

    def save(self, file, driver: str = ""):
        if isinstance(file, str):
            with rasterio.open(
                file,
                "w",
                driver=driver if driver else driver_from_extension(file),
                count=1,
                **_metadata(self),
            ) as dataset:
                dataset.write(self.data, 1)
        elif isinstance(file, MemoryFile):
            with file.open(
                driver=driver if driver else "GTiff",
                count=1,
                **_metadata(self),
            ) as dataset:
                dataset.write(self.data, 1)


@overload
def grid(file: str, index: int = 1) -> Grid:
    ...


@overload
def grid(file: MemoryFile, index: int = 1) -> Grid:
    ...


def grid(file, index: int = 1) -> Grid:
    if isinstance(file, str):
        with rasterio.open(file) as dataset:
            return _read(dataset, index)
    elif isinstance(file, MemoryFile):
        with file.open() as dataset:
            return _read(dataset, index)
    raise ValueError()


def _read(dataset, index):
    grid = Grid(dataset.read(index), dataset.crs, dataset.transform)
    return grid


def _metadata(grid: Grid):
    return {
        "height": grid.height,
        "width": grid.width,
        "crs": grid.crs,
        "transform": grid.transform,
        "dtype": grid.data.dtype,
        "nodata": grid.nodata,
    }


def _mask(buffer: int) -> ndarray:
    size = 2 * buffer + 1
    rows = []
    for y in range(size):
        row = []
        for x in range(size):
            d = ((x - buffer) ** 2 + (y - buffer) ** 2) ** (1 / 2)
            row.append(1 if d <= buffer else np.nan)
        rows.append(row)
    return np.array(rows)


def _pad(data: ndarray, buffer: int):
    row = np.zeros((buffer, data.shape[1])) * np.nan
    col = np.zeros((data.shape[0] + 2 * buffer, buffer)) * np.nan
    return np.hstack([col, np.vstack([row, data, row]), col])


def _func(args):
    func, row, mask = args

    def f(data):
        d = data.ravel()
        return func(d[np.isfinite(d)])

    return [f(block if mask is None else block * mask) for block in row]


def _focal(
    func: Callable[[ndarray], Value],
    buffer: int,
    circle: bool,
    max_workers: Optional[int],
    grid: Grid,
):
    size = 2 * buffer + 1
    mask = _mask(buffer) if circle else None

    array = sliding_window_view(_pad(grid.data, buffer), (size, size))

    if max_workers == 1:
        result = list(map(_func, [(func, row, mask) for row in array]))
    else:
        with futures.ProcessPoolExecutor(max_workers) as executor:
            result = list(executor.map(_func, [(func, row, mask) for row in array]))

    return grid._create(np.array(result))


def focal(
    func: Callable[[List[ndarray]], List[Value]],
    buffer: int,
    circle: bool,
    *grids: Grid,
):
    grids_adjusted = _standardize(True, *grids)
    size = 2 * buffer + 1
    mask = _mask(buffer) if circle else None

    arrays = [
        sliding_window_view(_pad(g.data, buffer), (size, size)) for g in grids_adjusted
    ]

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        results = [
            [
                func([block if mask is None else block * mask for block in blocks])
                for blocks in row
            ]
            for row in np.array(arrays).transpose((1, 2, 0, 3, 4))
        ]

    return tuple(
        [
            grids_adjusted[0]._create(result)
            for result in np.transpose(np.array(results), axes=(2, 0, 1))
        ]
    )


def con(grid: Grid, trueValue: Operand, falseValue: Operand):
    return grid.local(
        lambda data: np.where(data, grid._data(trueValue), grid._data(falseValue))
    )


def aggregate(func: Callable, *grids: Grid) -> Grid:
    grids_adjusted = _standardize(True, *grids)
    data = func(np.array([grid.data for grid in grids_adjusted]), axis=0)
    return grids_adjusted[0]._create(data)


def mean(*grids: Grid) -> Grid:
    return aggregate(np.mean, *grids)


def std(*grids: Grid) -> Grid:
    return aggregate(np.std, *grids)


def minimum(*grids: Grid) -> Grid:
    return aggregate(np.min, *grids)


def maximum(*grids: Grid) -> Grid:
    return aggregate(np.max, *grids)


def mosaic(*grids: Grid) -> Grid:
    grids_adjusted = _standardize(False, *grids)
    result = grids_adjusted[0]
    for grid in grids_adjusted[1:]:
        result = con(result.is_nan(), grid, result)
    return result


def _standardize(intersect: bool, *grids: Grid) -> List[Grid]:
    if len(grids) == 1:
        return list(grids)

    crs_set = set(grid.crs for grid in grids)

    if len(crs_set) > 1:
        raise ValueError("Input grids must have the same CRS.")

    cell_size = 0
    extent = None

    for grid in grids:
        cell_size = grid.cell_size if grid.cell_size > cell_size else cell_size
        extent = (
            grid.extent
            if extent is None
            else extent & grid.extent
            if intersect
            else extent | grid.extent
        )

    results = []

    for grid in grids:
        if grid.cell_size != cell_size:
            grid = grid.resample(cell_size)
        if grid.extent != extent:
            grid = grid.clip(extent)  # type: ignore
        results.append(grid)

    return results


@dataclass(frozen=True)
class Stack:
    grids: Tuple[Grid, ...]
    _rgb: Tuple[int, int, int] = (1, 2, 3)

    def __repr__(self):
        g = self.grids[0]
        return f"image: {g.width}x{g.height} {g.dtype} | crs: {g.crs} | cell: {g.cell_size} | count: {len(self.grids)}"

    @property
    def width(self) -> int:
        return self.grids[0].width

    @property
    def height(self) -> int:
        return self.grids[0].height

    @property
    def dtype(self) -> DataType:
        return self.grids[0].dtype

    @property
    def xmin(self) -> float:
        return self.grids[0].xmin

    @property
    def ymin(self) -> float:
        return self.grids[0].ymin

    @property
    def xmax(self) -> float:
        return self.grids[0].xmax

    @property
    def ymax(self) -> float:
        return self.grids[0].ymax

    @property
    def cell_size(self) -> float:
        return self.grids[0].cell_size

    @property
    def extent(self) -> Extent:
        return self.grids[0].extent

    def plot(self, *rgb: int):
        return dataclasses.replace(self, _rgb=rgb)

    def map(
        self,
        rgb: Tuple[int, int, int] = (1, 2, 3),
        opacity: float = 1.0,
        folium_map=None,
        width: int = 800,
        height: int = 600,
        basemap: str = "CartoDB positron",
        attribution: Optional[str] = None,
    ):
        return _map(self, rgb, opacity, folium_map, width, height, basemap, attribution)

    def each(self, func: Callable[[Grid], Grid]):
        return stack(*map(func, self.grids))

    def project(
        self, epsg: Union[int, CRS], resampling: Resampling = Resampling.nearest
    ):
        return self.each(lambda g: g.project(epsg, resampling))

    def zip_with(self, other_stack: "Stack", func: Callable[[Grid, Grid], Grid]):
        grids = []
        for grid1, grid2 in zip(self.grids, other_stack.grids):
            grid1, grid2 = _standardize(True, grid1, grid2)
            grids.append(func(grid1, grid2))
        return stack(*grids)

    def values(self, x: float, y: float):
        return tuple(grid.value(x, y) for grid in self.grids)

    @overload
    def save(self, file: str, driver: str = ""):
        ...

    @overload
    def save(self, file: MemoryFile, driver: str = ""):
        ...

    def save(self, file, driver: str = ""):
        g = self.grids[0]
        if isinstance(file, str):
            with rasterio.open(
                file,
                "w",
                driver=driver if driver else driver_from_extension(file),
                count=len(self.grids),
                **_metadata(g),
            ) as dataset:
                for index, grid in enumerate(self.grids):
                    dataset.write(grid.data, index + 1)
        elif isinstance(file, MemoryFile):
            with file.open(
                driver=driver if driver else "GTiff",
                count=len(self.grids),
                **_metadata(g),
            ) as dataset:
                for index, grid in enumerate(self.grids):
                    dataset.write(grid.data, index + 1)


@overload
def stack(*grids: str) -> Stack:
    ...


@overload
def stack(*grids: MemoryFile) -> Stack:
    ...


@overload
def stack(*grids: Grid) -> Stack:
    ...


def stack(*grids) -> Stack:
    bands: List[Grid] = []

    for grid in grids:
        if isinstance(grid, Grid):
            bands.append(grid)
        else:
            with rasterio.open(grid) if isinstance(
                grid, str
            ) else grid.open() as dataset:
                for index in dataset.indexes:
                    band = _read(dataset, index)
                    bands.append(band)

    return Stack(tuple(_standardize(True, *bands)))


def _thumbnail(obj: Union[Grid, Stack], color):
    with BytesIO() as buffer:
        figure = pyplot.figure(frameon=False)
        axes = figure.add_axes((0, 0, 1, 1))
        axes.axis("off")
        if isinstance(obj, Grid):
            pyplot.imshow(obj.data, cmap=color)
        elif isinstance(obj, Stack):
            pyplot.imshow(
                np.dstack([obj.grids[i - 1].type("uint8").data for i in color])
            )
        pyplot.savefig(buffer)
        pyplot.close(figure)
        image = b64encode(buffer.getvalue()).decode()
        return f"data:image/png;base64, {image}"


def _map(
    obj: Union[Grid, Stack],
    color,
    opacity: float,
    folium_map,
    width: int,
    height: int,
    basemap: str,
    attribution: Optional[str],
):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        if isinstance(obj, Grid):
            obj = obj.project(4326)
        elif isinstance(obj, Stack):
            obj = obj.project(4326)

    figure = folium.Figure(width=str(width), height=height)
    bounds = [[obj.ymin, obj.xmin], [obj.ymax, obj.xmax]]

    if folium_map is None:
        tiles = folium.TileLayer(basemap, attr=attribution)
        folium_map = folium.Map(tiles=tiles).add_to(figure)
        folium_map.fit_bounds(bounds)

    folium.raster_layers.ImageOverlay(  # type: ignore
        image=_thumbnail(obj, color),
        bounds=bounds,
        opacity=opacity,
    ).add_to(folium_map)

    return folium_map
