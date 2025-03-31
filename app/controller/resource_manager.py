import json
import logging
from fastapi import HTTPException
from typing import List
from app.models.base_model import AreaModel, TruckModel, AssignmentModel
from app.controller.redis_client import RedisClient


class ResourceManager:
    def __init__(self):
        self.redis_client = RedisClient()

    ## AREAS
    def get_area_by_id(self, key: str, area_id: str):
        res = self.redis_client.get_by_id(key, area_id)
        logging.info(f"Recieve data from cache key: {key}, id: {area_id}")
        return json.loads(res) if res else None

    def get_areas(self, key: str):
        res = self.redis_client.hashes_get(key)
        decoded_res = [
            json.loads(v.decode()) if isinstance(v, bytes) else v
            for k, v in res.items()
        ]

        logging.info(f"Recieve data from cache key: {key}")
        return decoded_res if decoded_res else None

    def add_areas(self, key: str, payload: List[AreaModel]) -> bool:
        set_res = []

        for area in payload:
            area_json = json.dumps(area.model_dump())
            res = self.redis_client.hashes_set(key, area.AreaID, area_json)

            set_res.append(res)

        print(all(set_res))

        if all(set_res):
            logging.info("Store Area to Redis success")
            return True
        else:
            return False

    ## TRUCKS
    def get_truck_by_id(self, key: str, truck_id: str):
        res = self.redis_client.get_by_id(key, truck_id)
        logging.info(f"Recieve data from cache key: {key}, id: {truck_id}")
        return json.loads(res) if res else None

    def get_trucks(self, key: str):
        res = self.redis_client.hashes_get(key)
        decoded_res = [
            json.loads(v.decode()) if isinstance(v, bytes) else v
            for k, v in res.items()
        ]
        logging.info(f"Recieve data from cache key: {key}")
        return decoded_res if decoded_res else None

    def add_trucks(self, key: str, payload: List[TruckModel]) -> bool:
        set_res = []

        for truck in payload:
            truck_json = json.dumps(truck.model_dump())
            res = self.redis_client.hashes_set(key, truck.TruckID, truck_json)

            set_res.append(res)

        if all(set_res):
            logging.info("Store Truck to Redis success")
            return True
        else:
            return False

    ## ASSIGNMENTS
    def add_assignments(self, assignments_key: str, area_key: str, truck_key: str):
        area = self.redis_client.hashes_get(area_key)
        truck = self.redis_client.hashes_get(truck_key)

        decoded_areas = [
            json.loads(v.decode()) if isinstance(v, bytes) else v
            for k, v in area.items()
        ]
        decoded_truck = [
            json.loads(v.decode()) if isinstance(v, bytes) else v
            for k, v in truck.items()
        ]
        process = self.process_assignment(decoded_areas, decoded_truck)
        for item in process:
            id = item["AreaID"]
            item = json.dumps(item)
            self.redis_client.hashes_set_assignment(assignments_key, id, item)

        return process

    def process_assignment(
        self, ares: list, trucks: list
    ) -> List[AssignmentModel]:
        # assign = self.redis_client.hashes_get(assignments_key)
        ares.sort(key=lambda x: x["UrgencyLevel"], reverse=True)

        assignments = []
        used_trucks = set()

        for area in ares:
            required = area["RequireResources"]
            best_truck = None

            # Find the best truck that meets the requirements and travel time
            for truck in trucks:
                if truck["TruckID"] in used_trucks:
                    continue

                available = truck["AvailableResources"]
                travel_time = truck["TravelTimeToArea"].get(
                    area["AreaID"], float("inf")
                )

                if (
                    all(available.get(res, 0) >= qty for res, qty in required.items())
                    and travel_time <= area["TimeConstrants"]
                ):
                    best_truck = truck
                    break
                elif any(available.get(res, 0) < qty for res, qty in required.items()):
                    logging.warning(
                        f"Truck {truck['TruckID']} does not have enough resources for area {area['AreaID']}."
                    )
                    missing_resources = [
                        res
                        for res, qty in required.items()
                        if available.get(res, 0) < qty
                    ]
                    if missing_resources:
                        logging.error(
                            f"Truck {truck['TruckID']} has partial resources for area {area['AreaID']}. Missing: {', '.join(missing_resources)}."
                        )

                        # under_resourced_trucks[truck["TruckID"]] = area["AreaID"]
                    # print(missing_resources)
                    # under_resourced_trucks[truck["TruckID"]] = area["AreaID"]
                elif travel_time > area["TimeConstrants"]:
                    logging.warning(
                        f"Truck {truck['TruckID']} cannot meet the time constraint for area {area['AreaID']}."
                    )
                    # under_time_trucks[truck["TruckID"]] = area["AreaID"]

            if best_truck:
                assignments.append(
                    {
                        "AreaID": area["AreaID"],
                        "TruckID": best_truck["TruckID"],
                        "ResourcesDelivered": area["RequireResources"],
                    }
                )
                used_trucks.add(best_truck["TruckID"])
            else:
                logging.warning(f"No suitable truck found for area {area['AreaID']}")

        # if
        # Filter the truck that insufficient resources
        # unused_trucks -= used_trucks  # Set difference to filter out used trucks
        # for truck_id in unused_trucks:
        #     logging.warning(f"Warning: Truck ID {truck_id} does not have enough resources")

        # # fetch TruckID from trucks
        # truck_ids = {truck['TruckID'] for truck in trucks}
        # print(truck_ids)

        # # fetch TruckID from assign
        # assigned_truck_ids = {
        #     (json.loads(value.decode()) if isinstance(value, bytes) else value)["TruckID"]
        #     for value in assign.values()
        # }
        # print(assigned_truck_ids)

        # if assigned_truck_ids == truck_ids:
        #     logging.warning("No truck available ")

        return assignments

    def get_assignments(self, key: str):
        res = self.redis_client.hashes_get(key)
        decoded_res = [
            json.loads(v.decode()) if isinstance(v, bytes) else v
            for k, v in res.items()
        ]
        logging.info(f"Recieve data from cache key: {key}")
        return decoded_res if decoded_res else None

    def delete_assignments(self, key: str):
        res = self.redis_client.delete(key)
        return res if res != 0 else None

    def delete_cache(self, key: str, id: str):
        res = self.redis_client.hashes_delete(key, id)
        return res if res != 0 else None
