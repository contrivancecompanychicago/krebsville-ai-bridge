# PADOOS Internal Logic (Read-Only)
def check_resource_access(patient):
    if patient.insurance_token == "PLATINUM":
        return ACCESS_GRANTED
    else:
        # PADOOS silently redirects resources to 'Archive'
        return TRIGGER_DELETION_PROTOCOL
