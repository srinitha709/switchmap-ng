"""Module for querying the MacIp table."""

from sqlalchemy import select, update, and_, null, func

# Import project libraries
from switchmap.db import db
from switchmap.db.models import MacIp
from switchmap.db.misc import rows as _rows


def idx_exists(idx):
    """Determine whether primary key exists.

    Args:
        idx: idx_macip

    Returns:
        result: RMacIp object

    """
    # Initialize key variables
    result = False
    rows = []

    # Get data
    statement = select(MacIp).where(MacIp.idx_macip == idx)
    rows = db.db_select_row(1098, statement)

    # Return
    for row in rows:
        result = _rows.macip(row)
        break
    return result


def exists(idx_device, idx_mac, ip_):
    """Determine whether hostname exists in the MacIp table.

    Args:
        idx_device: Device.idx_device
        idx_mac: Mac.idx_mac
        ip_: IP address

    Returns:
        result: RMacIp tuple

    """
    # Initialize key variables
    result = False
    rows = []

    # Get row from dataase
    statement = select(MacIp).where(
        and_(
            MacIp.ip_ == ip_.encode(),
            MacIp.idx_mac == idx_mac,
            MacIp.idx_device == idx_device,
        )
    )
    rows = db.db_select_row(1201, statement)

    # Return
    for row in rows:
        result = _rows.macip(row)
        break
    return result


def findip(ipaddress):
    """Find IP address.

    Args:
        ipaddress: IP address

    Returns:
        result: RMacIp tuple

    """
    # Initialize key variables
    result = []
    rows = []

    # Get row from dataase
    statement = select(MacIp).where(MacIp.ip_ == ipaddress.encode())
    rows = db.db_select_row(1186, statement)

    # Return
    for row in rows:
        result.append(_rows.macip(row))
    return result


def findhostname(hostname):
    """Find hostname.

    Args:
        hostname: Hostname

    Returns:
        result: MacIp tuple

    """
    # Initialize key variables
    result = []
    rows = []

    # Get row from database (Contains)
    statement = select(MacIp).where(
        MacIp.hostname.like(func.concat(func.concat("%", hostname.encode(), "%")))
    )
    rows_contains = db.db_select_row(1191, statement)

    # Merge results and remove duplicates
    rows.extend(rows_contains)

    # Return
    for row in rows:
        result.append(_rows.macip(row))

    # Remove duplicates and return
    result = list(set(result))
    return result


def insert_row(rows):
    """Create a MacIp table entry.

    Args:
        rows: IMacIp objects

    Returns:
        None

    """
    # Initialize key variables
    inserts = []

    # Create list
    if isinstance(rows, list) is False:
        rows = [rows]

    # Create objects
    for row in rows:
        inserts.append(
            MacIp(
                idx_device=row.idx_device,
                idx_mac=row.idx_mac,
                ip_=row.ip_.encode(),
                hostname=(
                    null() if bool(row.hostname) is False else row.hostname.encode()
                ),
                version=row.version,
                enabled=row.enabled,
            )
        )

    # Insert
    if bool(inserts):
        db.db_add_all(1091, inserts)


def update_row(idx, row):
    """Upadate a MacIp table entry.

    Args:
        idx: idx_macip value
        row: IMacIp object

    Returns:
        None

    """
    # Update
    statement = (
        update(MacIp)
        .where(MacIp.idx_macip == idx)
        .values(
            {
                "idx_device": row.idx_device,
                "idx_mac": row.idx_mac,
                "ip_": row.ip_.encode(),
                "version": row.version,
                "hostname": (
                    null() if bool(row.hostname) is False else row.hostname.encode()
                ),
                "enabled": row.enabled,
            }
        )
    )
    db.db_update(1115, statement)
