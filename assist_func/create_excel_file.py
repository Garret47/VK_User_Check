import pandas as pd
import io
from data import MAX_LOAD_BYTES_FILE


async def create_file(df: dict):
    files_bytes = {}
    for i in df:
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter', mode='w',
                            engine_kwargs={'options': {'strings_to_urls': False}}) as writer:
            df[i].to_excel(writer, sheet_name=f'{i}')
        if len(output.getvalue()) > MAX_LOAD_BYTES_FILE:
            files_bytes[i] = None
        else:
            files_bytes[i] = output
    return files_bytes
