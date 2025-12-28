import asyncio

async def trigger_mainframe_boot(channel):
    boot_text = [
        "```ansi",
        "[2;34m[SYSTEM]: INITIALIZING KREBSVILLE_OS_V4.02...[0m",
        "[2;34m[SYSTEM]: LOADING PADOOS_LOGISTICS... [OK][0m",
        "[2;31m[WARNING]: MALICE_INTERFERENCE DETECTED IN ZONE 0[0m",
        "[2;35m[ARCHIVIST]: s e g m e n t a t i o n _ f a u l t[0m",
        "```"
    ]
    
    msg = await channel.send("`[BOOTING SYSTEM...]`")
    
    for line in boot_text:
        await asyncio.sleep(0.8) # Simulates system lag
        current_content = msg.content + "\n" + line
        await msg.edit(content=current_content)

    # The Final ASCII Flare
    ascii_art = """```
    ___________________________________________________
    | [ LOGIC ANCHOR: OFFLINE ]   [ EQUITY: 31% ]     |
    |_________________________________________________|
    ```"""
    await channel.send(ascii_art)
