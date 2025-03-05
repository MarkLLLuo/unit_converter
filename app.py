from typing import Annotated

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

lengthUnits = {
    "mm": 0.001,
    "cm": 0.01,
    "m": 1,
    "km": 1000,
    "in.": 0.0254,
    "ft": 0.3048,
    "yd": 0.9144,
    "mi": 1609.344,
}

weightUnits = {"mg": 0.001, "g": 1, "kg": 1000, "oz": 28.3495, "lb": 453.5924}

temperatureUnits = {"°C": 274.15, "°F": 255.927778, "K": 1}


def convertValue(num: float, unitFrom: str, unitTo: str) -> float:
    if unitFrom in lengthUnits.keys():
        return num * lengthUnits[unitFrom] / lengthUnits[unitTo]
    elif unitFrom in weightUnits.keys():
        return num * weightUnits[unitFrom] / weightUnits[unitTo]
    else:
        return num * temperatureUnits[unitFrom] / temperatureUnits[unitTo]


app = FastAPI()

templates = Jinja2Templates(directory="templates")


class FormData(BaseModel):
    unitFrom: Annotated[str, Form()]
    unitTo: Annotated[str, Form()]
    value: Annotated[float, Form()]


class FormResult(FormData):
    convertedValue: Annotated[float, Form()]
    href: Annotated[str, Form()]


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/length", response_class=HTMLResponse)
async def lengthPage(request: Request):
    return templates.TemplateResponse(
        request, "length.html", {"units": lengthUnits.keys()}
    )


@app.get("/weight", response_class=HTMLResponse)
async def weightPage(request: Request):
    return templates.TemplateResponse(
        request, name="weight.html", context={"units": weightUnits.keys()}
    )


@app.get("/temperature", response_class=HTMLResponse)
async def temperaturePage(request: Request):
    return templates.TemplateResponse(
        request, name="temperature.html", context={"units": temperatureUnits.keys()}
    )


@app.post("/length", response_class=HTMLResponse)
@app.post("/weight", response_class=HTMLResponse)
@app.post("/temperature", response_class=HTMLResponse)
async def convertLength(request: Request, data: Annotated[FormData, Form()]):
    convertedValue = convertValue(data.value, data.unitFrom, data.unitTo)
    if data.unitFrom in lengthUnits:
        href = "/length"
    elif data.unitFrom in weightUnits:
        href = "/weight"
    else:
        href = "/temperature"
    return templates.TemplateResponse(
        request,
        "result.html",
        {
            **data.model_dump(),
            "convertedValue": convertedValue,
            "href": href,
        },
    )
