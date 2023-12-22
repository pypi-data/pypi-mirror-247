import hypercorn.asyncio
import logging


async def serve_http(app, port=8000):
    config = hypercorn.Config()
    config.bind = [f"0.0.0.0:{int(port)}"]
    config.accesslog = logging.getLogger("hypercorn.access")
    config.access_log_format = '[%(s)s] %(m)s %(U)s?%(q)s [%(L)ss] %(b)s "%(h)s"'

    await hypercorn.asyncio.serve(app, config)
