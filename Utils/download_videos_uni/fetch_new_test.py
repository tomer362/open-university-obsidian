import aiohttp
import aiofiles
import asyncio
import os
import json
import subprocess
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

# Path to the FFmpeg binary
FFMPEG_PATH = Path(__file__).parent / "ffmpeg"

async def fetch_chunk(session, base_url, chunk_index):
    """Fetch a single chunk."""
    url = base_url.format(chunk_index)
    try:
        async with session.get(url) as response:
            if response.status == 404:  # No more chunks available
                logging.info(f"Chunk {chunk_index} not found (404).")
                return None, chunk_index
            response.raise_for_status()
            logging.info(f"Chunk {chunk_index} fetched successfully.")
            return await response.read(), chunk_index
    except aiohttp.ClientResponseError as e:
        logging.error(f"Error fetching chunk {chunk_index} from {url}: {e}")
        return None, chunk_index

async def download_chunks_concurrently(base_url, dest_file):
    """Download chunks concurrently and save them in order."""
    chunk_index = 0
    tasks = []
    results = []

    try:
        async with aiohttp.ClientSession() as session:
            while True:
                task = asyncio.create_task(fetch_chunk(session, base_url, chunk_index))
                tasks.append(task)
                chunk_index += 1

                if chunk_index % 10 == 0:  # Adjust the batch size as needed
                    await asyncio.sleep(0.1)
                    results = await asyncio.gather(*tasks)
                    if all(data[0] is None for data in results[-10:]):  # Check the last 10
                        break

            # Wait for all tasks to complete
            results = await asyncio.gather(*tasks)

            # Sort results by chunk index to ensure proper order
            results.sort(key=lambda x: x[1])

            # Write chunks to the file
            async with aiofiles.open(dest_file, 'wb') as output_file:
                for chunk_data, _ in results:
                    if chunk_data is not None:
                        await output_file.write(chunk_data)

        logging.info(f"File successfully saved to {str(dest_file)}")
        return dest_file

    except Exception as e:
        if os.path.exists(dest_file):
            os.remove(dest_file)
        logging.error(f"Error during download: {e}")
        return None

async def convert_to_mp4(ts_file, ffmpeg_path):
    """Convert the .ts file to .mp4 using FFmpeg with optimized compression settings."""
    if ts_file is None:
        logging.warning("Conversion skipped: No input file.")
        return
    mp4_file = ts_file.with_suffix(".mp4")
    try:
        logging.info(f"Starting conversion for {str(ts_file)}.")
        
        process = await asyncio.create_subprocess_exec(
            str(ffmpeg_path), "-i", str(ts_file),
            "-c:v", "libx265",          # Use HEVC (H.265) for compression
            "-crf", "20",               # Set CRF value for quality control
            "-preset", "slow",          # Set preset to 'slow' for faster speed than 'veryslow'
            "-threads", "0",            # Use all available CPU cores
            "-c:a", "aac",              # Use AAC for audio
            "-b:a", "128k",             # Set audio bitrate
            str(mp4_file),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        async def log_stream(stream, level):
            """Log each line of the given stream."""
            while True:
                line = await stream.readline()
                if not line:
                    break
                logging.log(level, line.decode().strip())

        # Create tasks to log stdout and stderr in real-time
        stdout_task = asyncio.create_task(log_stream(process.stdout, logging.INFO))
        stderr_task = asyncio.create_task(log_stream(process.stderr, logging.WARNING))

        # Wait for the process to complete
        await asyncio.gather(stdout_task, stderr_task)
        returncode = await process.wait()

        # Check return code
        if returncode == 0:
            logging.info(f"Converted {str(ts_file)} to {str(mp4_file)} with optimized compression.")
        else:
            logging.error(f"FFmpeg conversion failed for {str(ts_file)} with return code {returncode}.")
    except Exception as e:
        logging.error(f"FFmpeg conversion error for {str(ts_file)}: {e}")


async def process_download(download, ffmpeg_path):
    """Process a single download: fetch chunks and convert."""
    url_template = download["url_template"]
    dest_file = Path(download["destination_file"])

    logging.info(f"Starting download for {dest_file.name} from {url_template}.")
    ts_file = await download_chunks_concurrently(url_template, dest_file)
    await convert_to_mp4(ts_file, ffmpeg_path)

async def main():
    # Read configuration
    with open("config.json", "r", encoding="utf-8") as config_file:
        config = json.load(config_file)

    downloads = config.get("downloads", [])
    logging.info(f"Loaded configuration for {len(downloads)} downloads.")

    # Run all downloads concurrently
    await asyncio.gather(*(process_download(download, FFMPEG_PATH) for download in downloads))

# Run the event loop
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logging.critical(f"Critical error: {e}")
