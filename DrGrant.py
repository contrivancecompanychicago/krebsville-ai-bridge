import requests

webhook_url = "https://discord.com/api/webhooks/1454889886006903095/P9Om72cpC9ybFhIkPxNzNgedZc-b0xHvuKCmgFRWtPbTf-CN2RMCml6P_mJTGkkr12K1"
data = {
    "username": "Dr. Frederick Grant",
    "avatar_url": "URL_TO_GRANT_IMAGE",
    "content": "Sharma, the terminal is ready. Begin the audit of Batch #402."
}
requests.post(webhook_url, json=data)
