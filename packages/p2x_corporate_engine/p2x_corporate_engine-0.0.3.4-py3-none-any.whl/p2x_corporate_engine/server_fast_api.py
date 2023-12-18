import os
import asyncio
import json
import logging
from p2x_corporate_engine.engine import Engine
import yaml
from fastapi import FastAPI, Request
from p2x_corporate_engine.language_mapping import LANGUAGE_MAPPING
import pickle
logger = logging.getLogger("p2x_server")
logger.setLevel(logging.INFO)

app = FastAPI()

@app.on_event("startup")
async def startup():
    config = os.path.join(os.getenv('LOCAL_PATH'), "config.yml")
    app.state.lock = asyncio.Lock()

    with open(config, "r") as file:
        config = yaml.safe_load(file)
        app.state.engine = Engine(config)

    @app.get("/healthcheck")
    async def healthcheck():
        return "ok"

    @app.post("/isready")
    async def handle_ready():
        return {"rc": 0}

    @app.post("/translate")
    async def handle_translate(request: Request):
        lock = app.state.lock
        engine = app.state.engine

        try:
            req = await request.json()
            batch = None
            src_lc = req.get("src")
            tgt_lc = req.get("tgt")
            batch = req.get("srcs")
            logging.info((LANGUAGE_MAPPING[src_lc]))
            logging.info((LANGUAGE_MAPPING[tgt_lc]))

            translations = None
            translations = await engine.process_batch(batch, LANGUAGE_MAPPING[src_lc], LANGUAGE_MAPPING[tgt_lc], lock)
            ans = {
                "tus": []
            }
            for src, translation in zip(batch, translations):
                ans["tus"].append({"src": src, "tgt": translation})
            return ans

        except Exception as e:
            logging.exception("ERROR in handle_translate: " + str(e))
            logging.info("BATCH: " + str(batch))
            logging.info("TRANSLATIONS: " + str(translations))
            logging.info("REQ: " + str(req))
            response_obj = {'status': 'failed', 'reason': str(e)}
            return response_obj
