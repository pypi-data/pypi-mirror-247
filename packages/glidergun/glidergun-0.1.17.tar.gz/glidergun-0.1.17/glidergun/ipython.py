import IPython
from typing import Union
from glidergun.core import Grid, Stack

ipython = IPython.get_ipython()  # type: ignore

if ipython:

    def html(obj: Union[Grid, Stack]):
        description = str(obj).replace("|", "<br />")
        if isinstance(obj, Grid):
            thumbnail = obj._thumbnail(obj._cmap)
            extent = obj.extent
        elif isinstance(obj, Stack):
            thumbnail = obj._thumbnail(*obj._rgb)
            extent = obj.grids[0].extent
        return f'<div>{description}</div><img src="{thumbnail}" /><div>{extent}</div>'

    formatter = ipython.display_formatter.formatters["text/html"]  # type: ignore
    formatter.for_type(Grid, html)
    formatter.for_type(Stack, html)
    formatter.for_type(
        tuple,
        lambda items: f"""
            <table>
                <tr style="text-align: left">
                    {"".join(f"<td>{html(item)}</td>" for item in items)}
                </tr>
            </table>
        """
        if all(isinstance(item, Grid) or isinstance(item, Stack) for item in items)
        else f"{items}",
    )
