def patch_httpx(async_client=True, sync_client: bool | None = None):
    if async_client:
        from ._async import patch_async_client

        patch_async_client()

    if sync_client is None:
        from .utils.sync import JSPI_SUPPORTED as sync_client

    if sync_client:
        from ._sync import patch_sync_client

        patch_sync_client()
