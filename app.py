from typing import Annotated

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

lengthUnits = {
    "mm": 0.01,
    "cm": 0.1,
    "m": 1,
    "in.": 0.025,
    "ft": 0.3,
    "yd": 0.91,
    "mi": 1609.34,
}

weightUnits = {"mg": 0.001, "g": 1, "kg": 1000, "oz": 28.35, "lb": 453.59}

temperatureUnits = {"°C": 274.15, "°F": 255.927778, "K": 1}


def convertValue(num: float, unitFrom: str, unitTo: str) -> int:
    return 0


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
async def convertLength(request: Request, data: Annotated[FormData, Form()]):
    convertedValue = convertValue(data.value, data.unitFrom, data.unitTo)
    return templates.TemplateResponse(
        request,
        "result.html",
        {
            **data.model_dump(),
            "convertedValue": convertedValue,
            "href": "/length",
        },
    )


@app.post("/weight", response_class=HTMLResponse)
async def convertWeight(request: Request, data: Annotated[FormData, Form()]):
    convertedValue = convertValue(data.value, data.unitFrom, data.unitTo)
    return templates.TemplateResponse(
        request,
        "result.html",
        {**data.model_dump(), "convertedValue": convertedValue, "href": "/weight"},
    )


@app.post("/temperature", response_class=HTMLResponse)
async def convertTemperature(request: Request, data: Annotated[FormData, Form()]):
    convertedValue = convertValue(data.value, data.unitFrom, data.unitTo)
    return templates.TemplateResponse(
        request,
        "result.html",
        {**data.model_dump(), "convertedValue": convertedValue, "href": "/temperature"},
    )
