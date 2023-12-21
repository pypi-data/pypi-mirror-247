
import time
from typing import Optional, Dict, Union
import click
import openapi_client as client
from openapi_client import PostgresqlAssetState as AssetState
from .logger import log
from .helpers import TimeoutTracker, Uploader
from .logger import log


def from_betas(
        gender: Optional[client.EnumsGender], 
        betas: list[float], 
        name: str, 
        model_version: Optional[client.EnumsModelVersion],
        api_instance: client.CreateAvatarsFromBetasApi
        ) -> str:
    """Create avatar from betas."""
    betas_request = client.SchemasBetasAvatarRequest(
        betas=betas,
        gender=gender,
        name=name,
        modelVersion=model_version)

    try:
        # Creates avatar from betas
        api_response = api_instance.create_avatar_from_betas(betas_request)
    except Exception as e:
        raise click.ClickException("Exception when calling CreateAvatarsFromBetasApi->create_avatar_from_betas: %s\n" % e) from e
    if api_response.data is None or api_response.data.attributes is None:
        raise click.ClickException("Creating avatar from betas response came back empty")
    log.info(f"Creating an avatar from betas finished with state {AssetState(api_response.data.attributes.state).name}")
    return str(api_response.data.id)


def get_processing_state(api_instance: client.AvatarsApi, asset_id: str) -> AssetState:
    """List avatar to retrieve its state"""
    try:
        # List one avatar
        api_response = api_instance.describe_avatar(asset_id)
    except Exception as e:
        raise click.ClickException("Exception when calling AvatarsApi->describe_avatar: %s\n" % e) from e
    if api_response.data is None or \
        api_response.data.attributes is None:
        raise click.ClickException("Response came back empty")
    state = api_response.data.attributes.state
    if state == AssetState.ERROR:
        raise click.ClickException("Processing finished with state ERROR")
    else:
        return AssetState(state)


def request_avatar_from_images(api_instance: client.CreateAvatarFromImagesApi) -> str:
    """Initiate avatar from images creation"""
    try:
        api_response = api_instance.create_avatar_from_images()
    except Exception as e:
        raise click.ClickException("Exception when calling CreateAvatarFromImagesApi->create_avatar_from_images: %s\n" % e) from e
    if api_response.data is None:
        raise click.ClickException("Initiating avatar from images response came back empty")
    asset_id = str(api_response.data.id)
    log.info(f"AssetID: {asset_id}")
    return asset_id

def request_avatar_from_scans(api_instance: client.CreateAvatarFromScansApi) -> str:
    """Initiate avatar from scans creation"""
    try:
        api_response = api_instance.create_avatar_from_scans()
    except Exception as e:
        raise click.ClickException("Exception when calling CreateAvatarFromScansApi->create_avatar_from_scans: %s\n" % e) from e
    if api_response.data is None:
        raise click.ClickException("Initiating avatar from scans response came back empty")
    asset_id = str(api_response.data.id)
    log.info(f"AssetID: {asset_id}")
    return asset_id

def request_image_upload(
        api_instance: client.CreateAvatarFromImagesApi,
        asset_id: str
        ) -> str:
    """Request image upload URL for avatar creation"""
    try:
        api_response = api_instance.upload_image_to_avatar(asset_id)
    except Exception as e:
        raise click.ClickException("Exception when calling CreateAvatarFromImagesApi->upload_image_to_avatar: %s\n" % e) from e
    if api_response.data is None or \
            api_response.data.attributes is None or \
            api_response.data.attributes.url is None:
        raise click.ClickException("Requesting image upload response came back empty")
    upload_url = str(api_response.data.attributes.url.path)
    return upload_url

def request_scan_upload(
        api_instance: client.CreateAvatarFromScansApi,
        asset_id: str
        ) -> str:
    """Request image upload URL for avatar creation"""
    try:
        api_response = api_instance.upload_mesh_to_avatar(asset_id)
    except Exception as e:
        raise click.ClickException("Exception when calling CreateAvatarFromScansApi->upload_mesh_to_avatar: %s\n" % e) from e
    if api_response.data is None or \
            api_response.data.attributes is None or \
            api_response.data.attributes.url is None:
        raise click.ClickException("Requesting image upload response came back empty")
    upload_url = str(api_response.data.attributes.url.path)
    return upload_url


def from_images(gender: Optional[client.EnumsGender],
                name: str,
                input: str,
                height: int,
                weight: int,
                image_mode: str,
                api_instance_images: client.CreateAvatarFromImagesApi,
                api_instance_avatars: client.AvatarsApi,
                uploader: Uploader,
                timeout: int
                ) -> str:
    """Create avatar from images."""

    asset_id = request_avatar_from_images(api_instance=api_instance_images)

    upload_url = request_image_upload(api_instance=api_instance_images, asset_id=asset_id)

    uploader.upload(file_to_upload=input, upload_url=upload_url)

    # Fit to images
    afi_inputs = client.DocschemasDocAFIInputs(avatarname=name, 
                                                       gender=gender, 
                                                       height=height, 
                                                       weight=weight, 
                                                       imageMode=image_mode)
    try:
        api_response = api_instance_images.avatar_fit_to_images(asset_id, afi_inputs)
    except Exception as e:
        raise click.ClickException("Exception when calling CreateAvatarFromImagesApi->avatar_fit_to_images: %s\n" % e) from e
    if api_response.data is None or api_response.data.attributes is None:
            raise click.ClickException("Fitting to images response came back empty")
    
    # Wait for processing to finish
    timeout_tracker = TimeoutTracker(timeout)
    afi_state = ""
    while not afi_state == AssetState.READY and not timeout_tracker.timed_out():
        afi_state = get_processing_state(api_instance_avatars, asset_id)
        log.info(f"Avatar from images processing state: {afi_state.name}" if afi_state != AssetState.READY \
                 else f"Avatar from images processing finished with state {afi_state.name}")
        time.sleep(5)
    if not afi_state == AssetState.READY:
        # image creation didn't finish before it timed out
        raise click.ClickException("Avatar from images creation timed out.")
    return asset_id

def from_scans(gender: Optional[client.EnumsGender],
                name: str,
                input: str,
                init_pose: str,
                up_axis: str,
                look_axis: str,
                input_units: str,
                api_instance_scans: client.CreateAvatarFromScansApi,
                api_instance_avatars: client.AvatarsApi,
                uploader: Uploader,
                timeout: int
                ) -> str:
    """Create avatar from images."""

    asset_id = request_avatar_from_scans(api_instance=api_instance_scans)

    upload_url = request_scan_upload(api_instance=api_instance_scans, asset_id=asset_id)

    uploader.upload(file_to_upload=input, upload_url=upload_url)

    # Fit to images
    afs_inputs = client.DocschemasDocAFSInputs(avatarname=name,
                                                       gender=gender,
                                                       initPose=init_pose,
                                                       upAxis=up_axis,
                                                       lookAxis=look_axis,
                                                       inputUnits=input_units
                                                       )
    try:
        api_response = api_instance_scans.avatar_fit_to_scans(asset_id, afs_inputs)
    except Exception as e:
        raise click.ClickException("Exception when calling CreateAvatarFromScansApi->avatar_fit_to_scans: %s\n" % e) from e
    if api_response.data is None or api_response.data.attributes is None:
            raise click.ClickException("Fitting to scans response came back empty")
    
    # Wait for processing to finish
    timeout_tracker = TimeoutTracker(timeout)
    afs_state = ""
    while not afs_state == AssetState.READY and not timeout_tracker.timed_out():
        afs_state = get_processing_state(api_instance_avatars, asset_id)
        log.info(f"Avatar from scans processing state: {afs_state.name}" if afs_state != AssetState.READY \
                 else f"Avatar from scans processing finished with state {afs_state.name}")
        time.sleep(5)
    if not afs_state == AssetState.READY:
        # image creation didn't finish before it timed out
        raise click.ClickException("Avatar from scans creation timed out.")
    return asset_id


def from_measurements(gender: Optional[client.EnumsGender],
                name: str,
                measurements: Optional[Dict[str, Union[float, int]]],
                model_version: Optional[client.EnumsModelVersion],
                api_instance_from_measurements: client.CreateAvatarFromMeasurementsApi,
                api_instance_avatars: client.AvatarsApi,
                timeout: int
                ) -> str:
    """Create avatar from measurements."""
    afm_inputs = client.SchemasMeasurementAvatarRequest(gender=gender,
                                                                name=name,
                                                                measurements=measurements,
                                                                modelVersion=model_version)

    try:
        api_response = api_instance_from_measurements.avatar_from_measurements(afm_inputs)
    except Exception as e:
        raise click.ClickException("Exception when calling CreateAvatarFromMeasurementsApi->avatar_from_measurements: %s\n" % e) from e
    if api_response.data is None:
            raise click.ClickException("Avatar from measurements response came back empty")
    asset_id = str(api_response.data.id)
    
    # Wait for processing to finish
    timeout_tracker = TimeoutTracker(timeout)
    afm_state = ""
    while not afm_state == AssetState.READY and not timeout_tracker.timed_out():
        afm_state = get_processing_state(api_instance_avatars, asset_id)
        if afm_state == AssetState.READY:
            log.info(f"Avatar from measurements processing finished with state {afm_state.name}")
        else:
            log.info(f"Avatar from measurements processing state: {afm_state.name}")
            time.sleep(5)
    if not afm_state == AssetState.READY:
        # afm creation didn't finish before it timed out
        raise click.ClickException("Avatar from measurements creation timed out.")
    return asset_id
           

def try_get_download_url(
        api_instance: client.AvatarsApi,
        asset_id: str,
        input: client.DocschemasDocExportInputs) -> Optional[str]:
    """Initiate avatar export and call export endpoint to check on state"""
    try:
        # Call export avatar endpoint
        api_response = api_instance.export_avatar(asset_id, input)
    except Exception as e:
        raise click.ClickException("Exception when calling AvatarsApi->export_avatar: %s\n" % e) from e
    if api_response.data is None or \
        api_response.data.attributes is None or \
        api_response.data.attributes.url is None:
        raise click.ClickException("Export avatar response came back empty")
    # get current processing state and download url from api response
    state = api_response.data.attributes.state
    download_url = str(api_response.data.attributes.url.path)
    if state == AssetState.READY:
            # export finished with state ready, return results
            log.info(f"Exporting the created avatar finished with state {AssetState(state).name}")
            return download_url
    elif state == AssetState.ERROR:
        raise click.ClickException("Exporting finished with state ERROR")
    else:
        log.info(f"Exporting avatar state: {AssetState(state).name}")
        return None
        
        
def export( 
        asset_id: str, 
        download_format: str, 
        pose: str, 
        animation: str, 
        compatibility_mode: str,
        api_instance: client.AvatarsApi,
        timeout: int
        ) -> str:
    """Export avatar"""
    input = client.DocschemasDocExportInputs(
        format=download_format,
        pose=pose,
        animation=animation,
        compatibilityMode=compatibility_mode)
    timeout_tracker = TimeoutTracker(timeout)
    download_url =  None
    while not download_url and not timeout_tracker.timed_out():
        download_url = try_get_download_url(api_instance, asset_id, input)
        # if state is still processing or awaiting processing, call export enpoint again after waiting a bit
        time.sleep(5)
    if download_url is None:
        # export didn't return anything before it timed out
        raise click.ClickException("Export timed out.")
    return download_url