from webfleet_connect.connection import Connection
from webfleet_connect.actions.action import Action

class Session:
  def __init__(self, credentials, config):
    self._credentials = credentials
    self._config = config

  def set_connection(self):
    self._connection = Connection(self)

  def has_json(self):
    return self._config.has_json()
  
  def _exec(self, action):
    return self._connection.exec(self._url(action))

  def _url(self, action):
    return f'{str(self._config)}&{str(self._credentials)}&{str(action)}'

  def create_queue_extern(self, args):
    return self._exec(Action('createQueueExtern', args))

  def delete_queue_extern(self, args):
    return self._exec(Action('deleteQueueExtern', args))

  def pop_queue_messages_extern(self, args):
    return self._exec(Action('popQueueMessagesExtern', args))

  def ack_queue_messages_extern(self, args):
    return self._exec(Action('ackQueueMessagesExtern', args))

  def show_object_report_extern(self, args = {}):
    return self._exec(Action('showObjectReportExtern', args))

  def show_vehicle_report_extern(self, args):
    return self._exec(Action('showVehicleReportExtern', args))

  def show_nearest_vehicles(self, args):
    return self._exec(Action('showNearestVehicles', args))

  def show_contracts(self, args):
    return self._exec(Action('showContracts', args))

  def update_vehicle(self, args):
    return self._exec(Action('updateVehicle', args))

  def show_object_groups(self, args):
    return self._exec(Action('showObjectGroups', args))

  def show_object_group_objects(self, args):
    return self._exec(Action('showObjectGroupObjects', args))

  def attach_object_to_group(self, args):
    return self._exec(Action('attachObjectToGroup', args))

  def detach_object_from_group(self, args):
    return self._exec(Action('detachObjectFromGroup', args))

  def insert_object_group(self, args):
    return self._exec(Action('insertObjectGroup', args))

  def delete_object_group(self, args):
    return self._exec(Action('deleteObjectGroup', args))

  def update_object_group(self, args):
    return self._exec(Action('updateObjectGroup', args))

  def switch_output(self, args):
    return self._exec(Action('switchOutput', args))

  def show_wakeup_timers(self, args):
    return self._exec(Action('showWakeupTimers', args))

  def update_wakeup_timers(self, args):
    return self._exec(Action('updateWakeupTimers', args))

  def get_object_features(self, args):
    return self._exec(Action('getObjectFeatures', args))

  def update_contract_info(self, args):
    return self._exec(Action('updateContractInfo', args))

  def get_object_can_signals(self, args):
    return self._exec(Action('getObjectCanSignals', args))

  def get_object_can_malfunctions(self, args):
    return self._exec(Action('getObjectCanMalfunctions', args))

  def get_electric_vehicle_data(self, args):
    return self._exec(Action('getElectricVehicleData', args))

  def get_active_asset_couplings(self, args):
    return self._exec(Action('getActiveAssetCouplings', args))

  def send_order_extern(self, args):
    return self._exec(Action('sendOrderExtern', args))

  def send_destination_order_extern(self, args):
    return self._exec(Action('sendDestinationOrderExtern', args))

  def update_order_extern(self, args):
    return self._exec(Action('updateOrderExtern', args))

  def update_destination_order_extern(self, args):
    return self._exec(Action('updateDestinationOrderExtern', args))

  def insert_destination_order_extern(self, args):
    return self._exec(Action('insertDestinationOrderExtern', args))

  def cancel_order_extern(self, args):
    return self._exec(Action('cancelOrderExtern', args))

  def assign_order_extern(self, args):
    return self._exec(Action('assignOrderExtern', args))

  def reassign_order_extern(self, args):
    return self._exec(Action('reassignOrderExtern', args))

  def delete_order_extern(self, args):
    return self._exec(Action('deleteOrderExtern', args))

  def clear_orders_extern(self, args):
    return self._exec(Action('clearOrdersExtern', args))

  def show_order_report_extern(self, args):
    return self._exec(Action('showOrderReportExtern', args))

  def show_order_waypoints(self, args):
    return self._exec(Action('showOrderWaypoints', args))

  def send_text_message_extern(self, args):
    return self._exec(Action('sendTextMessageExtern', args))

  def clear_text_messages_extern(self, args):
    return self._exec(Action('clearTextMessagesExtern', args))

  def show_messages(self, args):
    return self._exec(Action('showMessages', args))

  def send_binary_message(self, args):
    return self._exec(Action('sendBinaryMessage', args))

  def reset_binary_messages(self, args):
    return self._exec(Action('resetBinaryMessages', args))

  def clear_binary_messages(self, args):
    return self._exec(Action('clearBinaryMessages', args))

  def show_driver_report_extern(self, args):
    return self._exec(Action('showDriverReportExtern', args))

  def insert_driver_extern(self, args):
    return self._exec(Action('insertDriverExtern', args))

  def update_driver_extern(self, args):
    return self._exec(Action('updateDriverExtern', args))

  def delete_driver_extern(self, args):
    return self._exec(Action('deleteDriverExtern', args))

  def show_opti_drive_indicator(self, args):
    return self._exec(Action('showOptiDriveIndicator', args))

  def show_driver_groups(self, args):
    return self._exec(Action('showDriverGroups', args))

  def show_driver_group_drivers(self, args):
    return self._exec(Action('showDriverGroupDrivers', args))

  def attach_driver_to_group(self, args):
    return self._exec(Action('attachDriverToGroup', args))

  def detach_driver_from_group(self, args):
    return self._exec(Action('detachDriverFromGroup', args))

  def insert_driver_group(self, args):
    return self._exec(Action('insertDriverGroup', args))

  def delete_driver_group(self, args):
    return self._exec(Action('deleteDriverGroup', args))

  def update_driver_group(self, args):
    return self._exec(Action('updateDriverGroup', args))

  def attach_driver_to_vehicle(self, args):
    return self._exec(Action('attachDriverToVehicle', args))

  def detach_driver_from_vehicle(self, args):
    return self._exec(Action('detachDriverFromVehicle', args))

  def get_driver_rdt_rules(self, args):
    return self._exec(Action('getDriverRdtRules', args))

  def update_driver_rdt_rules(self, args):
    return self._exec(Action('updateDriverRdtRules', args))

  def show_address_report_extern(self, args):
    return self._exec(Action('showAddressReportExtern', args))

  def show_address_group_report_extern(self, args):
    return self._exec(Action('showAddressGroupReportExtern', args))

  def show_address_group_address_report_extern(self, args):
    return self._exec(Action('showAddressGroupAddressReportExtern', args))

  def insert_address_extern(self, args):
    return self._exec(Action('insertAddressExtern', args))

  def updateAddressExtern(self, args):
    return self._exec(Action('updateAddressExtern', args))

  def delete_address_extern(self, args):
    return self._exec(Action('deleteAddressExtern', args))

  def attach_address_to_group_extern(self, args):
    return self._exec(Action('attachAddressToGroupExtern', args))

  def detach_address_from_group_extern(self, args):
    return self._exec(Action('detachAddressFromGroupExtern', args))

  def insert_address_group_extern(self, args):
    return self._exec(Action('insertAddressGroupExtern', args))

  def delete_address_group_extern(self, args):
    return self._exec(Action('deleteAddressGroupExtern', args))

  def show_event_report_extern(self, args):
    return self._exec(Action('showEventReportExtern', args))

  def acknowledge_event_extern(self, args):
    return self._exec(Action('acknowledgeEventExtern', args))

  def resolve_event_extern(self, args):
    return self._exec(Action('resolveEventExtern', args))

  def get_event_forward_configs(self, args):
    return self._exec(Action('getEventForwardConfigs', args))

  def get_event_forward_config_recipients(self, args):
    return self._exec(Action('getEventForwardConfigRecipients', args))

  def insert_event_forward_config(self, args):
    return self._exec(Action('insertEventForwardConfig', args))

  def update_event_forward_config(self, args):
    return self._exec(Action('updateEventForwardConfig', args))

  def delete_event_forward_config(self, args):
    return self._exec(Action('deleteEventForwardConfig', args))

  def show_trip_report_extern(self, args):
    return self._exec(Action('showTripReportExtern', args))

  def show_trip_summary_report_extern(self, args):
    return self._exec(Action('showTripSummaryReportExtern', args))

  def show_tracks(self, args):
    return self._exec(Action('showTracks', args))

  def update_logbook(self, args):
    return self._exec(Action('updateLogbook', args))

  def show_logbook(self, args):
    return self._exec(Action('showLogbook', args))

  def show_logbook_history(self, args):
    return self._exec(Action('showLogbook_history', args))

  def update_logbook_mode(self, args):
    return self._exec(Action('updateLogbookMode', args))

  def update_logbook_driver(self, args):
    return self._exec(Action('updateLogbookDriver', args))

  def show_working_times(self, args):
    return self._exec(Action('showWorkingTimes', args))

  def show_stand_stills(self, args):
    return self._exec(Action('showStandStills', args))

  def show_idle_exceptions(self, args):
    return self._exec(Action('showIdleExceptions', args))

  def get_object_kpis(self, args):
    return self._exec(Action('getObjectKpis', args))

  def get_driver_kpis(self, args):
    return self._exec(Action('getDriverKpis', args))

  def get_remaining_driving_times_eu(self, args):
    return self._exec(Action('getRemainingDrivingTimesEu', args))

  def get_charger_connections(self, args):
    return self._exec(Action('getChargerConnections', args))

  def show_io_report_extern(self, args):
    return self._exec(Action('showIoReportExtern', args))

  def show_acceleration_events(self, args):
    return self._exec(Action('showAccelerationEvents', args))

  def show_speeding_events(self, args):
    return self._exec(Action('showSpeedingEvents', args))

  def show_digital_input_state_mileage(self, args):
    return self._exec(Action('showDigitalInputStateMileage', args))

  def get_charger_connections(self, args):
    return self._exec(Action('getChargerConnections', args))

  def geocode_address(self, args):
    return self._exec(Action('geocodeAddress', args))

  def calc_route_simple_extern(self, args):
    return self._exec(Action('calcRouteSimpleExtern', args))

  def show_settings(self, args):
    return self._exec(Action('showSettings', args))

  def create_session(self, args):
    return self._exec(Action('createSession', args))

  def terminate_session(self, args):
    return self._exec(Action('terminateSession', args))

  def show_account_order_states(self, args):
    return self._exec(Action('showAccountOrderStates', args))

  def update_account_order_state(self, args):
    return self._exec(Action('updateAccountOrderState', args))

  def show_account_order_automations(self, args):
    return self._exec(Action('showAccountOrderAutomations', args))

  def update_account_order_automation(self, args):
    return self._exec(Action('updateAccountOrderAutomation', args))

  def get_account_status_messages(self, args):
    return self._exec(Action('getAccountStatusMessages', args))

  def get_status_messages(self, args):
    return self._exec(Action('getStatusMessages', args))

  def set_vehicle_config(self, args):
    return self._exec(Action('setVehicleConfig', args))

  def get_vehicle_config(self, args):
    return self._exec(Action('getVehicleConfig', args))

  def set_status_messages(self, args):
    return self._exec(Action('setStatusMessages', args))

  def set_account_status_messages(self, args):
    return self._exec(Action('setAccountStatusMessages', args))

  def show_users(self, args):
    return self._exec(Action('showUsers', args))

  def change_password(self, args):
    return self._exec(Action('changePassword', args))

  def insert_maintenance_schedule(self, args):
    return self._exec(Action('insertMaintenanceSchedule', args))

  def update_maintenance_schedule(self, args):
    return self._exec(Action('updateMaintenanceSchedule', args))

  def delete_maintenance_schedule(self, args):
    return self._exec(Action('deleteMaintenanceSchedule', args))

  def show_maintenance_schedules(self, args):
    return self._exec(Action('showMaintenanceSchedules', args))

  def show_maintenance_tasks(self, args):
    return self._exec(Action('showMaintenanceTasks', args))

  def resolve_maintenance_task(self, args):
    return self._exec(Action('resolveMaintenanceTask', args))

  def get_archived_report_list(self, args):
    return self._exec(Action('getArchivedReportList', args))

  def get_archived_report(self, args):
    return self._exec(Action('getArchivedReport', args))

  def delete_archived_report(self, args):
    return self._exec(Action('deleteArchivedReport', args))

  def get_report_list(self, args):
    return self._exec(Action('getReportList', args))

  def create_report(self, args):
    return self._exec(Action('createReport', args))

  def send_report_via_mail(self, args):
    return self._exec(Action('sendReportViaMail', args))

  def get_areas(self, args):
    return self._exec(Action('getAreas', args))

  def insert_area(self, args):
    return self._exec(Action('insertArea', args))

  def delete_area(self, args):
    return self._exec(Action('deleteArea', args))

  def update_area(self, args):
    return self._exec(Action('updateArea', args))

  def get_area_points(self, args):
    return self._exec(Action('getAreaPoints', args))

  def get_area_assignments(self, args):
    return self._exec(Action('getAreaAssignments', args))

  def insert_area_assignment(self, args):
    return self._exec(Action('insertAreaAssignment', args))

  def delete_area_assignment(self, args):
    return self._exec(Action('deleteAreaAssignment', args))

  def get_area_schedules(self, args):
    return self._exec(Action('getAreaSchedules', args))

  def insert_area_schedule(self, args):
    return self._exec(Action('insertAreaSchedule', args))

  def delete_area_schedule(self, args):
    return self._exec(Action('deleteAreaSchedule', args))

  def send_aux_device_data(self, args):
    return self._exec(Action('sendAuxDeviceData', args))

  def get_local_aux_device_config(self, args):
    return self._exec(Action('getLocalAuxDeviceConfig', args))

  def configure_local_aux_device(self, args):
    return self._exec(Action('configureLocalAuxDevice', args))

  def get_remote_aux_device_config(self, args):
    return self._exec(Action('getRemoteAuxDeviceConfig', args))

  def configure_remote_aux_device(self, args):
    return self._exec(Action('configureRemoteAuxDevice', args))

  def remove_remote_aux_device_config(self, args):
    return self._exec(Action('removeRemoteAuxDeviceConfig', args))

  def clear_aux_device_data_queue(self, args):
    return self._exec(Action('clearAuxDeviceDataQueue', args))

  def reset_aux_device_data(self, args):
    return self._exec(Action('resetAuxDeviceData', args))

  def insert_external_event(self, args):
    return self._exec(Action('insertExternalEvent', args))

  def set_external_object_data(self, args):
    return self._exec(Action('setExternalObjectData', args))
