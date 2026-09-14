import csv
import io
from typing import List, Any, Iterator
from fastapi.responses import StreamingResponse
from datetime import datetime


def get_column_names(model_instance, exclude_columns: List[str] = None) -> List[str]:
    """
    Extract column names from a SQLAlchemy model instance.

    Args:
        model_instance: A SQLAlchemy model instance
        exclude_columns: List of column names to exclude from output

    Returns:
        List of column names as strings
    """
    if not model_instance:
        return []

    # Get the mapper for the model
    mapper = model_instance.__class__.__mapper__
    # Extract column names
    columns = [column.key for column in mapper.columns]

    # Exclude specified columns
    if exclude_columns:
        columns = [col for col in columns if col not in exclude_columns]

    return columns


def stream_csv(data: List[Any], delimiter: str = ',', exclude_columns: List[str] = None) -> Iterator[str]:
    """
    A generator function that streams SQLAlchemy query results as CSV/TSV rows.
    This is memory-efficient as it yields rows one by one.

    Args:
        data: List of SQLAlchemy model instances
        delimiter: Field delimiter (',' for CSV, '\t' for TSV)
        exclude_columns: List of column names to exclude from output

    Yields:
        CSV/TSV formatted rows as strings
    """
    if not data:
        return

    # Use a StringIO buffer for each row to use the csv writer
    output = io.StringIO()
    # Use QUOTE_NONNUMERIC to properly quote strings (important for SMILES/InChI)
    writer = csv.writer(output, delimiter=delimiter, quoting=csv.QUOTE_NONNUMERIC)

    # Get column names from first row
    column_names = get_column_names(data[0], exclude_columns)

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
            # Keep numeric types as numbers (int, float) so QUOTE_NONNUMERIC doesn't quote them
            elif isinstance(value, (int, float)):
                row_data.append(value)
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
    delimiter: str,
    exclude_columns: List[str] = None
) -> StreamingResponse:
    """
    Creates a memory-efficient StreamingResponse for CSV/TSV download.

    Args:
        data: List of SQLAlchemy model instances
        filename: Name of the file to download
        media_type: The media type for the response
        delimiter: The delimiter for the data (',' or '\t')
        exclude_columns: List of column names to exclude from output

    Returns:
        FastAPI StreamingResponse with proper headers
    """
    # The stream_csv generator is passed directly to the response
    response = StreamingResponse(
        stream_csv(data, delimiter, exclude_columns),
        media_type=media_type,
        headers={
            "Content-Disposition": f"attachment; filename={filename}",
            "Content-Type": f"{media_type}; charset=utf-8"
        }
    )
    return response


def create_csv_response(data: List[Any], filename: str = "export.csv", exclude_columns: List[str] = None) -> StreamingResponse:
    """
    Create a FastAPI StreamingResponse for CSV download with true streaming.

    Args:
        data: List of SQLAlchemy model instances
        filename: Name of the file to download
        exclude_columns: List of column names to exclude from output

    Returns:
        FastAPI StreamingResponse with proper headers
    """
    return create_streaming_response(
        data=data,
        filename=filename,
        media_type="text/csv",
        delimiter=',',
        exclude_columns=exclude_columns
    )


def create_tsv_response(data: List[Any], filename: str = "export.tsv", exclude_columns: List[str] = None) -> StreamingResponse:
    """
    Create a FastAPI StreamingResponse for TSV download with true streaming.

    Args:
        data: List of SQLAlchemy model instances
        filename: Name of the file to download
        exclude_columns: List of column names to exclude from output

    Returns:
        FastAPI StreamingResponse with proper headers
    """
    return create_streaming_response(
        data=data,
        filename=filename,
        media_type="text/tab-separated-values",
        delimiter='\t',
        exclude_columns=exclude_columns
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