# Update the door status to allow the move to Zone 1
db.collection('Zones').document('zone_0_administration').update({
    'systems.door_controls.bay_4_access': 'GRANTED',
    'metadata.is_locked': False
})
