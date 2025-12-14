import csv
import io
from typing import List, Any, Iterator
from fastapi.responses import StreamingResponse
from datetime import datetime


def get_column_names(model_instance) -> List[str]:
    """
    Extract column names from a SQLAlchemy model instance.

    Args:
        model_instance: A SQLAlchemy model instance

    Returns:
        List of column names as strings
    """
    if not model_instance:
        return []

    # Get the mapper for the model
    mapper = model_instance.__class__.__mapper__
    # Extract column names
    return [column.key for column in mapper.columns]


def stream_csv(data: List[Any], delimiter: str = ',') -> Iterator[str]:
    """
    A generator function that streams SQLAlchemy query results as CSV/TSV rows.
    This is memory-efficient as it yields rows one by one.

    Args:
        data: List of SQLAlchemy model instances
        delimiter: Field delimiter (',' for CSV, '\t' for TSV)

    Yields:
        CSV/TSV formatted rows as strings
    """
    if not data:
        return

    # Use a StringIO buffer for each row to use the csv writer
    output = io.StringIO()
    writer = csv.writer(output, delimiter=delimiter, quoting=csv.QUOTE_MINIMAL)

    # Get column names from first row
    column_names = get_column_names(data[0])

    # Yield header row
    writer.writerow(column_names)
    yield output.getvalue()
    output.seek(0)
    output.truncate(0)

    # Yield data rows
    for row in data:
        row_data = []
        for col in column_names:
            value = getattr(row, col, None)
            # Handle None values
            if value is None:
                row_data.append('')
            # Handle datetime objects
            elif isinstance(value, datetime):
                row_data.append(value.isoformat())
            else:
                row_data.append(str(value))

        writer.writerow(row_data)
        yield output.getvalue()
        output.seek(0)
        output.truncate(0)


def create_streaming_response(
    data: List[Any],
    filename: str,
    media_type: str,
    delimiter: str
) -> StreamingResponse:
    """
    Creates a memory-efficient StreamingResponse for CSV/TSV download.

    Args:
        data: List of SQLAlchemy model instances
        filename: Name of the file to download
        media_type: The media type for the response
        delimiter: The delimiter for the data (',' or '\t')

    Returns:
        FastAPI StreamingResponse with proper headers
    """
    # The stream_csv generator is passed directly to the response
    response = StreamingResponse(
        stream_csv(data, delimiter),
        media_type=media_type,
        headers={
            "Content-Disposition": f"attachment; filename={filename}",
            "Content-Type": f"{media_type}; charset=utf-8"
        }
    )
    return response


def create_csv_response(data: List[Any], filename: str = "export.csv") -> StreamingResponse:
    """
    Create a FastAPI StreamingResponse for CSV download with true streaming.

    Args:
        data: List of SQLAlchemy model instances
        filename: Name of the file to download

    Returns:
        FastAPI StreamingResponse with proper headers
    """
    return create_streaming_response(
        data=data,
        filename=filename,
        media_type="text/csv",
        delimiter=','
    )


def create_tsv_response(data: List[Any], filename: str = "export.tsv") -> StreamingResponse:
    """
    Create a FastAPI StreamingResponse for TSV download with true streaming.

    Args:
        data: List of SQLAlchemy model instances
        filename: Name of the file to download

    Returns:
        FastAPI StreamingResponse with proper headers
    """
    return create_streaming_response(
        data=data,
        filename=filename,
        media_type="text/tab-separated-values",
        delimiter='\t'
    )


def generate_filename(table_name: str, format: str = "csv", include_timestamp: bool = True) -> str:
    """
    Generate a standardized filename for exports.

    Args:
        table_name: Name of the database table
        format: File format ('csv' or 'tsv')
        include_timestamp: Whether to include timestamp in filename

    Returns:
        Formatted filename string
    """
    if include_timestamp:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"drugcentral_{table_name}_{timestamp}.{format}"
    else:
        return f"drugcentral_{table_name}.{format}"