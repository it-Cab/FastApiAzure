import json
import logging
from fastapi import HTTPException
from fastapi import FastAPI

from app.models.base_model import AreaModel, TruckModel, Item
from app.controller.resource_manager import ResourceManager
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse, JSONResponse

app = FastAPI()


resource_manager = ResourceManager()
area_key = "areas"
truck_key = "trucks"
assignment_key = "assignments"


@app.get("/")
async def read_item():
    return {"message": "Welcome to our app"}


@app.get("/api/areas/{area_id}")
async def get_area_by_id(area_id: str) -> AreaModel:
    area = resource_manager.get_area_by_id(area_key, area_id)
    if area:
        body = {"area: ": area}
        return JSONResponse(status_code=200, content=body)
    raise HTTPException(status_code=404, detail="Area not found")


@app.get("/api/areas")
async def get_areas() -> list[AreaModel]:
    areas = resource_manager.get_areas(area_key)
    if areas:
        body = {"areas: ": areas}
        return JSONResponse(status_code=200, content=body)
    raise HTTPException(status_code=404, detail="Area data not found")


@app.post("/api/areas")
async def add_area(payload: list[AreaModel]):
    res = resource_manager.add_areas(area_key, payload)
    return JSONResponse(
        status_code=200 if res else 500,
        content={
            "message": (
                "Store Area to Redis success" if res else "Store Area to Redis fail"
            )
        },
    )


@app.get("/api/trucks/{truck_id}")
async def get_truck_by_id(truck_id) -> TruckModel:
    truck = resource_manager.get_truck_by_id(truck_key, truck_id)
    if truck:
        body = {"truck: ": truck}
        return JSONResponse(status_code=200, content=body)
    raise HTTPException(status_code=404, detail="Truck not found")


@app.get("/api/trucks")
async def get_trucks() -> list[TruckModel]:
    trucks = resource_manager.get_trucks(truck_key)
    if trucks:
        body = {"trucks: ": trucks}
        return JSONResponse(status_code=200, content=body)
    raise HTTPException(status_code=404, detail="Truck data not found")


@app.post("/api/trucks")
async def add_truck(payload: list[TruckModel]):
    res = resource_manager.add_trucks(truck_key, payload)
    return JSONResponse(
        status_code=200 if res else 500,
        content={
            "message": (
                "Store Truck to Redis success" if res else "Store Truck to Redis fail"
            )
        },
    )


@app.post("/api/assignments")
async def add_assignments():
    res = resource_manager.add_assignments(assignment_key, area_key, truck_key)
    return JSONResponse(
        status_code=200 if res else 500,
        content={
            "message": (
                "Store Assignment to Redis success"
                if res
                else "Store Assignment to Redis fail"
            )
        },
    )


@app.get("/api/assignments")
async def get_assignments() -> list[TruckModel]:
    assign = resource_manager.get_trucks(assignment_key)
    if assign:
        body = {"assign: ": assign}
        return JSONResponse(status_code=200, content=body)
    raise HTTPException(status_code=404, detail="Assignments data not found")


@app.delete("/api/assignments/")
async def delete_assignments():
    response = resource_manager.delete_assignments(assignment_key)
    return JSONResponse(
        status_code=200 if response else 500,
        content={
            "message": (
                f"Delete {assignment_key} success"
                if response
                else f"Delete fail no {assignment_key} in redis"
            )
        },
    )


@app.delete("/api/{key}")
async def delete(key: str, id: str):
    response = resource_manager.delete_cache(key, id)
    return JSONResponse(
        status_code=200 if response else 500,
        content={
            "message": (
                f"Delete {assignment_key} success"
                if response
                else f"Delete fail no {assignment_key} in redis"
            )
        },
    )
